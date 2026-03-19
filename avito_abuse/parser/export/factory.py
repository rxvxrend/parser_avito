from pathlib import Path

from ...dto import AvitoConfig
from .base import ResultStorage
from .composite import CompositeResultStorage, NullResultStorage
from .excel import ExcelStorage


def build_result_storage(config: AvitoConfig) -> ResultStorage:
    storages: list[ResultStorage] = []

    save_xlsx = bool(getattr(config, "save_xlsx", False))
    output_dir = Path(getattr(config, "output_dir", "result"))

    if save_xlsx:
        file_path = output_dir / "avito.xlsx"
        storages.append(ExcelStorage(file_path))

    if not storages:
        return NullResultStorage()

    return CompositeResultStorage(storages)
