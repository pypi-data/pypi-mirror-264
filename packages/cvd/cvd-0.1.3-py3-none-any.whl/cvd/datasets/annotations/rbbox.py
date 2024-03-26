from typing import List, Tuple
from xml.etree.ElementTree import Element

from bs4.element import Tag
import numpy as np

from cvd.datasets.annotations.sbbox import BBoxXYXY, BBoxXYWH, BBoxXYCenterWH
from cvd.datasets.interfaces import Serializable, CustomSerializer, StateType


class RBBoxXYCenterWHA(Serializable, CustomSerializer):
    """Representation of rotated bounding boxing by using center point, width, height, and angles of bbox

    Args:
        x_center(float): x coordinate of rectangle center point (>= 0)
        y_center(float): y coordinate of rectangle center point (>= 0)
        width(float): width of rectangle (> 0)
        height(float): height of rectangle (> 0)
        angle(float): Angle of rectangle in degrees
    """
    def __init__(
            self,
            x_center: float,
            y_center: float,
            width: float,
            height: float,
            angle: float
    ):
        try:
            self.x_center = float(x_center)
            self.y_center = float(y_center)
            self.width = float(width)
            self.height = float(height)
            self.angle = float(angle)
        except (ValueError, TypeError) as e:
            raise Exception(f"Wrong bbox coordinates format. {e}")

        assert self.width > 0, f"width = {self.width}, but the width cannot be less or equal than 0."

        # TODO: Angle from 0 to 180 or any?
        # assert self.x_center >= self.width/2, f"x_center = {self.x_center}, " \
        #                                       f"but the x_center coordinate cannot be less than width/2."
        assert self.height > 0, f"height = {self.height}, but the height cannot be less than 0."
        # assert self.y_center >= self.height/2, f"y_center = {self.y_center}, " \
        #                                        f"but the y_center coordinate cannot be less than height/2."
        # assert self.angle >= 0, f"angle = {self.angle}, but the angle should be from 0 to 180"

    def __getstate__(self) -> StateType:
        return dict(
            x_center=self.x_center,
            y_center=self.y_center,
            width=self.width,
            height=self.height,
            angle=self.angle
        )

    def __setstate__(self, state: StateType):
        try:
            self.__init__(**state)
        except TypeError:
            raise TypeError("Wrong format in bbox state")

    def to_xml(self, tag: Tag) -> Tag:
        tag.attrs['x_center'] = self.x_center
        tag.attrs['y_center'] = self.y_center
        tag.attrs['width'] = self.width
        tag.attrs['height'] = self.height
        tag.attrs['angle'] = self.angle
        return tag

    @staticmethod
    def from_xml(tag: Element):
        return RBBoxXYCenterWHA(
            x_center=float(tag.attrib['x_center']),
            y_center=float(tag.attrib['y_center']),
            width=float(tag.attrib['width']),
            height=float(tag.attrib['height']),
            angle=float(tag.attrib['angle']),
        )

    def _4point(self) -> List[Tuple[float, float]]:
        c, s = np.cos(self.angle / 180 * np.pi), np.sin(self.angle / 180 * np.pi)
        rotation_matrix = np.asarray([[c, s], [-s, c]])
        pts = np.asarray(
            [
                [-self.width / 2, -self.height / 2],
                [self.width / 2, -self.height / 2],
                [self.width / 2, self.height / 2],
                [-self.width / 2, self.height / 2]
            ]
        )

        rect_points = []
        for pt in pts:
            rect_points.append(([self.x_center, self.y_center] + pt @ rotation_matrix))
        return list(map(lambda x: tuple(x.tolist()), rect_points))

    def contours(self) -> List[Tuple[float, float]]:
        return self._4point()

    def toxyxy(self):
        rect_points = self._4point()
        xmin = min([point[0] for point in rect_points])
        ymin = min([point[1] for point in rect_points])
        xmax = max([point[0] for point in rect_points])
        ymax = max([point[1] for point in rect_points])

        return BBoxXYXY(
            xmin=xmin,
            ymin=ymin,
            xmax=xmax,
            ymax=ymax
        )

    def toxywh(self):
        rect_points = self._4point()
        xmin = min([point[0] for point in rect_points])
        ymin = min([point[1] for point in rect_points])
        xmax = max([point[0] for point in rect_points])
        ymax = max([point[1] for point in rect_points])
        return BBoxXYWH(
            x=xmin,
            y=ymin,
            width=xmax-xmin,
            height=ymax-ymin
        )

    def toxycenterwh(self) -> BBoxXYCenterWH:
        rect_points = self._4point()
        xmin = min([point[0] for point in rect_points])
        ymin = min([point[1] for point in rect_points])
        xmax = max([point[0] for point in rect_points])
        ymax = max([point[1] for point in rect_points])
        return BBoxXYCenterWH(
            x_center=(xmax + xmin)/2,
            y_center=(ymax + ymin)/2,
            width=xmax-xmin,
            height=ymax - ymin
        )

    def toxycenterwha(self) -> 'RBBoxXYCenterWHA':
        return self

    def to_numpy(self) -> np.ndarray:
        """return boxes as float numpy array [x_center, y_center, width, height, angle]"""
        return np.array([self.x_center, self.y_center, self.width, self.height, self.angle], dtype=np.float)

    def __repr__(self):
        return f"{self.__class__.__name__}(x_center={self.x_center}, y_center={self.y_center}, " \
               f"width={self.width}, height={self.height}, angle={self.angle})"
