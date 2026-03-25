import re
import json

from bs4 import BeautifulSoup

from utils.dto import ParsedProduct


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
            photos=AvitoParse._extract_photos(soup),
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

    @staticmethod
    def _extract_photos(soup: BeautifulSoup) -> list[str]:
        json_ld_photos = AvitoParse._extract_photos_from_json_ld(soup)
        if json_ld_photos:
            return AvitoParse._unique(json_ld_photos)

        return AvitoParse._unique(AvitoParse._extract_photos_from_meta(soup))

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

            candidate = AvitoParse._find_product(payload)
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
                    found = AvitoParse._find_product(item)
                    if found:
                        return found

            for value in payload.values():
                found = AvitoParse._find_product(value)
                if found:
                    return found

        if isinstance(payload, list):
            for item in payload:
                found = AvitoParse._find_product(item)
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