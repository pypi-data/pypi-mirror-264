from itertools import repeat
from typing import Callable, List, Optional
from indra.pytorch.buffered_loader import BufferedLoader
from indra.pytorch.common import collate_fn as default_collate
from indra.pytorch.multiprocess_utils import (
    MP_STATUS_CHECK_INTERVAL,
    adjust_environment,
    early_transform_collate,
)
from indra.pytorch.util import (
    init_process_threads,
    process_initializer,
    create_folder,
)

from indra.pytorch.tensorinfo import TensorsInfo, LoaderMetaInfo
from indra.pytorch.mp_dataloader_params import MultiprocessDataloaderParams
from indra.pytorch.log import get_logger

import os
import dill as pickle


class MultiProcessingIterator:
    def __init__(
        self,
        info: TensorsInfo,
        loader_meta: LoaderMetaInfo,
        transform_fn: Optional[Callable] = None,
        collate_fn: Optional[Callable] = default_collate,
        worker_init_fn: Optional[Callable] = None,
        num_workers: int = 0,
        persistent_workers: bool = False,
        deeplake_dataset=None,
        drop_last: bool = False,
        batch_size: int = 1,
        num_threads: Optional[int] = None,
        tensors: Optional[List] = None,
        shuffle: bool = False,
    ):
        """
        Returns an iterator for single process iteration

        Args:
            info (TensorsInfo)
            loader_meta (LoaderMetaInfo)
            prefetch_factor (int) Number of samples loaded in advance by workers. Defaults to 10
            transform_fn (Callable, optional) Callable object which is needed to apply on each sample on batch. Defaults to None.
            collate_fn (callable, optional): merges a list of samples to form a
                mini-batch of Tensor(s).  Used when using batched loading from a
                map-style dataset.
            worker_init_fn (Callable, optional) function to initialise the child processes. Defaults to None.
            num_workers (int, optional): how many subprocesses to use for data
                loading. ``0`` means that the data will be loaded in the main process.
                (default: ``0``)
            persistent_workers (bool): If ``True``, the data loader will not shutdown the worker processes after a dataset has been consumed once. Defaults to ``False``.
            shuffle (bool, optional): set to ``True`` to have the data reshuffled at every epoch
                (default: ``False``).
        """

        assert num_workers > 0
        assert loader_meta.prefetch_factor > 0

        self.info = info
        self.loader_meta = loader_meta

        self.worker_init_fn = worker_init_fn or None
        self.num_workers = num_workers
        self.persistent_workers = persistent_workers or False
        self.workers_initialized = False
        self.persistent_workers = False
        self.deeplake_dataset = deeplake_dataset

        self.worker_ids = list(range(self.num_workers))
        self.finished_set = set()

        self.iter_pos = 0
        self.pool = None
        self.manager = None

        self.pid = os.getpid()
        self.logger = get_logger(self.loader_meta.verbose)

        init_process_threads()
        if loader_meta.context is None:
            import multiprocessing

            loader_meta.context = multiprocessing

        self.mp_dl_params = MultiprocessDataloaderParams(
            info=self.info,
            loader_meta=self.loader_meta,
            transform_fn=transform_fn,
            collate_fn=collate_fn,
            num_workers=self.num_workers,
            deeplake_dataset=deeplake_dataset,
            drop_last=drop_last,
            batch_size=batch_size,
            num_threads=num_threads,
            tensors=tensors,
            ignore_errors=self.loader_meta.ignore_errors,
            shuffle=shuffle,
        )

    @property
    def dataset(self):
        return (
            self.deeplake_dataset.query("SELECT * SAMPLE BY 1 REPLACE FALSE")
            if self.mp_dl_params.shuffle
            else self.deeplake_dataset
        )

    def __iter__(self):
        self.logger.info(f"Dataloader iterator initialization {self.pid}")

        if self.persistent_workers and self.pool is not None:
            self.set_stop_event()
            self.clear_queues()

        self.reset_positions()
        if self.pool is not None:
            if not self.persistent_workers:
                self.close()
                self.start_processes()
            self.run_workers()

        return self

    def __del__(self):
        self.free_resources()

    def __next__(self):
        if self.pool is None:
            self.start_processes()
            self.run_workers()
        elif (
            self.pool is not None
            and self.persistent_workers
            and not self.workers_initialized
        ):
            self.run_workers()
        return self.get_data()

    def reset_positions(self):
        self.iter_pos = 0
        self.finished_set = set()

    def clear_queues(self):
        self.logger.info(f"clear multiprocessing queues for process {self.pid}")
        for item in self.data_out_queues:
            while not item.empty():
                item.get_nowait()

    def start_processes(self):
        if self.pool is None:
            child_env = adjust_environment(self.num_workers)
            id_queue = self.loader_meta.context.Queue(maxsize=self.num_workers)
            for i in range(self.num_workers):
                id_queue.put(i)

            self.pool = self.loader_meta.context.Pool(
                processes=self.num_workers,
                initializer=process_initializer,
                initargs=(child_env, self.worker_init_fn, id_queue),
            )

            if self.manager is None:
                self.manager = self.loader_meta.context.Manager()

            self.data_out_queues = [
                self.manager.Queue(maxsize=self.loader_meta.prefetch_factor)
                for _ in range(self.num_workers)
            ]

        self.stop_events = [self.manager.Event() for _ in range(self.num_workers)]

    def run_workers(self):
        if self.mp_dl_params.shuffle:
            self.mp_dl_params.deeplake_dataset = self.dataset

        inp = list(
            zip(
                self.data_out_queues,
                self.stop_events,
                repeat(pickle.dumps(self.mp_dl_params)),
            )
        )

        self.workers_initialized = True
        self.pool.map_async(early_transform_collate, inp)

    def handle_stop_iteration(self, worker_id):
        self.finished_set.add(worker_id)

    def get_next_valid_id(self, wid):
        next_id = (wid + 1) % self.num_workers

        while next_id != wid:
            if next_id not in self.finished_set:
                return next_id
            next_id = (next_id + 1) % self.num_workers
        return None

    def get_data(self):
        out = None

        while True:
            wid = self.iter_pos % self.num_workers
            if wid in self.finished_set:
                wid = self.get_next_valid_id(wid)
                if wid is None:
                    raise StopIteration
            try:
                out = self.data_out_queues[wid].get(timeout=MP_STATUS_CHECK_INTERVAL)
                self.iter_pos += 1
            except Exception as ex:
                self.iter_pos += 1
                continue
            if isinstance(out, StopIteration):
                self.logger.info(f"StopIteration from worker {wid}")
                self.handle_stop_iteration(worker_id=wid)
                continue
            return out

    def set_stop_event(self):
        for idx, ev in enumerate(self.stop_events):
            if idx not in self.finished_set:
                ev.set()

    def close(self):
        if self.pool is not None:
            self.set_stop_event()
            self.logger.info(f"Closing dataloader iterator for process {self.pid}")
            self.pool.close()
            self.pool.join()
            self.pool = None
            self.workers_initialized = False

    def free_resources(self):
        self.close()
        if self.manager is not None:
            self.manager.shutdown()
            self.manager = None

    @staticmethod
    def _clean_up_worker(obj):
        obj.free_resources()

    def __len__(self):
        return self.length

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"MPIterator length {self.length} num_workers {self.num_workers}"
