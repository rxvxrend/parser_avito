from pathlib import Path

from dto import AvitoConfig
from parser.export.base import ResultStorage
from parser.export.composite import CompositeResultStorage, NullResultStorage
from parser.export.excel import ExcelStorage


def build_result_storage(config: AvitoConfig) -> ResultStorage:
    storages: list[ResultStorage] = []

    if config.save_xlsx:
        file_path = Path(config.output_dir) / "avito.xlsx"
        storages.append(ExcelStorage(file_path))

    if not storages:
        return NullResultStorage()

    return CompositeResultStorage(storages)
