import tomllib

from dto import AvitoConfig


def load_avito_config(path: str = "config.toml") -> AvitoConfig:
    with open(path, "rb") as f:
        data = tomllib.load(f)
    return AvitoConfig(**data["avito"])
