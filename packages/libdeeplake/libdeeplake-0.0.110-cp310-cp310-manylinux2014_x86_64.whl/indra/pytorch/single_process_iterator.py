from typing import Callable, List, Optional
from indra.pytorch.buffered_loader import BufferedLoader
from deeplake.core.compression import _decompress_dicom, _decompress_nifti

from indra.pytorch.util import (
    transform_collate_batch,
    get_indexes,
)
from indra.pytorch.tensorinfo import TensorsInfo, LoaderMetaInfo
from indra.pytorch.exceptions import (
    TransformExceptionWrapper,
)

from indra.pytorch.log import get_logger

from indra.pytorch.common import collate_fn as default_collate
from deeplake.integrations.pytorch.common import convert_sample_to_data
from deeplake.core.serialize import bytes_to_text
from indra.pytorch.create_dataloader import create_dataloader
from deeplake.enterprise.convert_to_libdeeplake import dataset_to_libdeeplake
from functools import partial


from PIL import Image
import traceback

import io
import os


# TODO take into consideration shuffle case
class SingleProcessDataLoader:
    def __init__(
        self,
        info: TensorsInfo,
        loader_meta: LoaderMetaInfo,
        transform_fn: Optional[Callable] = None,
        collate_fn: Optional[Callable] = default_collate,
        num_workers: int = 1,
        worker_id: int = 0,
        deeplake_dataset=None,
        drop_last: bool = False,
        batch_size: int = 1,
        num_threads: Optional[int] = None,
        tensors: Optional[List] = None,
        shuffle: bool = False,
        force_distribute: bool = False,
        ignore_cache: bool = False,
    ):
        """
        Returns an iterator for single process iteration

        Args:
            list_tensors (List[str], optional) Subset of raw tensors, these will be decompressed by python workers into lists.
            upcast (bool) flag that is showing whether we need to upcast object if dtype is not supported this is needed only for
                pytorch as it is not support all the dtypes. Defaults to True.
            transform_fn (Callable, optional) Callable object which is needed to be applyed on each sample on batch. Defaults to None.
            collate_fn (callable, optional): merges a list of samples to form a
                mini-batch of Tensor(s).  Used when using batched loading from a
                map-style dataset.
            ignore_errors(bool) shows whether need to ignore the errors appearing during transformation
            ignore_cache(bool) wheter need to ignore libdeeplake dataset while creating dataloader object
        """
        self.info = info
        self.loader_meta = loader_meta
        self.upcast = self.loader_meta.upcast
        self.transform_fn = transform_fn
        self.collate_fn = collate_fn
        self.ignore_cache = ignore_cache
        self.raw_tensor_set = (
            set(self.info.raw_tensors)
            - set(self.info.json_tensors)
            - set(self.info.list_tensors)
        )  # tensors to be returned as bytes

        self.helper_dict = {
            t: {
                "compression": deeplake_dataset[t].meta.sample_compression,
                "dtype": deeplake_dataset[t].dtype,
            }
            for t in self.info.medical_tensors
        }

        self.shuffle = shuffle
        self.deeplake_dataset = deeplake_dataset

        self.deeplake_dataset = (
            deeplake_dataset[
                get_indexes(
                    deeplake_dataset, batch_size=batch_size, sdrop_last=drop_last
                )
            ]
            if self.loader_meta.distributed and force_distribute
            else deeplake_dataset
        )

        self._dataloader = None

        self.iter_pos = None
        self.skipped = 0
        self.processed = 0
        self.pid = os.getpid()
        self.logger = get_logger(self.loader_meta.verbose)

        self.dl_create_fn = partial(
            create_dataloader,
            num_workers=num_workers,
            worker_id=worker_id,
            drop_last=drop_last,
            return_index=self.loader_meta.return_index,
            batch_size=batch_size,
            num_threads=num_threads,
            tensors=tensors,
            raw_tensors=list(
                set(
                    self.info.raw_tensors
                    + self.info.list_tensors
                    + self.info.json_tensors
                    + self.info.pil_compressed_tensors
                    + self.info.medical_tensors
                )
            ),
            shuffle=False,
            ignore_errors=self.loader_meta.ignore_errors,
            offset=self.loader_meta.offset,
        )

    @property
    def dataset(self):
        return (
            self.deeplake_dataset.query("SELECT * SAMPLE BY 1 REPLACE FALSE")
            if self.shuffle
            else self.deeplake_dataset
        )

    @property
    def dataloader(self):
        if not self._dataloader or self.shuffle:
            dataset = dataset_to_libdeeplake(
                self.dataset, ignore_cache=self.ignore_cache
            )
            self._dataloader = self.dl_create_fn(indra_dataset=dataset)
            return self._dataloader
        return self._dataloader

    def __iter__(self):
        self.reset()
        self.iter_pos = iter(self._dataloader)

        return self

    def reset(self):
        self.dataloader.reset()
        self.skipped = 0
        self.processed = 0

    def __next__(self):
        return self.get_data()

    def __len__(self) -> int:
        return len(self._dataloader)

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"SingleProcessDataLoader length {len(self)}"

    def _next_data(self):
        batch = next(self.iter_pos)
        for sample in batch:
            for tensor in self.info.pil_compressed_tensors:
                if isinstance(sample[tensor], (list, tuple)):
                    sample[tensor] = list(
                        Image.open(io.BytesIO(t)) for t in sample[tensor]
                    )
                else:
                    sample[tensor] = Image.open(io.BytesIO(sample[tensor]))
            for tensor in self.info.medical_tensors:
                if self.helper_dict[tensor]["compression"] == "nii":
                    dt = _decompress_nifti(sample[tensor])
                elif self.helper_dict[tensor]["compression"] == "nii.gz":
                    dt = _decompress_nifti(sample[tensor], gz=True)
                else:
                    dt = _decompress_dicom(sample[tensor])
                sample[tensor] = dt.astype(self.helper_dict[tensor]["dtype"])
            for tensor in self.info.json_tensors:
                sample[tensor] = bytes_to_text(sample[tensor], "json")
            for tensor in self.info.list_tensors:
                sample[tensor] = bytes_to_text(sample[tensor], "list")
            if self.info.htype_dict:
                convert_sample_to_data(
                    sample,
                    self.info.htype_dict,
                    self.info.ndim_dict,
                    self.info.tensor_info_dict,
                )
        return batch

    def get_data(self):
        while True:
            self.processed += 1
            batch = self._next_data()
            try:
                return transform_collate_batch(
                    batch,
                    self.transform_fn,
                    self.collate_fn,
                    self.upcast,
                    self.raw_tensor_set,
                )
            except Exception as ex:
                self.logger.debug(
                    f"SingleProcessDataLoader {self.pid} exception happened {ex}"
                )
                self.handle_exception(ex)
                if self.loader_meta.ignore_errors:
                    continue
                else:
                    raise

    def handle_exception(self, ex):
        self.processed -= 1
        if isinstance(ex, TransformExceptionWrapper):
            ex.processed = self.processed
            ex.skipped = self.skipped
            if self.loader_meta.ignore_errors:
                self.logger.info(
                    f"An exception happened during data handling exception: {ex} processed batches {ex.processed} skipped batched {ex.skipped}"
                )
            else:
                traceback.print_tb(ex.exception.__traceback__)
        else:
            if self.loader_meta.ignore_errors:
                self.logger.info(
                    f"An exception happened during data handling exception: {ex} processed batches {self.processed}"
                )
            else:
                traceback.print_tb(ex)
        self.skipped += 1

    def close(self):
        return
