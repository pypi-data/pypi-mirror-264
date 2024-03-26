from abc import ABC, abstractmethod
from typing import Dict, List, Union, Tuple
from xml.etree.ElementTree import Element

from bs4 import BeautifulSoup
from bs4.element import Tag

SimpleType = Union[float, int, str, bool]
ListSimplyType = List[SimpleType]
StateType = Dict[str, Union[SimpleType, 'Serializable', list, tuple, dict]]


class Serializable(ABC):

    @abstractmethod
    def __setstate__(self, state: StateType):
        pass

    @abstractmethod
    def __getstate__(self) -> StateType:
        pass


class CustomSerializer(ABC):
    @abstractmethod
    def to_xml(self, soup: BeautifulSoup) -> Tag:
        pass

    @staticmethod
    @abstractmethod
    def from_xml(tag: Element):
        pass


class BBox(Serializable):
    @abstractmethod
    def contours(self) -> List[Tuple[float, float]]:
        pass


