from copy import deepcopy
from typing import List, Union

from cvd.datasets.image_dataset import ImagesDataset
from cvd.datasets.video_dataset import VideoDataset


def merge(datasets: Union[List[ImagesDataset], List[VideoDataset]]):
    assert len(datasets), "Dataset list is empty"
    new_dataset = type(datasets[0])()

    for dataset in datasets:
        for ds_item in dataset:
            new_dataset.add_item(deepcopy(ds_item.file_info), deepcopy(ds_item.annotations))

    return new_dataset

