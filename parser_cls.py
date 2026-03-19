import re
import time

from bs4 import BeautifulSoup
#from loguru import logger

from dto import AvitoConfig, ParsedProduct
from hide_private_data import log_config
from load_config import load_avito_config
from parser.export.factory import build_result_storage
from parser.http.client import HttpClient
from parser.proxies.proxy_factory import build_proxy
from version import VERSION

#print("logs/app.log", rotation="5 MB", retention="5 days", level="DEBUG")


class AvitoParse:
    def __init__(self, config: AvitoConfig, stop_event=None):
        self.config = config
        self.proxy = build_proxy(self.config)
        self.stop_event = stop_event
        self.good_request_count = 0
        self.bad_request_count = 0
        self.http = HttpClient(
            proxy=self.proxy,
            timeout=20,
            max_retries=self.config.max_count_of_retry,
        )
        self.result_storage = build_result_storage(config=self.config)
        log_config(config=self.config, version=VERSION)

    def fetch_data(self, url: str) -> str | None:
        if self.stop_event and self.stop_event.is_set():
            return None

        try:
            response = self.http.request("GET", url)
            self.good_request_count += 1
            return response.text
        except Exception as err:
            self.bad_request_count += 1
            print(f"Ошибка при запросе {url}: {err}")
            return None

    def parse(self):
        parsed_items: list[ParsedProduct] = []

        for url in self.config.urls:
            html_code = self.fetch_data(url=url)
            if not html_code:
                continue

            parsed_items.append(self._parse_product_card(url=url, html=html_code))

            print(f"Пауза {self.config.pause_between_links} сек.")
            time.sleep(self.config.pause_between_links)

        self.result_storage.save(parsed_items)

        print(f"Готово. Спарсено карточек: {len(parsed_items)}. Хорошие запросы: {self.good_request_count}, плохие: {self.bad_request_count}")

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
        print(f"Название: {title}, Цена: {price}, Описание: {description}")

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


if __name__ == "__main__":
    try:
        config = load_avito_config("config.toml")
    except Exception as err:
        print(f"Ошибка загрузки конфига: {err}")
        raise SystemExit(1)

    parser = AvitoParse(config)
    parser.parse()
