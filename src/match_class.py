from abc import ABC, abstractmethod

class Match(ABC):
    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def add_matcher(self, sty: tuple[str, str, str]):
        pass

    @abstractmethod
    def match(self, mathcstr, pos) -> tuple[str, str, str]:
        pass