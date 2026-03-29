from abc import ABC, abstractmethod
from typing import Iterable

import requests


class Proxy(ABC):
    @abstractmethod
    def get_httpx_proxy(self) -> str:
        pass

    @abstractmethod
    def handle_block(self):
        pass


class MobileProxy(Proxy):
    def __init__(self, url: str, change_ip_urls: Iterable[str]):
        self.url = url
        self.change_ip_urls = [item for item in change_ip_urls if item]

    def get_httpx_proxy(self) -> str:
        if "@" not in self.url:
            raise ValueError(
                "Некорректный proxy_string. Ожидается формат login:password@host:port"
            )
        return f"http://{self.url}"

    def handle_block(self):
        # смена IP на мобильном прокси: пробуем основную и резервные ссылки
        last_error = None
        for change_ip_url in self.change_ip_urls:
            try:
                requests.get(change_ip_url, timeout=10).raise_for_status()
                return
            except requests.RequestException as error:
                last_error = error

        if last_error:
            raise RuntimeError(
                "Не удалось сменить IP ни по одной ссылке смены IP"
            ) from last_error