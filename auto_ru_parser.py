import re
import json

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
            photos=AutoRuParse._extract_photos(soup),
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

    @staticmethod
    def _extract_photos(soup: BeautifulSoup) -> list[str]:
        json_ld_photos = AutoRuParse._extract_photos_from_json_ld(soup)
        if json_ld_photos:
            return AutoRuParse._unique(json_ld_photos)

        return AutoRuParse._unique(AutoRuParse._extract_photos_from_meta(soup))

    @staticmethod
    def _extract_photos_from_meta(soup: BeautifulSoup) -> list[str]:
        photos: list[str] = []
        for node in soup.find_all("meta", attrs={"property": "og:image"}):
            value = node.get("content", "").strip()
            if value:
                photos.append(value)
        return photos

    @staticmethod
    def _extract_photos_from_json_ld(soup: BeautifulSoup) -> list[str]:
        scripts = soup.find_all("script", attrs={"type": "application/ld+json"})
        for script in scripts:
            raw = script.string or script.get_text(strip=True)
            if not raw:
                continue

            try:
                payload = json.loads(raw)
            except json.JSONDecodeError:
                continue

            candidate = AutoRuParse._find_product(payload)
            if not candidate:
                continue

            images = candidate.get("image") or []
            if isinstance(images, str):
                return [images]
            if isinstance(images, list):
                return [item for item in images if isinstance(item, str) and item.strip()]

        return []

    @staticmethod
    def _find_product(payload):
        if isinstance(payload, dict):
            if payload.get("@type") == "Product":
                return payload

            graph = payload.get("@graph")
            if isinstance(graph, list):
                for item in graph:
                    found = AutoRuParse._find_product(item)
                    if found:
                        return found

            for value in payload.values():
                found = AutoRuParse._find_product(value)
                if found:
                    return found

        if isinstance(payload, list):
            for item in payload:
                found = AutoRuParse._find_product(item)
                if found:
                    return found

        return None

    @staticmethod
    def _unique(items: list[str]) -> list[str]:
        seen: set[str] = set()
        result: list[str] = []
        for item in items:
            value = item.strip()
            if not value or value in seen:
                continue
            seen.add(value)
            result.append(value)
        return result