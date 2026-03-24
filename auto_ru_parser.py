import re

from bs4 import BeautifulSoup

from avito_abuse.dto import ParsedProduct


class AutoRuParse:
    @staticmethod
    def parse_html(url: str, html: str) -> ParsedProduct:
        soup = BeautifulSoup(html, "html.parser")

        title = (
            AutoRuParse._text(soup.select_one("h1"))
            or AutoRuParse._text(soup.select_one('[data-testid="title"]'))
            or AutoRuParse._meta_content(soup, "property", "og:title")
            or ""
        )

        price = (
            AutoRuParse._text(soup.select_one('[data-testid="price"]'))
            or AutoRuParse._text(soup.select_one('[data-testid="price-block"]'))
            or AutoRuParse._text(soup.select_one('[itemprop="price"]'))
            or AutoRuParse._extract_price_by_regex(html)
            or ""
        )

        description = (
            AutoRuParse._text(soup.select_one('[data-testid="description"]'))
            or AutoRuParse._text(soup.select_one('[data-testid="text"]'))
            or AutoRuParse._meta_content(soup, "name", "description")
            or ""
        )

        return ParsedProduct(
            url=url,
            title=title.strip(),
            price=price.strip(),
            description=description.strip(),
        )

    @staticmethod
    def _text(tag) -> str:
        if not tag:
            return ""
        return tag.get_text(" ", strip=True)

    @staticmethod
    def _meta_content(soup: BeautifulSoup, attr_name: str, attr_value: str) -> str:
        tag = soup.find("meta", attrs={attr_name: attr_value})
        if not tag:
            return ""
        return tag.get("content", "")

    @staticmethod
    def _extract_price_by_regex(html: str) -> str:
        match = re.search(r"\d[\d\s]{3,}\s?₽", html)
        if not match:
            return ""
        return match.group(0)