import re

from bs4 import BeautifulSoup

from avito_abuse.dto import AvitoConfig, ParsedProduct
from avito_abuse.hide_private_data import log_config
from avito_abuse.parser.http.client import HttpClient
from avito_abuse.parser.proxies.proxy_factory import build_proxy
from avito_abuse.version import VERSION


class AvitoParse:
    def __init__(self, config: AvitoConfig):
        self.config = config
        self.proxy = build_proxy(self.config)
        self.http = HttpClient(
            proxy=self.proxy,
            timeout=20,
            max_retries=self.config.max_count_of_retry,
        )
        log_config(config=self.config, version=VERSION)

    def parse_url(self, url: str) -> ParsedProduct:
        html_code = self.fetch_data(url)
        if not html_code:
            raise RuntimeError(f"Не удалось получить HTML для {url}")
        return self._parse_product_card(url=url, html=html_code)

    def fetch_data(self, url: str) -> str | None:
        try:
            response = self.http.request("GET", url)
            return response.text
        except Exception as err:
            print(f"Ошибка при запросе {url}: {err}")
            return None

    @staticmethod
    def _parse_product_card(url: str, html: str) -> ParsedProduct:
        soup = BeautifulSoup(html, "html.parser")

        title = (
            AvitoParse._meta_content(soup, "property", "og:title")
            or AvitoParse._text(soup.select_one("h1"))
            or ""
        )

        price = (
            AvitoParse._text(soup.select_one('[data-marker="item-view/item-price"]'))
            or AvitoParse._text(soup.select_one('[itemprop="price"]'))
            or AvitoParse._extract_price_by_regex(html)
            or ""
        )

        description = (
            AvitoParse._text(
                soup.select_one('[data-marker="item-view/item-description"]')
            )
            or AvitoParse._meta_content(soup, "name", "description")
            or ""
        )

        return ParsedProduct(
            url=url,
            title=title.strip(),
            price=price.strip(),
            description=description.strip(),
        )

    @staticmethod
    def _meta_content(soup: BeautifulSoup, attr: str, value: str) -> str | None:
        tag = soup.find("meta", attrs={attr: value})
        if tag:
            return tag.get("content")
        return None

    @staticmethod
    def _text(tag) -> str:
        if not tag:
            return ""
        return tag.get_text(" ", strip=True)

    @staticmethod
    def _extract_price_by_regex(html: str) -> str | None:
        match = re.search(r'"price"\s*:\s*\{[^}]*?"value"\s*:\s*(\d+)', html)
        if match:
            return match.group(1)
        return None
