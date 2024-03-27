from typing import List, Optional


def create_dataloader(
    indra_dataset,
    num_workers: int,
    worker_id: int,
    batch_size: int = 1,
    num_threads: int = None,
    tensors: Optional[List] = None,
    raw_tensors: Optional[List] = None,
    drop_last: bool = False,
    shuffle: bool = False,
    return_index: bool = True,
    ignore_errors: bool = True,
    offset: Optional[int] = 0,
):
    if num_threads is None:
        return indra_dataset.loader(
            num_workers=num_workers,
            worker_id=worker_id,
            batch_size=batch_size,
            tensors=tensors,
            raw_tensors=raw_tensors,
            drop_last=drop_last,
            shuffle=shuffle,
            return_index=return_index,
            ignore_errors=ignore_errors,
            offset=offset if offset else 0,
        )

    return indra_dataset.loader(
        num_workers=num_workers,
        worker_id=worker_id,
        batch_size=batch_size,
        num_threads=num_threads,
        tensors=tensors,
        raw_tensors=raw_tensors,
        drop_last=drop_last,
        shuffle=shuffle,
        return_index=return_index,
        ignore_errors=ignore_errors,
        offset=offset if offset else 0,
    )
