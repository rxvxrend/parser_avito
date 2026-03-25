from abc import ABC, abstractmethod

import requests


class Proxy(ABC):
    @abstractmethod
    def get_httpx_proxy(self) -> str:
        pass

    @abstractmethod
    def handle_block(self):
        pass


class MobileProxy(Proxy):
    def __init__(self, url: str, change_ip_url: str):
        self.url = url
        self.change_ip_url = change_ip_url

    def get_httpx_proxy(self) -> str:
        return f"http://{self.url}"

    def handle_block(self):
        # смена IP на мобильном прокси
        requests.get(self.change_ip_url, timeout=10)
