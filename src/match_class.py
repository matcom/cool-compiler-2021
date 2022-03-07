from abc import ABC, abstractmethod
from typing import Tuple


class Match(ABC):
    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def add_matcher(self, sty: Tuple[str, str, str]):
        pass

    @abstractmethod
    def match(self, mathcstr, pos) -> Tuple[str, str, str]:
        pass
