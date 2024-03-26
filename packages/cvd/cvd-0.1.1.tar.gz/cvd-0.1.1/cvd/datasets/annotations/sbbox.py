from dataclasses import dataclass
from typing import List, Tuple
from xml.etree.ElementTree import Element
import numpy as np

from bs4.element import Tag
from dataclasses_json import dataclass_json

from cvd.datasets.interfaces import StateType, CustomSerializer, BBox


class BBoxXYXY(BBox, CustomSerializer):
    def __init__(
            self,
            xmin: float,
            ymin: float,
            xmax: float,
            ymax: float
    ):
        """Representation of bounding boxing by using top left and bottom right corner coordinates

        Args:
            xmin (float): x coordinate of upper left corner of the rectangle (>= 0)
            ymin (float): y coordinate of upper left corner of the rectangle (>= 0)
            xmax (float): x coordinate of bottom right corner of the rectangle (> xmin)
            ymax (float): y coordinate of bottom right corner of the rectangle (> ymin)
        """
        try:
            self.xmin = float(xmin)
            self.xmax = float(xmax)
            self.ymin = float(ymin)
            self.ymax = float(ymax)
        except (ValueError, TypeError) as e:
            raise Exception(f"Wrong bbox coordinates format. {e}")
        assert self.xmin >= 0, f"xmin = {self.xmin}, but the xmin coordinate cannot be less than 0."
        assert self.xmin < self.xmax, f"xmin={self.xmin} and xmax={self.xmax}, but the xmax cannot be less or equal than xmin."
        assert self.ymin >= 0, f"ymin = {self.ymin}, but the ymin coordinate cannot be less than 0."
        assert self.ymin < self.ymax, f"ymin={self.ymin} and ymax={self.ymax}, but the ymax cannot be less or equal than ymin."

    def __getstate__(self) -> StateType:
        return dict(
            xmin=self.xmin,
            ymin=self.ymin,
            xmax=self.xmax,
            ymax=self.ymax
        )

    def __setstate__(self, state: StateType):
        try:
            self.__init__(**state)
        except TypeError:
            raise TypeError("Wrong format in bbox state")

    def to_xml(self, tag: Tag) -> Tag:
        tag.attrs['xtl'] = self.xmin
        tag.attrs['ytl'] = self.ymin
        tag.attrs['xbr'] = self.xmax
        tag.attrs['ybr'] = self.ymax
        return tag

    @staticmethod
    def from_xml(tag: Element):
        return BBoxXYXY(
            xmin=float(tag.attrib['xtl']),
            ymin=float(tag.attrib['ytl']),
            xmax=float(tag.attrib['xbr']),
            ymax=float(tag.attrib['ybr'])
        )

    def toxywh(self):
        return BBoxXYWH(
            x=self.xmin,
            y=self.ymin,
            width=self.xmax - self.xmin,
            height=self.ymax - self.ymin
        )

    def toxycenterwh(self):
        width = self.xmax - self.xmin
        height = self.ymax - self.ymin
        return BBoxXYCenterWH(
            x_center=self.xmin + width/2,
            y_center=self.ymin + height/2,
            width=width,
            height=height
        )

    def toxycenterwha(self):
        from cvd.datasets.annotations.rbbox import RBBoxXYCenterWHA
        width = self.xmax - self.xmin
        height = self.ymax - self.ymin
        return RBBoxXYCenterWHA(
            x_center=self.xmin + width/2,
            y_center=self.ymin + height/2,
            width=width,
            height=height,
            angle=0
        )

    def contours(self) -> List[Tuple[float, float]]:
        return [(self.xmin, self.ymin), (self.xmin, self.ymax), (self.xmax, self.ymax), (self.xmax, self.ymin)]

    def __repr__(self):
        return f"{self.__class__.__name__}(xmin={self.xmin}, ymin={self.ymin}, xmax={self.xmax}, ymax={self.ymax})"


@dataclass_json
@dataclass
class BBoxXYCenterWH:
    """Representation of bounding boxing by using center point, width, and height of bbox

    Args:
        x_center(float): x coordinate of rectangle center point (>= width/2)
        y_center(float): y coordinate of rectangle center point (>= height/2)
        width(float): width of rectangle (> 0)
        height(float): height of rectangle (> 0)
    """
    x_center: float
    y_center: float
    width: float
    height: float

    def __post_init__(self):
        try:
            self.x_center = float(self.x_center)
            self.y_center = float(self.y_center)
            self.width = float(self.width)
            self.height = float(self.height)
        except (ValueError, TypeError) as e:
            raise Exception(f"Wrong bbox coordinates format. {e}")
        assert self.width > 0, f"width = {self.width}, but the width cannot be less or equal than 0."
        assert self.x_center >= self.width/2, f"x_center = {self.x_center}, " \
                                  f"but the x_center coordinate cannot be less than width/2."
        assert self.height > 0, f"height = {self.height}, but the height cannot be less than 0."
        assert self.y_center >= self.height/2, f"y_center = {self.y_center}, " \
                                  f"but the y_center coordinate cannot be less than height/2."

    def toxyxy(self):
        half_width = self.width/2
        half_height = self.height/2
        return BBoxXYXY(
            xmin=self.x_center - half_width,
            ymin=self.y_center - half_height,
            xmax=self.x_center + half_width,
            ymax=self.y_center + half_height
        )

    def toxywh(self):
        half_width = self.width/2
        half_height = self.height/2
        return BBoxXYWH(
            x=self.x_center - half_width,
            y=self.y_center - half_height,
            width=self.width,
            height=self.height
        )

    def toxycenterwha(self):
        from cvd.datasets.annotations.rbbox import RBBoxXYCenterWHA
        return RBBoxXYCenterWHA(
            x_center=self.x_center,
            y_center=self.y_center,
            width=self.width,
            height=self.height,
            angle=0
        )

    def to_numpy(self) -> np.ndarray:
        """return boxes as float numpy array [x_center, y_center, width, height]"""
        return np.array([self.x_center, self.y_center, self.width, self.height], dtype=np.float32)

@dataclass_json
@dataclass
class BBoxXYWH:
    """Representation of bounding boxing by using top left corner coordinates, width and height

    Args:
        x(float): x coordinate of rectangle top left corner (>= 0)
        y(float): y coordinate of rectangle top left corner (>= 0)
        width(float): width of rectangle (> 0)
        height(float): height of rectangle (> 0)
    """
    x: float
    y: float
    width: float
    height: float

    def __post_init__(self):
        try:
            self.x = float(self.x)
            self.y = float(self.y)
            self.width = float(self.width)
            self.height = float(self.height)
        except (ValueError, TypeError) as e:
            raise Exception(f"Wrong bbox coordinates format. {e}")
        assert self.x >= 0, f"x = {self.x}, but the x coordinate cannot be less than 0."
        assert self.width > 0, f"width = {self.width}, but the width cannot be less or equal than 0."
        assert self.y >= 0, f"y = {self.y}, but the y coordinate cannot be less than 0."
        assert self.height > 0, f"height = {self.height}, but the height cannot be less or equal than 0."

    def toxyxy(self):
        return BBoxXYXY(
            xmin=self.x,
            ymin=self.y,
            xmax=self.x + self.width,
            ymax=self.y + self.height
        )

    def toxycenterwh(self):
        return BBoxXYCenterWH(
            x_center=self.x + self.width/2,
            y_center=self.y + self.height/2,
            width=self.width,
            height=self.height
        )

    def toxycenterwha(self):
        from cvd.datasets.annotations.rbbox import RBBoxXYCenterWHA
        return RBBoxXYCenterWHA(
            x_center=self.x + self.width/2,
            y_center=self.y + self.height/2,
            width=self.width,
            height=self.height,
            angle=0
        )