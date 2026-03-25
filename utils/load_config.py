import tomllib
from pathlib import Path

from .dto import ParserConfig


def load_parser_config(path: str = "utils/config.toml") -> ParserConfig:
    config_path = Path(path)
    with open(config_path, "rb") as f:
        data = tomllib.load(f)
    return ParserConfig(**data["parser"])