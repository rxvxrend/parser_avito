from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class AvitoConfig:
    urls: List[str]
    proxy_string: str
    proxy_change_url: str
    max_count_of_retry: int = 5
    pause_between_links: int = 1
    one_time_start: bool = True
    save_xlsx: bool = True
    output_dir: Path = Path("result")


@dataclass
class ParsedProduct:
    url: str
    title: str
    price: str
    description: str
