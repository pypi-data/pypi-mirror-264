from indra.pytorch.single_process_iterator import SingleProcessDataLoader

from multiprocessing import current_process
import dill as pickle
import os
import warnings
import queue

MP_STATUS_CHECK_INTERVAL = 10.0
r"""Interval (in seconds) to check status of processes to avoid hanging in
    multiprocessing data loading. This is mainly used in getting data from
    another process, in which case we need to periodically check whether the
    sender is alive to prevent hanging."""


def adjust_environment(num_workers: int):
    child_env = os.environ.copy()

    # This code is referred from https://github.com/pytorch/pytorch/blob/master/torch/distributed/run.py
    if num_workers >= 1 and "OMP_NUM_THREADS" not in os.environ:
        omp_num_threads = 1
        warnings.warn(
            f"Setting OMP_NUM_THREADS environment variable for each process "
            f"to be {omp_num_threads} in default, to avoid your system being "
            f"overloaded, please further tune the variable for optimal "
            f"performance in your application as needed."
        )
        child_env["OMP_NUM_THREADS"] = str(omp_num_threads)
        os.environ["OMP_NUM_THREADS"] = str(omp_num_threads)

        if num_workers >= 1 and "MKL_NUM_THREADS" not in os.environ:
            mkl_num_threads = 1
            warnings.warn(
                f"Setting MKL_NUM_THREADS environment variable for each process "
                f"to be {mkl_num_threads} in default, to avoid your system being "
                f"overloaded, please further tune the variable for optimal "
                f"performance in your application as needed."
            )

            child_env["MKL_NUM_THREADS"] = str(mkl_num_threads)
            os.environ["MKL_NUM_THREADS"] = str(mkl_num_threads)

    return child_env


def early_transform_collate(inp):
    (
        data_out_queue,
        stop_event,
        mp_dl_params,
    ) = inp
    mp_dl_params = pickle.loads(mp_dl_params)

    single_iter = iter(
        SingleProcessDataLoader(
            info=mp_dl_params.info,
            loader_meta=mp_dl_params.loader_meta,
            transform_fn=mp_dl_params.transform_fn,
            collate_fn=mp_dl_params.collate_fn,
            num_workers=mp_dl_params.num_workers,
            worker_id=int(os.environ["INDRA_WORKER_ID"]),
            deeplake_dataset=mp_dl_params.deeplake_dataset,
            drop_last=mp_dl_params.drop_last,
            batch_size=mp_dl_params.batch_size,
            num_threads=mp_dl_params.num_threads,
            tensors=mp_dl_params.tensors,
            ignore_cache=True,
        )
    )

    while True:
        try:
            batch = next(single_iter)
            while True:
                try:
                    data_out_queue.put(batch, timeout=4.0)
                    break
                except Exception as ex:
                    if isinstance(ex, queue.Full):
                        if stop_event.is_set():
                            return
        except StopIteration:
            data_out_queue.put(StopIteration())
            return
