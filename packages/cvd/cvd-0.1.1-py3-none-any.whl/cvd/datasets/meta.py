from enum import Enum
from pathlib import Path
from typing import Union, Dict

from beartype import beartype
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config

from cvd.datasets.interfaces import Serializable, StateType


class DatasetPart(Enum):
    TRAIN = 'train'
    VALIDATION = 'val'
    TEST = 'test'
    ALL = 'all'


class DatasetType(Enum):
    IMAGE = 'image'
    VIDEO = 'video'


class DatasetMeta(Serializable):
    @beartype
    def __init__(
            self,
            name: str,
            version: str,
            description: str,
            part: Union[DatasetPart, str],
            dstype: Union[DatasetType, str]
    ):
        self._name = name
        self._version = version
        self._description = description
        if isinstance(part, str):
            self._part = DatasetPart(part)
        else:
            self._part = part

        if isinstance(dstype, str):
            self._dstype = DatasetType(dstype)
        else:
            self._dstype = dstype

    @property
    def name(self):
        return self._name

    @name.setter
    @beartype
    def name(self, value: str):
        self._name = value

    @property
    def version(self):
        return self._version

    @version.setter
    @beartype
    def version(self, value: str):
        self._version = value

    @property
    def part(self) -> DatasetPart:
        return self._part

    @part.setter
    @beartype
    def part(self, value: Union[str, DatasetPart]):
        if isinstance(value, str):
            self._part = DatasetPart(value)
        else:
            self._part = value

    @property
    def dstype(self) -> DatasetType:
        return self._dstype

    @dstype.setter
    @beartype
    def dstype(self, value: Union[str, DatasetType]):
        if isinstance(value, str):
            self._dstype = DatasetType(value)
        else:
            self._dstype = value

    @property
    def description(self):
        return self._description

    @description.setter
    @beartype
    def description(self, value: str):
        self._description = value

    def __setstate__(self, state):
        self.__init__(**state)

    def __getstate__(self) -> Dict:
        return dict(
            name=self._name,
            version=self._version,
            description=self._description,
            part=self._part.value,
            dstype=self._dstype.value
        )

    def to_dict(self) -> Dict:
        return self.__getstate__()

    @staticmethod
    def from_dict(state) -> 'DatasetMeta':
        new_ds_meta = DatasetMeta.__new__(DatasetMeta)
        new_ds_meta.__setstate__(state)
        return new_ds_meta

    def __repr__(self):
        return f"DatasetMeta(name={self._name}, version={self._version}, part={self.part.name}, " \
               f"dstype={self.dstype.name}, description={self._description[:20]}..."


class FileInfo(Serializable):
    def __init__(
            self,
            abs_path: Path,
            unique_id: str,
    ):
        """
            Args:
                abs_path: absolute path to data file
                unique_id: unique identifier for the file
        """
        self.abs_path = abs_path
        self.unique_id = unique_id

    def __getstate__(self) -> StateType:
        return dict(
            abs_path=str(self.abs_path),
            unique_id=self.unique_id,
        )

    def __setstate__(self, state: StateType):
        self.abs_path = Path(state["abs_path"])
        self.unique_id = state["unique_id"]

    def __repr__(self):
        return f"{self.__class__.__name__}(abs_path={str(self.abs_path)}, unique_id={self.unique_id}"


class ImageFileInfo(FileInfo):
    def __init__(self, abs_path: Path, unique_id: str, width: int, height: int):
        """
            Args:
                abs_path: absolute path to data file
                unique_id: unique identifier for the file
                height: height of image. The argument is optional, if not set it will be determined automatically
                width: width of image. The argument is optional, if not set it will be determined automatically
        """
        super().__init__(abs_path=abs_path, unique_id=unique_id)
        self.width = width
        self.height = height

    def __getstate__(self) -> StateType:
        _file_info_state = super().__getstate__()
        return dict(
            file_info=_file_info_state,
            width=self.width,
            height=self.height,
        )

    def __setstate__(self, state: StateType):
        super().__setstate__(state["file_info"])
        self.width = state["width"]
        self.height = state["height"]


class VideoFileInfo(FileInfo):
    def __init__(
            self,
            abs_path: Path,
            unique_id: str,
            width: int,
            height: int,
            fps: int,
            frames_number: int
    ):
        """
            Args:
                abs_path: absolute path to data file
                unique_id: unique identifier for the file
                height: height of image. The argument is optional, if not set it will be determined automatically
                width: width of image. The argument is optional, if not set it will be determined automatically
                fps: FPS of video file
                frames_number: Total frame numbers of video file
        """
        super().__init__(abs_path=abs_path, unique_id=unique_id)
        self.width = width
        self.height = height
        self.fps = fps
        self.frames_number = frames_number

    def __getstate__(self) -> StateType:
        _file_info_state = super().__getstate__()
        return dict(
            file_info=_file_info_state,
            width=self.width,
            height=self.height,
            fps=self.fps,
            frames_number=self.frames_number
        )

    def __setstate__(self, state: StateType):
        super().__setstate__(state["file_info"])
        self.width = state["width"]
        self.height = state["height"]
        self.fps = state["fps"]
        self.frames_number = state["frames_number"]
