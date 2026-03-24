import re

from bs4 import BeautifulSoup

from avito_abuse.dto import ParsedProduct


class AvitoParse:
    @staticmethod
    def parse_html(url: str, html: str) -> ParsedProduct:
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
    def _meta_content(soup: BeautifulSoup, attr: str, value: str) -> str:
        tag = soup.find("meta", attrs={attr: value})
        if tag:
            return tag.get("content", "")
        return ""

    @staticmethod
    def _text(tag) -> str:
        if not tag:
            return ""
        return tag.get_text(" ", strip=True)

    @staticmethod
    def _extract_price_by_regex(html: str) -> str:
        match = re.search(r'"price"\s*:\s*\{[^}]*?"value"\s*:\s*(\d+)', html)
        if match:
            return match.group(1)
        return ""