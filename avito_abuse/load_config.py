import tomllib
from pathlib import Path

from .dto import AvitoConfig


def load_avito_config(path: str = "avito_abuse/config.toml") -> AvitoConfig:
    config_path = Path(path)
    with open(config_path, "rb") as f:
        data = tomllib.load(f)
    return AvitoConfig(**data["avito"])
