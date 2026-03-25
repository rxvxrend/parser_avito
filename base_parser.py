"""Головной парсер карточек Avito, Auto.ru и Cian: антибот + прокси + парсинг."""

from auto_ru_parser import AutoRuParse
from avito_parser import AvitoParse
from cian_parser import CianParse
from utils.load_config import load_parser_config
from utils.parser.http.client import HttpClient
from utils.parser.proxies.proxy_factory import build_proxy


class BaseParser:
    def __init__(self, config_path: str = "utils/config.toml"):
        self.config = load_parser_config(config_path)
        self.proxy = build_proxy(self.config)
        self.http = HttpClient(
            proxy=self.proxy,
            timeout=20,
            max_retries=self.config.max_count_of_retry,
        )

    def fetch_data(self, url: str) -> str:
        response = self.http.request("GET", url)
        return response.text

    def parse_card(self, url: str):
        html = self.fetch_data(url)
        if "auto.ru" in url:
            return AutoRuParse.parse_html(url=url, html=html)
        if "cian.ru" in url:
            return CianParse.parse_html(url=url, html=html)
        if "avito.ru" in url:
            return AvitoParse.parse_html(url=url, html=html)