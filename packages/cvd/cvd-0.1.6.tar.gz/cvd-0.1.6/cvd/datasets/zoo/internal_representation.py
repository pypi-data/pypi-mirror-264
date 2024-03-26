from pathlib import Path
from typing import List, Set, Optional, Union
from cvd.datasets.annotations.image_annotation import ImageAnnotation
from cvd.datasets.annotations.video_annotation import VideoAnnotation
from cvd.datasets.interfaces import Serializable, StateType
from cvd.datasets.interfaces.idataset import IDataset
from cvd.datasets.meta import DatasetMeta, ImageFileInfo, VideoFileInfo


class _InternalFileMeta(Serializable):
    def __init__(
            self,
            file_info: Union[ImageFileInfo, VideoFileInfo],
            partial_path: Path,
            dataset_id: str,
            duplicate: bool
    ):
        """
            file_info: reference file info
            partial_path: partial path to data file relative data folder
            dataset_id: dataset identifier
            duplicate: True if file found in other datasets
        """
        self.partial_path: Path = partial_path
        self.dataset_id: str = dataset_id
        self.file_info = file_info
        self.duplicate: bool = duplicate

    def __getstate__(self) -> StateType:
        return dict(
            partial_path=str(self.partial_path),
            dataset_id=self.dataset_id,
            file_info=self.file_info,
            duplicate=self.duplicate
        )

    def __setstate__(self, state: StateType):
        partial_path = Path(state.pop('partial_path'))
        self.__init__(partial_path=partial_path, **state)


class _InternalDataset(Serializable):
    def __init__(
            self,
            dataset: IDataset,
            files: List[_InternalFileMeta],
            annotations: List[Union[ImageAnnotation, VideoAnnotation]]
    ):
        self.files = files
        self.annotations = annotations
        self.dataset = dataset

    def __setstate__(self, state):
        self.__init__(**state)

    def __getstate__(self):
        return dict(
            files=[fi for fi in self.files],
            annotations=[ann for ann in self.annotations],
            dataset=self.dataset
        )


class _InternalMeta:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.version = 0

    def inc_version(self):
        self.version += 1


class _InternalFilesMeta(_InternalMeta, Serializable, dict):

    def __getstate__(self) -> StateType:
        return dict(
            version=self.version,
            values=dict([(key, value) for key, value in self.items()])
        )

    def __setstate__(self, state: StateType):
        self.version = state["version"]
        for key, value in state['values'].items():
            self[key] = value

    def __getitem__(self, item) -> _InternalFileMeta:
        return super().__getitem__(item)


class _InternalDatasetMeta(Serializable):
    def __init__(
        self,
        dataset_meta: DatasetMeta,
        dataset_dependences: Optional[Union[Set, List]] = None
    ):
        self.dataset_meta = dataset_meta
        if dataset_dependences is not None:
            self.dataset_dependences = set(dataset_dependences)
        else:
            self.dataset_dependences = set()

    def add_dependency(self, parent_dataset_id: str):
        self.dataset_dependences = self.dataset_dependences | {parent_dataset_id}

    def __getstate__(self) -> StateType:
        return dict(
            dataset_meta=self.dataset_meta,
            dataset_dependences=list(self.dataset_dependences)
        )

    def __setstate__(self, state: StateType):
        self.__init__(**state)


class _InternalDatasetsMeta(_InternalMeta, Serializable, dict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __getstate__(self) -> StateType:
        state = dict(
            version=self.version,
            values=dict([(key, value) for key, value in self.items()]),
        )
        return state

    def __setstate__(self, state: StateType):
        self.version = state["version"]
        for key, value in state["values"].items():
            self[key] = value

    def __getitem__(self, item) -> _InternalDatasetMeta:
        return super().__getitem__(item)