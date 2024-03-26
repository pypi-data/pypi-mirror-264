import itertools
from typing import Optional, Dict, Tuple, Iterable

from cvd.datasets.annotations.type import ObjectsSet, Object, MarkupType
from cvd.datasets.annotations.objects import DetectionObjectPolygon, TrackGTObjectPolygon, \
                                         DetectionObjectBBox, TrackGTObjectBBox, PredictedObject, TrackPRObject

from cvd.datasets.interfaces.iannotation import IAnnotation
import numpy as np


class ImageAnnotation(IAnnotation):
    def __init__(
            self,
            objects: Optional[ObjectsSet] = None,
    ):
        """
            Class for working with markup image data, reading and converting
        Args:
            objects: List of objects that are on the image
        """
        # TODO: resolve the error "Parameterized generics cannot be used with class or instance checks"
        if objects is not None:
            assert isinstance(objects, Iterable), "Objects type must be iterable"
            assert not isinstance(objects, str), f"Wrong objects format"
        self._objects = tuple(objects) if objects is not None else tuple()
        self.check_objects_type(objects)
        self._labels = tuple(set([obj.label for obj in self.objects]))
        self._markup_type = self.get_markup_type()

    def is_empty(self) -> bool:
        return not bool(self._objects)

    @property
    def objects(self) -> Tuple[Object]:
        return self._objects

    def add_objects(self, objects: ObjectsSet):
        if objects:
            self.check_objects_type(objects)
            self._objects = tuple(itertools.chain(self._objects, objects))
            self._labels = tuple(set([obj.label for obj in self._objects]))
            self._markup_type = self.get_markup_type()

    def check_objects_type(self, objects):
        if not bool(objects):
            return

        if not self.is_empty():
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

    @property
    def labels(self) -> Tuple[str, ...]:
        return self._labels

    @property
    def markup_type(self) -> str:
        return self._markup_type

    def __getstate__(self) -> Dict:
        return dict(
            objects=[obj for obj in self._objects],
            labels=self._labels,
            markup_type=self._markup_type
        )

    def __setstate__(self, state):
        try:
            self.__init__(state["objects"])
        except (KeyError, TypeError):
            raise Exception("Wrong format of state params")

    def __len__(self):
        return len(self._objects)

    def to_numpy(self, label2index: Dict[str, int], format: str = 'xycenterwh') -> Optional[Tuple[np.ndarray, np.ndarray]]:
        if self._objects:
            if format == 'xycenterwh':
                bboxes = np.stack(list(map(lambda x: x.bbox.toxycenterwh().to_numpy(), self._objects)))
                labels = np.array(list(map(lambda x: label2index[x], map(lambda x: x.label, self._objects))))
                return bboxes, labels
            else:
                raise ValueError(f"Unknown format {format}. Use 'xycenterwh' format")
        return None

    def get_markup_type(self) -> Optional[MarkupType]:
        object_type = None

        if not self.is_empty():
            if isinstance(self._objects[0], (DetectionObjectPolygon, TrackGTObjectPolygon)):
                object_type = MarkupType.POLYGON.value
            elif isinstance(self._objects[0], (DetectionObjectBBox, TrackGTObjectBBox, PredictedObject, TrackPRObject)):
                object_type = MarkupType.BBOX.value
            else:
                raise TypeError(f"Markup object type not defined! Check objects data. self._objects[0] is {type(self._objects[0])}")

        return object_type
