import random
from copy import deepcopy
from typing import Tuple, Optional

from sklearn.model_selection import train_test_split

from cvd.datasets.image_dataset import ImagesDataset


def train_val_split(ds: ImagesDataset, train_size: float = 0.8, random_state: Optional[int]=None) -> Tuple[ImagesDataset, ImagesDataset]:
    train, val = train_test_split(ds, train_size=train_size, random_state=random_state)
    train_dataset = ImagesDataset(dataset_meta=deepcopy(ds.dataset_meta))
    for ds_item in train:
        train_dataset.add_item(ds_item.file_info, ds_item.annotations)
    train_dataset.dataset_meta.part = 'train'

    val_dataset = ImagesDataset(dataset_meta=deepcopy(ds.dataset_meta))
    for ds_item in val:
        val_dataset.add_item(ds_item.file_info, ds_item.annotations)
    val_dataset.dataset_meta.part = 'val'

    return train_dataset, val_dataset


def random_selection(ds: ImagesDataset, amount: int):
    total_amount = len(ds)
    selected_id = random.sample(range(total_amount), amount)
    return ds[selected_id]
