import itertools
from typing import Tuple, Optional, Dict
from cvd.datasets.annotations.type import MarkupType
from cvd.datasets.interfaces import Serializable
from cvd.datasets.interfaces.iannotation import IAnnotation
from cvd.datasets.annotations.type import ObjectsSet, Object, FramesSet
from cvd.datasets.annotations.rbbox import RBBoxXYCenterWHA
from cvd.datasets.annotations.objects import DetectionObjectPolygon, TrackGTObjectPolygon, \
                                         DetectionObjectBBox, TrackGTObjectBBox, PredictedObject, TrackPRObject

import pandas as pd


class Frame(Serializable):
    def __init__(
            self,
            objects: ObjectsSet,
            number: int
    ):
        """
            One frame of the video with marked objects
        Args:
            objects: list of marked objects in frame
            number: frame number
        Returns:
             Annotation of frame
        """
        assert isinstance(number, int), f"Incorrect type of argument `number`"
        assert number >= 0, f"Value of argument `number` must have >= 0"
        assert not isinstance(objects, str), f"Wrong objects format"
        self._number = number
        self._objects = tuple(objects) if objects is not None else tuple()
        self.check_objects_type(objects)
        self._labels = tuple(set([obj.label for obj in self.objects]))
        self._markup_type = self.get_markup_type()

    def __len__(self):
        return len(self._objects)

    @property
    def number(self) -> int:
        return self._number

    @property
    def objects(self) -> Tuple[Object]:
        return self._objects

    @property
    def labels(self) -> Tuple[str, ...]:
        return self._labels

    @property
    def markup_type(self) -> MarkupType:
        return self._markup_type

    def add_objects(self, objects: ObjectsSet):
        self.check_objects_type(objects)
        self._objects = tuple(itertools.chain(self._objects, objects))
        self._labels = tuple(set([obj.label for obj in self._objects]))
        self._markup_type = self.get_markup_type()

    def check_objects_type(self, objects):
        if not bool(objects):
            return

        if bool(self._objects):
            obj_type = type(self._objects[0])
            bbox_type = type(self._objects[0].bbox) if self.obj_type_is_bbox(self._objects[0]) else None
        else:
            obj_type = type(objects[0])
            bbox_type = type(objects[0].bbox) if self.obj_type_is_bbox(objects[0]) else None

        for obj in objects:
            if type(obj) != obj_type:
                raise Exception(f"Object type {type(obj)} not match {obj_type}. All objects must have the same type.")
            if self.obj_type_is_bbox(obj):
                if type(obj.bbox) != bbox_type:
                    raise Exception(f"Object type {type(obj.bbox)} not match {bbox_type}. "\
                                    f"All objects must have the same type.")

    def obj_type_is_bbox(self, obj):
        return True if isinstance(obj, (DetectionObjectBBox, PredictedObject, TrackGTObjectBBox, TrackPRObject)) \
                    else False

    def __getstate__(self) -> Dict:
        return dict(
            objects=self._objects,
            number=self._number,
            markup_type=self._markup_type
        )

    def __setstate__(self, state):
        try:
            self.__init__(state["objects"], state["number"])
        except (KeyError, TypeError):
            raise Exception("Wrong format objects in frame state")

    def __repr__(self):
        if self._objects:
            return f"{self.__class__.__name__}=(objects=[{self._objects[0]}, ...], number={self._number}," \
                   f" markup_type={self._markup_type})"
        return f"{self.__class__.__name__}=(objects=[], number={self._number})"

    def get_markup_type(self) -> MarkupType:
        if self._objects:
            if isinstance(self._objects[0], (DetectionObjectPolygon, TrackGTObjectPolygon)):
                return MarkupType.POLYGON.value
            elif isinstance(self._objects[0], (DetectionObjectBBox, TrackGTObjectBBox, PredictedObject, TrackPRObject)):
                return MarkupType.BBOX.value
            else:
                raise TypeError("Markup object type not defined! Check objects data")

        return None


class VideoAnnotation(IAnnotation):
    def __init__(
            self,
            frames: Optional[FramesSet] = None,
    ):
        """
            Class for working with markup video data, reading and converting
        Args:
            frames: List of objects that are on the image
        Returns:
            Video Annotation
        """
        assert not isinstance(frames, str), f"Wrong frame objects format"
        self._frames = dict()
        self._labels = tuple()
        if frames is not None:
            for frame in frames:
                self._frames[frame.number] = frame
            self._labels = tuple(set(itertools.chain(*[frame.labels for frame in self.frames])))
        self._markup_type = self.get_markup_type()

    def is_empty(self) -> bool:
        return not bool(self._frames)

    @property
    def frames(self) -> Tuple[Frame, ...]:
        all_frames: Tuple[Frame, ...] = tuple(self._frames.values())
        return all_frames

    @property
    def labels(self) -> Tuple[str, ...]:
        return self._labels

    @property
    def markup_type(self) -> MarkupType:
        return self._markup_type

    def rename_labels(self, rename_map: Dict[str, str]):
        for frame in self.frames:
            for obj in frame.objects:
                obj.label = rename_map[obj.label]
        self._labels = tuple(x for x in rename_map.values())

    def get_markup_type(self):
        for frame in self.frames:
            if frame.__len__() > 0:
                return frame.markup_type
        return None

    def __len__(self):
        return len(self._frames)

    def __getstate__(self) -> Dict:
        _frames = list(filter(lambda x: len(x), self._frames.values()))
        return dict(
            frames=_frames,
            markup_type=self._markup_type
        )

    def __setstate__(self, state):
        try:
            self.__init__(state['frames'])
            self._markup_type = self.get_markup_type()
        except (KeyError, TypeError):
            raise Exception("Wrong frame format in video state")

    def __getitem__(self, item: int) -> Optional[Frame]:
        if item in self._frames:
            return self._frames[item]
        else:
            return Frame(objects=[], number=item)

    def to_df(self) -> pd.DataFrame:
        """
        Not supported for rotated BBoxes. If bbox is rotated then it will be converted to simple rectangle bbox.
        """
        if self.markup_type is not None:
            assert self.markup_type == MarkupType.BBOX.value, \
                "Convertation video annotation to DataFrame not supported for polygon markup type"
            # TODO Convertation video annotation to DataFrame for polygon markup type

        _data = []
        bbox_params_names = None
        attributes_names = None
        _atts_names = None

        for frame in self.frames:
            for obj in frame.objects:
                _atts_names = list(obj.attributes.keys())
                _atts_values = obj.attributes.values()
                _bbox = obj.bbox

                if bbox_params_names is None:
                    if isinstance(_bbox, RBBoxXYCenterWHA):
                        bbox_params_names = ['x_center', 'y_center', 'width', 'height', 'angle']
                    else:
                        bbox_params_names = ['xmin', 'xmax', 'ymin', 'ymax']

                if attributes_names is None:
                    attributes_names = _atts_names
                else:
                    if attributes_names != _atts_names:
                        raise Exception("All additional attributes are not set on all frames "
                                        "or have different names.")
                if isinstance(_bbox, RBBoxXYCenterWHA):
                    bbox_params_values = (_bbox.x_center, _bbox.y_center, _bbox.width, _bbox.height, _bbox.angle)
                else:
                    bbox_params_values = (_bbox.xmin, _bbox.xmax, _bbox.ymin, _bbox.ymax)
                _data.append(
                    (frame.number,) +
                    bbox_params_values +
                    (obj.label,) +
                    tuple(_atts_values)
                )

        return pd.DataFrame(_data, columns=['frame_number'] + bbox_params_names + ['label'] +
                                            _atts_names if _atts_names is not None else [])

