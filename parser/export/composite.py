#from loguru import logger

from dto import ParsedProduct
from parser.export.base import ResultStorage


class CompositeResultStorage(ResultStorage):
    def __init__(self, storages: list[ResultStorage]):
        if not storages:
            raise ValueError("CompositeResultStorage requires at least one storage")
        self.storages = storages

    def save(self, items: list[ParsedProduct]) -> None:
        if not items:
            return

        for storage in self.storages:
            try:
                storage.save(items)
            except Exception as e:
                print(f"Failed to save results using {storage.__class__.__name__}: {e}")
                #logger.exception(
                #    f"Failed to save results using {storage.__class__.__name__}: {e}"
                #)


class NullResultStorage(ResultStorage):
    def save(self, items: list[ParsedProduct]) -> None:
        pass
