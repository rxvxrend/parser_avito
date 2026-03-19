from dataclasses import dataclass


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
