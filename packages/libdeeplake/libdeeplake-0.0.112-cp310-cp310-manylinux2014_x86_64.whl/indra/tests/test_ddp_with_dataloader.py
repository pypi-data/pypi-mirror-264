import deeplake
import os
import torch.distributed as dist
import torch.multiprocessing as mp
from functools import partial
import os


class TorchDDPMnistIterator:
    def __init__(self):
        self.batch_count = [33, 33, 31]

    def identity(self, x):
        return x

    def setup(self, rank, world_size):
        os.environ["MASTER_ADDR"] = "localhost"
        os.environ["MASTER_PORT"] = "12356"

        dist.init_process_group("gloo", rank=rank, world_size=world_size)

    def cleanup(self):
        dist.destroy_process_group()

    def iterate_loader(self, rank, world_size):
        self.setup(rank, world_size)
        ds = deeplake.load("hub://activeloop/mnist-train")[0:200]
        dl = (
            ds.dataloader()
            .batch(2)
            .transform(self.identity)
            .pytorch(distributed=True, num_workers=2)
        )

        for batch_ids, _ in enumerate(dl):
            if batch_ids % 10 == 0:
                print(f"rank {rank}, batch {batch_ids}")

        assert self.batch_count[rank] == batch_ids
        self.cleanup()


class TorchDDPMnistIteratorWithException:
    def __init__(self):
        self.batch_count = [33, 33, 15]

    def identity(self, x, rank: int):
        if rank == 2 and (int(os.environ["INDRA_WORKER_ID"]) == 0):
            raise Exception("Transform exception happened")
        return x

    def setup(self, rank, world_size):
        os.environ["MASTER_ADDR"] = "localhost"
        os.environ["MASTER_PORT"] = "12356"

        dist.init_process_group("gloo", rank=rank, world_size=world_size)

    def cleanup(self):
        dist.destroy_process_group()

    def iterate_loader(self, rank, world_size):
        self.setup(rank, world_size)
        ds = deeplake.load("hub://activeloop/mnist-train")[0:200]
        dl = (
            ds.dataloader(ignore_errors=True)
            .batch(2)
            .transform(partial(self.identity, rank=rank))
            .pytorch(distributed=True, num_workers=2)
        )

        for batch_ids, _ in enumerate(dl):
            if batch_ids % 10 == 0:
                print(f"rank {rank}, batch {batch_ids}")

        assert self.batch_count[rank] == batch_ids
        self.cleanup()


def identity(x):
    return x


def identity_with_exception(x):
    if int(os.environ["INDRA_WORKER_ID"]) == 0:
        raise Exception("Transform exception happened")
    return x


#########################################
#      Iteration without shuffling      #
#########################################
def test_iterate_numpy_loader():
    ds = deeplake.load("hub://activeloop/mnist-train")[0:200]
    dl = (
        ds.dataloader()
        .batch(2)
        .transform(identity)
        .numpy(tensors=["labels"], num_workers=2)
    )
    for batch_id, dl in enumerate(dl):
        pass

    assert batch_id == 99


def test_iterate_numpy_loader_with_excption():
    ds = deeplake.load("hub://activeloop/mnist-train")[0:200]
    dl = (
        ds.dataloader(ignore_errors=True)
        .batch(2)
        .transform(identity_with_exception)
        .numpy(num_workers=2)
    )
    for batch_id, _ in enumerate(dl):
        pass

    assert batch_id == 49


def test_iterator_reinit():
    ds = deeplake.load("hub://activeloop/mnist-train")
    dl = (
        ds.dataloader()
        .transform(identity)
        .batch(2)
        .numpy(num_workers=2, tensors=["labels"])
    )
    labels_1 = []
    for idx, item in enumerate(dl):
        if idx == 10:
            break
        idx += 1
        labels_1.append(item[0]["labels"])
        labels_1.append(item[1]["labels"])

    labels_2 = []
    for idx, item in enumerate(dl):
        if idx == 10:
            break
        idx += 1
        labels_2.append(item[0]["labels"])
        labels_2.append(item[1]["labels"])

    assert labels_1 == labels_2


def test_iterator_reinit_with_persistant_worker():
    ds = deeplake.load("hub://activeloop/mnist-train")
    dl = (
        ds.dataloader()
        .transform(identity)
        .batch(2)
        .numpy(num_workers=2, tensors=["labels"], persistent_workers=True)
    )
    labels_1 = []
    for idx, item in enumerate(dl):
        if idx == 10:
            break
        idx += 1
        labels_1.append(int(item[0]["labels"]))
        labels_1.append(int(item[1]["labels"]))

    labels_2 = []
    for idx, item in enumerate(dl):
        if idx == 10:
            break
        idx += 1
        labels_2.append(int(item[0]["labels"]))
        labels_2.append(int(item[1]["labels"]))

    assert labels_1 == labels_2


#########################################
#         Iteration with shuffling      #
#########################################


def test_zero_worker_shuffle():
    ds = deeplake.load("hub://activeloop/mnist-train")[0:100]
    dl = (
        ds.dataloader(ignore_errors=True)
        .shuffle()
        .batch(1)
        .transform(identity)
        .pytorch(tensors=["labels"], num_workers=0, collate_fn=identity)
    )
    indexes_1 = []
    for batch_id, item in enumerate(dl):
        if batch_id == 10:
            break
        indexes_1.append(int(item[0]["index"]))

    indexes_2 = []
    for batch_id, item in enumerate(dl):
        if batch_id == 10:
            break
        indexes_2.append(int(item[0]["index"]))

    assert len(indexes_1) == len(indexes_2) == 10
    assert indexes_1 != indexes_2


def test_mp_torch_shuffle():
    ds = deeplake.load("hub://activeloop/mnist-train")[0:100]
    dl = (
        ds.dataloader(ignore_errors=True)
        .shuffle()
        .batch(1)
        .transform(identity)
        .pytorch(tensors=["labels"], num_workers=2, collate_fn=identity)
    )
    indexes_1 = []

    for batch_id, item in enumerate(dl):
        if batch_id == 10:
            break
        indexes_1.append(int(item[0]["index"]))

    indexes_2 = []
    for batch_id, item in enumerate(dl):
        if batch_id == 10:
            break
        indexes_2.append(int(item[0]["index"]))

    assert len(indexes_1) == len(indexes_2) == 10
    assert indexes_1 != indexes_2


def test_mp_numpy_shuffle():
    ds = deeplake.load("hub://activeloop/mnist-train")[0:100]
    dl = (
        ds.dataloader(ignore_errors=True)
        .shuffle()
        .batch(1)
        .transform(identity)
        .numpy(tensors=["labels"], num_workers=2)
    )
    indexes_1 = []
    for batch_id, item in enumerate(dl):
        if batch_id == 10:
            break
        indexes_1.append(int(item[0]["labels"]))

    indexes_2 = []
    for batch_id, item in enumerate(dl):
        if batch_id == 10:
            break
        indexes_2.append(int(item[0]["labels"]))

    assert len(indexes_1) == len(indexes_2) == 10
    assert indexes_1 != indexes_2


def test_torch_ddp_mnist_iterator():
    world_size = 3
    iter = TorchDDPMnistIterator()
    mp.spawn(iter.iterate_loader, args=(world_size,), nprocs=world_size)


def test_torch_ddp_mnist_iterator_with_exception():
    world_size = 3
    iter = TorchDDPMnistIteratorWithException()
    mp.spawn(iter.iterate_loader, args=(world_size,), nprocs=world_size)
