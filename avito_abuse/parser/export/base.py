from abc import ABC, abstractmethod

from ...dto import ParsedProduct


class ResultStorage(ABC):
    name: str = "unknown"

    @abstractmethod
    def save(self, items: list[ParsedProduct]) -> None:
        pass
