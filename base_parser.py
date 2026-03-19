"""Пример головного парсера, который передаёт ссылку в AvitoParse."""

from avito_parser import AvitoParse
from avito_abuse.load_config import load_avito_config


class BaseParser:
    def __init__(self, config_path: str = "avito_abuse/config.toml"):
        self.config = load_avito_config(config_path)
        self.avito_parser = AvitoParse(self.config)

    def parse_avito_card(self, url: str):
        return self.avito_parser.parse_url(url)


if __name__ == "__main__":
    parser = BaseParser()
    product = parser.parse_avito_card("https://www.avito.ru/...")
    print(product)
