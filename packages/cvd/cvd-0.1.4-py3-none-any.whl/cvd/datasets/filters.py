from abc import ABC, abstractmethod
from typing import List, Union

from cvd.datasets.annotations.type import Object
from cvd.datasets.image_dataset_item import ImageDatasetItem
from cvd.datasets.video_dataset_item import VideoDatasetItem


class DatasetItemFilter(ABC):

    @abstractmethod
    def filter(self, ds_item: Union[ImageDatasetItem, VideoDatasetItem]):
        pass


class EmptyAnnotation(DatasetItemFilter):
    def __init__(self, exclude: bool = True):
        self._exclude = exclude

    def filter(self, ds_item: Union[ImageDatasetItem, VideoDatasetItem]):
        return not bool(ds_item.annotations.objects) if self._exclude else bool(ds_item.annotations.objects)


class ObjectsFilter(ABC):

    @abstractmethod
    def filter(self, obj: Object) -> bool:
        pass


class SmallObjectFilter(ObjectsFilter):
    def __init__(self, min_width: int, min_height: int):
        self._min_height = min_height
        self._min_width = min_width

    def filter(self, obj: Object) -> bool:
        bbox = obj.bbox_xywh()
        if bbox.width > self._min_width and bbox.height > self._min_height:
            return False
        return True


class IncludeLabelsFilter(ObjectsFilter):
    def __init__(self, include_labels: List[str]):
        self._include_labels = include_labels

    def filter(self, obj: Object) -> bool:
        if obj.label in self._include_labels:
            return False
        return True


class ExcludeLabelsFilter(ObjectsFilter):
    def __init__(self, exclude_labels: List[str]):
        self._exclude_labels = exclude_labels

    def filter(self, obj: Object) -> bool:
        if obj.label in self._exclude_labels:
            return True
        return False