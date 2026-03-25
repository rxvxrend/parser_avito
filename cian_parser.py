import re

from bs4 import BeautifulSoup

from avito_abuse.dto import ParsedProduct


class CianParse:
    @staticmethod
    def parse_html(url: str, html: str) -> ParsedProduct:
        soup = BeautifulSoup(html, "html.parser")

        title = (
            CianParse._text(soup.select_one("h1"))
            or CianParse._meta_content(soup, "property", "og:title")
            or ""
        )

        price = (
            CianParse._text(soup.select_one('[data-testid="price-amount"]'))
            or CianParse._text(soup.select_one('[data-mark="MainPrice"]'))
            or CianParse._text(soup.select_one('[itemprop="price"]'))
            or CianParse._extract_price_by_regex(html)
            or ""
        )

        description = (
            CianParse._text(soup.select_one('[data-name="Description"]'))
            or CianParse._meta_content(soup, "name", "description")
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
    def _meta_content(soup: BeautifulSoup, attr: str, value: str) -> str:
        tag = soup.find("meta", attrs={attr: value})
        if not tag:
            return ""
        return tag.get("content", "")

    @staticmethod
    def _extract_price_by_regex(html: str) -> str:
        match = re.search(r"\d[\d\s]{3,}\s?₽", html)
        if not match:
            return ""
        return match.group(0)