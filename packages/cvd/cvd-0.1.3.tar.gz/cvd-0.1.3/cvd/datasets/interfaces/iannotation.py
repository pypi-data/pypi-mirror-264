from abc import abstractmethod
from typing import Tuple

from cvd.datasets.interfaces import Serializable


class IAnnotation(Serializable):

    @property
    @abstractmethod
    def labels(self) -> Tuple[str, ...]:
        pass

    @abstractmethod
    def __len__(self) -> int:
        pass