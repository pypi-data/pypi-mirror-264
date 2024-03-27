from indra.pytorch.tensorinfo import TensorsInfo, LoaderMetaInfo
from typing import Callable, List, Optional
from indra.pytorch.common import collate_fn as default_collate


class MultiprocessDataloaderParams:
    def __init__(
        self,
        info: TensorsInfo,
        loader_meta: LoaderMetaInfo,
        transform_fn: Optional[Callable] = None,
        collate_fn: Optional[Callable] = default_collate,
        num_workers: int = 1,
        deeplake_dataset=None,
        drop_last: bool = False,
        batch_size: int = 1,
        num_threads: Optional[int] = None,
        tensors: Optional[List] = None,
        ignore_errors: bool = False,
        shuffle: bool = False,
    ):
        self.info = info
        self.loader_meta = loader_meta
        self.transform_fn = transform_fn
        self.collate_fn = collate_fn
        self.num_workers = num_workers
        self.deeplake_dataset = deeplake_dataset
        self.drop_last = drop_last
        self.batch_size = batch_size
        self.num_threads = num_threads
        self.tensors = tensors
        self.ignore_errors = ignore_errors
        self.shuffle = shuffle

    def __getstate__(self):
        return {
            "info": self.info,
            "loader_meta": self.loader_meta,
            "transform_fn": self.transform_fn,
            "collate_fn": self.collate_fn,
            "num_workers": self.num_workers,
            "deeplake_dataset": self.deeplake_dataset,
            "drop_last": self.drop_last,
            "batch_size": self.batch_size,
            "num_threads": self.num_threads,
            "tensors": self.tensors,
            "ignore_errors": self.ignore_errors,
            "shuffle": self.shuffle,
        }

    def __setstate__(self, state):
        self.info = state["info"]
        self.loader_meta = state["loader_meta"]
        self.transform_fn = state["transform_fn"]
        self.collate_fn = state["collate_fn"]
        self.num_workers = state["num_workers"]
        self.deeplake_dataset = state["deeplake_dataset"]
        self.drop_last = state["drop_last"]
        self.batch_size = state["batch_size"]
        self.num_threads = state["num_threads"]
        self.tensors = state["tensors"]
        self.ignore_errors = state["ignore_errors"]
        self.shuffle = state["shuffle"]
