from typing import List, Tuple

from bs4.element import Tag
from xml.etree.ElementTree import Element

from cvd.datasets.interfaces import Serializable, CustomSerializer, StateType


class Polygon(Serializable, CustomSerializer):
    """Representation of object segment by using polygon line

    Args:
        points: list of points. Each point is represented by tuple[x, y]
        accept_negative: if false then point should be [x >= 0, y >= 0], otherwise can take any values
    """
    def __init__(
            self,
            points: List[Tuple[float, float]],
            accept_negative: bool = False
    ):
        try:
            self._points = points
            min_x = min(map(lambda x: x[0], points))
            min_y = min(map(lambda x: x[1], points))
        except (IndexError, TypeError, ValueError) as e:
            raise Exception(f"Wrong polygons points format. {e}")
        if not accept_negative:
            assert min_x >= 0, f"one of points has x coordinate less then 0, points={points}"
            assert min_y >= 0, f"one of points has y coordinate less then 0, points={points}"

    def __getstate__(self) -> StateType:
        return dict(
            points=self._points
        )

    def __setstate__(self, state: StateType):
        try:
            self.__init__(**state)
        except TypeError:
            raise TypeError("Wrong format in polygon state")

    def to_xml(self, tag: Tag) -> Tag:
        tag.attrs['points'] = ";".join(map(lambda x: ",".join(map(str, x)), self._points))
        return tag

    @staticmethod
    def from_xml(tag: Element):
        return Polygon(
            points=list(
                map(
                    lambda x: (float(x.split(",")[0]), float(x.split(",")[1])),
                    tag.attrib['points'].split(";")
                )
            ),
        )

    def contours(self) -> List[Tuple[float, float]]:
        return self._points

    @property
    def points(self) -> List[Tuple[float, float]]:
        return self._points
