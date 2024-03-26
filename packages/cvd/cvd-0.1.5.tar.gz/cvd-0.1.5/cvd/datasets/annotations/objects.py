from enum import Enum
from typing import Optional, Dict, Union, List, Tuple

from cvd.datasets.annotations.polygon import Polygon
from cvd.datasets.annotations.sbbox import BBoxXYXY, BBoxXYWH, BBoxXYCenterWH

from cvd.datasets.annotations.rbbox import RBBoxXYCenterWHA
from cvd.datasets.annotations.type import BBox
from cvd.datasets.interfaces import Serializable


class DetectionObjectPolygon(Serializable):
    """Storing and processing object information about on image.
    """
    def __init__(
            self,
            polygon: Polygon,
            label: str,
            attributes: Optional[Dict[str, Union[int, float, str]]] = None
    ):
        """

        Args:
            polygon (Polygon): The polygon that encloses the object
            label (str): object label
            attributes (Dict[str, Union[int, float, str]]): Additional attributes describing or characterizing the object
        """
        attributes = dict() if attributes is None else attributes
        assert isinstance(label, str), f"Incorrect type of argument `label`"
        assert isinstance(attributes, dict), f"Incorrect type of argument `attribute`"

        assert isinstance(polygon, Polygon), f"Incorrect type '{type(polygon)}' of argument `polygon` {type(Polygon)}"
        self._polygon = polygon
        self._label = label
        self._attributes = attributes

    @property
    def label(self) -> str:
        return self._label

    @label.setter
    def label(self, value: str):
        assert isinstance(value, str), f"Incorrect type of argument `label`"
        self._label = value

    @property
    def attributes(self):
        return self._attributes

    @attributes.setter
    def attributes(self, value):
        assert isinstance(value, dict), f"Incorrect type of argument `attribute`"
        self._attributes = value

    @property
    def polygon(self):
        return self._polygon

    @polygon.setter
    def polygon(self, value: Polygon):
        assert isinstance(value, Polygon), f"Incorrect type of argument `Polygon`"

    def contours(self) -> List[Tuple[float, float]]:
        return self._polygon.contours()

    def __getstate__(self):
        return dict(
            polygon=self._polygon,
            label=self.label,
            attributes=self.attributes
        )

    def __setstate__(self, state):
        try:
            self.__init__(**state)
        except TypeError:
            raise TypeError("Wrong format in DetectionObjectPolygon state")

    def __repr__(self):
        return f"{self.__class__.__name__}(polygon={self._polygon}, label={self._label}, attributes={self._attributes})"


class DetectionObjectBBox(Serializable):
    """Storing and processing object information about on image.
    """
    def __init__(
            self,
            bbox: BBox,
            label: str,
            attributes: Optional[Dict[str, Union[int, float, str]]] = None
    ):
        """

        Args:
            bbox (BBox): Information about bounding box
            label (str): object label
            attributes (Dict[str, Union[int, float, str]]): Additional attributes describing or characterizing the object
        """
        attributes = dict() if attributes is None else attributes
        assert isinstance(label, str), f"Incorrect type of argument `label`"
        assert isinstance(attributes, dict), f"Incorrect type of argument `attribute`"

        assert isinstance(bbox, (BBoxXYXY, BBoxXYWH, BBoxXYCenterWH, RBBoxXYCenterWHA)), \
            f"Incorrect type '{type(bbox)}' of argument `bbox`"
        if isinstance(bbox, (BBoxXYWH, BBoxXYCenterWH)):
            self._bbox = bbox.toxyxy()
        else:
            self._bbox = bbox
        self._label = label
        self._attributes = attributes

    @property
    def label(self) -> str:
        return self._label

    @label.setter
    def label(self, value: str):
        assert isinstance(value, str), f"Incorrect type of argument `label`"
        self._label = value

    @property
    def attributes(self):
        return self._attributes

    @attributes.setter
    def attributes(self, value):
        assert isinstance(value, dict), f"Incorrect type of argument `attribute`"
        self._attributes = value

    @property
    def bbox(self):
        return self._bbox

    @bbox.setter
    def bbox(self, value: BBox):
        assert isinstance(value, (BBoxXYXY, BBoxXYWH, BBoxXYCenterWH, RBBoxXYCenterWHA)), f"Incorrect type of argument `bbox`"
        if isinstance(value, (BBoxXYWH, BBoxXYCenterWH)):
            self._bbox = value.toxyxy()
        else:
            self._bbox = value

    def bbox_xyxy(self):
        if isinstance(self._bbox, RBBoxXYCenterWHA):
            return self._bbox.toxyxy()
        return self._bbox

    def bbox_xywh(self):
        return self._bbox.toxywh()

    def bbox_xycenterwh(self):
        return self._bbox.toxycenterwh()

    def contours(self) -> List[Tuple[float, float]]:
        return self._bbox.contours()

    def __getstate__(self):
        return dict(
            bbox=self._bbox,
            label=self.label,
            attributes=self.attributes
        )

    def __setstate__(self, state):
        try:
            self.__init__(**state)
        except TypeError:
            raise TypeError("Wrong format in DetectionObjectBbox state")

    def __repr__(self):
        return f"{self.__class__.__name__}(bbox={self._bbox}, label={self._label}, attributes={self._attributes})"


class TrackGTObjectPolygon(DetectionObjectPolygon):
    """ Storing and processing information about all tracked objects in video"""
    def __init__(
            self,
            polygon: Polygon,
            label: str,
            track_id: int,
            attributes: Optional[Dict[str, Union[int, float, str]]] = None
    ):
        """

        Args:
            polygon (Polygon): Information about marked points of polygon
            label (str): object label
            track_id (int): id of tracked object in video
            attributes (Dict[str, Union[int, float, str]]): Additional attributes describing or characterizing the object
        """
        assert isinstance(track_id, int), f"Track_id = {track_id}, but it's type must be integer"
        assert track_id >= 0, f"Track_id = {track_id}, but it's value must be >= 0"

        super().__init__(
            polygon=polygon,
            label=label,
            attributes=attributes
        )
        self._track_id = track_id

    @property
    def track_id(self):
        return self._track_id

    def __getstate__(self):
        return dict(
            polygon=self._polygon,
            label=self.label,
            track_id=self.track_id,
            attributes=self.attributes
        )


class TrackGTObjectBBox(DetectionObjectBBox):
    """ Storing and processing information about all tracked objects in video"""
    def __init__(
            self,
            bbox: BBox,
            label: str,
            track_id: int,
            attributes: Optional[Dict[str, Union[int, float, str]]] = None
    ):
        """

        Args:
            bbox (BBox): Information about bounding box
            label (str): object label
            track_id (int): id of tracked object in video
            attributes (Dict[str, Union[int, float, str]]): Additional attributes describing or characterizing the object
        """
        super().__init__(bbox=bbox, label=label, attributes=attributes)
        assert isinstance(track_id, int), f"Track_id = {track_id}, but it's type must be integer"
        assert track_id >= -1, f"Track_id = {track_id}, but it's value must be >= -1, -1 is untracked object"
        self._track_id = track_id

    @property
    def track_id(self):
        return self._track_id

    def __getstate__(self):
        return dict(
            bbox=self._bbox,
            label=self.label,
            track_id=self.track_id,
            attributes=self.attributes
        )

    def __repr__(self):
        return f"{self.__class__.__name__}(bbox={self._bbox}, label={self._label}, " \
               f"track_id={self._track_id}, attributes={self._attributes})"


class PredictedObject(DetectionObjectBBox):
    """ Result data predicted by detection model """
    def __init__(
            self,
            bbox: BBox,
            label: str,
            confidence: float = 1.0,
            attributes: Optional[Dict[str, Union[int, float, str]]] = None
    ):
        """

        Args:
            bbox (BBox): Information about bounding box
            label (str): object label
            confidence (float): confidence that object has specified label
            attributes (Dict[str, Union[int, float, str]]): Additional attributes describing or characterizing the object
        """
        super().__init__(bbox, label, attributes)
        assert isinstance(confidence, float), f"Incorrect type of argument `confidence`"
        self._confidence = confidence

    @property
    def confidence(self):
        return self._confidence

    def __getstate__(self):
        return dict(
            bbox=self.bbox,
            label=self.label,
            confidence=self.confidence,
            attributes=self.attributes
        )

    @staticmethod
    def from_dict(state):
        try:
            return PredictedObject(**state)
        except TypeError:
            raise TypeError("Wrong format in state params")

    def __repr__(self):
        return f"{self.__class__.__name__}(bbox={self._bbox}, label={self._label}, " \
               f"confidence={self._confidence}, attributes={self._attributes})"


class TrackPRObject(PredictedObject):
    """ Result data predicted by detection model with tracked objects"""
    def __init__(
            self,
            bbox: BBox,
            label: str,
            track_id: int,
            confidence: float = 1.0,
            attributes: Optional[Dict[str, Union[int, float, str]]] = None
    ):
        """

        Args:
            bbox (BBox): Information about bounding box
            label (str): object label
            track_id (int): id of tracked object in video
            confidence (float): confidence that object has specified label
            attributes (Dict[str, Union[int, float, str]]): Additional attributes describing or characterizing the object
        """
        super().__init__(bbox, label, confidence, attributes)
        assert isinstance(track_id, int), f"Track_id = {track_id}, but it's type must be integer"
        assert track_id >= 0, f"Track_id = {track_id}, but it's value must be >= 0"
        self._track_id = track_id

    @property
    def track_id(self):
        return self._track_id

    def __getstate__(self):
        return dict(
            bbox=self.bbox,
            label=self.label,
            track_id=self.track_id,
            confidence=self.confidence,
            attributes=self.attributes
        )

    @staticmethod
    def from_dict(state):
        try:
            return TrackPRObject(**state)
        except TypeError:
            raise TypeError("Wrong format in state params")

    def __repr__(self):
        return f"{self.__class__.__name__}(bbox={self._bbox}, label={self._label}, track_id={self._track_id}, " \
               f"confidence={self._confidence}, attributes={self._attributes})"


class ObjectType(Enum):
    TRACK_DETECTION = TrackGTObjectBBox.__name__
    TRACK_PREDICTED = TrackPRObject.__name__
    DETECTION = DetectionObjectBBox.__name__
    PREDICTED = PredictedObject.__name__

    @classmethod
    def has_key(cls, name):
        return name in cls.__members__
