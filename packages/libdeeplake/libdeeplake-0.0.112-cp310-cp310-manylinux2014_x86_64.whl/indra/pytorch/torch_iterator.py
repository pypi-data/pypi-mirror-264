try:
    import torch
    from torch.utils.data import DataLoader
    from typing import Callable, List, Optional
    from indra.pytorch.util import adjust_worker_init_fn
    from indra.pytorch.common import collate_fn as default_collate

    from indra.pytorch.tensorinfo import TensorsInfo, LoaderMetaInfo
    from indra.pytorch.mp_dataloader_params import MultiprocessDataloaderParams

    import os

    from indra.pytorch.single_process_iterator import SingleProcessDataLoader
    from indra.pytorch.util import get_indexes

    class CustomDataset(torch.utils.data.IterableDataset):
        def __init__(self, mp_dl_params: MultiprocessDataloaderParams):
            self.mp_dl_params = mp_dl_params
            self.__iter = None
            if self.mp_dl_params.loader_meta.distributed:
                indexes = get_indexes(
                    self.mp_dl_params.deeplake_dataset,
                    batch_size=self.mp_dl_params.batch_size,
                    drop_last=self.mp_dl_params.drop_last,
                )
                self.mp_dl_params.deeplake_dataset = self.mp_dl_params.deeplake_dataset[
                    indexes
                ]

        def __getstate__(self):
            return {
                "mp_dl_params": self.mp_dl_params,
                "__iter": None,
            }

        def _create_iterator(self):
            return iter(
                SingleProcessDataLoader(
                    info=self.mp_dl_params.info,
                    loader_meta=self.mp_dl_params.loader_meta,
                    transform_fn=self.mp_dl_params.transform_fn,
                    collate_fn=self.mp_dl_params.collate_fn,
                    num_workers=self.mp_dl_params.num_workers,
                    worker_id=int(os.environ["INDRA_WORKER_ID"]),
                    deeplake_dataset=self.mp_dl_params.deeplake_dataset,
                    drop_last=self.mp_dl_params.drop_last,
                    batch_size=self.mp_dl_params.batch_size,
                    num_threads=self.mp_dl_params.num_threads,
                    tensors=self.mp_dl_params.tensors,
                    force_distribute=False,
                    ignore_cache=True,
                )
            )

        def __setstate__(self, state):
            self.mp_dl_params = state["mp_dl_params"]
            self.__iter = None

        def __iter__(self):
            if self.__iter is None:
                self.__iter = self._create_iterator()
            else:
                self.__iter.reset()

            return self

        def __next__(self):
            try:
                item = next(self.__iter)
                return item
            except StopIteration:
                raise StopIteration

    class TorchIterator:
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
                deeplake_dataset: deeplake dataset that dataloader will create over (default: ``None``)
                drop_last (bool, optional): set to ``True`` to drop the last incomplete batch,
                    if the dataset size is not divisible by the batch size. If ``False`` and
                    the size of dataset is not divisible by the batch size, then the last batch
                    will be smaller. (default: ``False``)
                batch_size (int): size of the batch that dataloader need to return during each iteration (default: ``1``)
                num_threads (int, optional): number of threads that dataloader need to spin up (default: ``os.cpu_count()``)
                tensors (list, optional): lest of the tendors that dataloader needs to iterate over (default: ``None``)
                shuffle (bool, optional): set to ``True`` to have the data reshuffled at every epoch
                    (default: ``False``).
            """

            assert num_workers > 0
            assert loader_meta.prefetch_factor > 0
            self.info = info
            self.loader_meta = loader_meta

            self.prefetch_factor = self.loader_meta.prefetch_factor
            self.transform_fn = transform_fn
            self.collate_fn = collate_fn
            self.worker_init_fn = adjust_worker_init_fn(worker_init_fn)
            self.num_workers = num_workers
            self.persistent_workers = persistent_workers or False
            self.deeplake_dataset = deeplake_dataset

            self.ignore_errors = self.loader_meta.ignore_errors

            self.mp_dl_params = MultiprocessDataloaderParams(
                info=self.info,
                loader_meta=self.loader_meta,
                transform_fn=self.transform_fn,
                collate_fn=self.collate_fn,
                num_workers=self.num_workers,
                deeplake_dataset=deeplake_dataset,
                drop_last=drop_last,
                batch_size=batch_size,
                num_threads=num_threads,
                tensors=tensors,
                ignore_errors=self.ignore_errors,
                shuffle=shuffle,
            )

            self.iter_pos = None

        @property
        def dataset(self):
            return (
                self.deeplake_dataset.query("SELECT * SAMPLE BY 1 REPLACE FALSE")
                if self.mp_dl_params.shuffle
                else self.deeplake_dataset
            )

        def _create_iterator(self):
            if self.mp_dl_params.shuffle:
                self.mp_dl_params.deeplake_dataset = self.dataset

            self.iter_pos = iter(
                DataLoader(
                    CustomDataset(self.mp_dl_params),
                    num_workers=self.num_workers,
                    prefetch_factor=self.prefetch_factor,
                    worker_init_fn=self.worker_init_fn,
                    multiprocessing_context=self.loader_meta.context,
                    persistent_workers=self.persistent_workers,
                    collate_fn=self.identity,
                    batch_size=1,
                    pin_memory=self.loader_meta.pin_memory,
                    pin_memory_device=self.loader_meta.pin_memory_device,
                )
            )

        def identity(self, x):
            return x[0]

        def __iter__(self):
            self._create_iterator()
            return self

        def __next__(self):
            if self.iter_pos is None:
                self._create_iterator()
            return next(self.iter_pos)

except ImportError:
    pass
