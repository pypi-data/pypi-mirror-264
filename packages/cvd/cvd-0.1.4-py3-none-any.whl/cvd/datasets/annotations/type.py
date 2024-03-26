from typing import Union, List, Iterable, Tuple
from enum import Enum

from cvd.datasets.annotations.rbbox import RBBoxXYCenterWHA

Object = Union['DetectionObjectBBox', 'PredictedObject', 'TrackGTObjectBBox', 'TrackGTObjectPolygon',
               'DetectionObjectPolygon', 'TrackPRObject']
ObjectsSet = Union[List[Object], Tuple[Object], Iterable[Object]]
FramesSet = Union[List['Frame'], Tuple['Frame'], Iterable['Frame']]
ImageAnnotationSet = Union[List[Object], Tuple[Object], Iterable[Object]]
BBox = Union['BBoxXYXY', 'BBoxXYCenterWH', 'BBoxXYWH', RBBoxXYCenterWHA]


class MarkupType(Enum):
    POLYGON = 'polygon'
    BBOX = 'bbox'


