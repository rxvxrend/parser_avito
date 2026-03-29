from ...dto import ParserConfig
from .proxy import MobileProxy, Proxy


def build_proxy(config: ParserConfig) -> Proxy:
    """В проекте поддерживаются только мобильные прокси."""
    if not config.proxy_string or not config.proxy_change_url:
        raise ValueError(
            "Нужны оба поля для мобильного прокси: proxy_string и proxy_change_url"
        )

    change_urls = list(config.proxy_change_urls)
    if not change_urls:
        change_urls = [config.proxy_change_url]

    return MobileProxy(config.proxy_string, change_urls)