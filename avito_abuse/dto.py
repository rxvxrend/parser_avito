from dataclasses import dataclass
from dataclasses import field


@dataclass
class AvitoConfig:
    proxy_string: str
    proxy_change_url: str
    max_count_of_retry: int = 5


@dataclass
class ParsedProduct:
    url: str
    title: str
    price: str
    description: str
    photos: list[str] = field(default_factory=list)