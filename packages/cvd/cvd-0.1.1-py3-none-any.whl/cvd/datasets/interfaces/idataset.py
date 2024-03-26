import logging
from abc import abstractmethod
from copy import deepcopy
from typing import Optional, Tuple, Dict

from cvd.datasets.filters import DatasetItemFilter
from cvd.datasets.interfaces.iannotation import IAnnotation
from cvd.datasets.interfaces.interface import Serializable, StateType
from cvd.datasets.meta import DatasetMeta, FileInfo


class DuplicationError(Exception):
    pass


class IDataset(Serializable):
    def __init__(self, dataset_meta: Optional[DatasetMeta] = None):
        self._dataset_meta: DatasetMeta = deepcopy(dataset_meta) if dataset_meta is not None else None
        self._annotations = {}
        # self._file_tags: Dict[str, Tags] = {}
        self._labels = []
        self._current = 0
        self._logger = logging.getLogger(self.__class__.__name__)

    @property
    def dataset_meta(self):
        return self._dataset_meta

    @dataset_meta.setter
    def dataset_meta(self, value: DatasetMeta):
        self._dataset_meta = value

    def __setstate__(self, state):
        self._files = []
        self._files_index = {}
        self._annotations = {}
        self._current = 0
        self._dataset_meta = state["dataset_meta"]
        for fi, ann in state["files_annotations"]:
            self._files.append(fi)
            self._annotations[fi.unique_id] = ann
            self._files_index[fi.unique_id] = fi
        self._labels = state["labels"]

    def __getstate__(self) -> StateType:
        return dict(
            files_annotations=[(fi, self._annotations[fi.unique_id]) for fi in self._files],
            labels=self._labels,
            dataset_meta=self._dataset_meta
        )

    def __len__(self):
        return len(self._files)

    def __iter__(self):
        self._current = 0
        return self

    @abstractmethod
    def __getitem__(self, value):
        pass

    @abstractmethod
    def __next__(self):
        pass

    @property
    def labels(self) -> Tuple[str, ...]:
        return tuple(self._labels)

    def update_labels(self):
        _labels = []
        for ds_item in self:
            _labels = sorted(list(set(_labels) | set(ds_item.annotations.labels)))
        self._labels = _labels

    def items_filter(self, items_filter: DatasetItemFilter):
        new_ds = type(self)()
        for ds_item in self:
            if not items_filter.filter(ds_item):
                new_ds.add_item(ds_item.file_info, ds_item.annotations)
        return new_ds

    def add_item(self, file_info: FileInfo, annotation: IAnnotation):
        if file_info.unique_id in self._annotations:
            raise DuplicationError(f"A file with a unique id `{file_info.abs_path} `exists in the dataset")

        self._files.append(file_info)
        unique_id = file_info.unique_id
        assert unique_id not in self._annotations, f"The unique_id in FileINfo isn't unique. " \
                                                   f"For the following id {unique_id} dataset contains following data:"\
                                                   f"file_info = {self._files_index[unique_id]} " \
                                                   f"and annotations = {self._annotations[unique_id]}"
        self._annotations[file_info.unique_id] = annotation
        self._files_index[file_info.unique_id] = file_info
        if len(annotation):
            self._labels = sorted(list(set(self.labels) | set(annotation.labels)))
