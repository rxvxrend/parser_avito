from ...dto import AvitoConfig
from .proxy import MobileProxy, Proxy


def build_proxy(config: AvitoConfig) -> Proxy:
    """В проекте поддерживаются только мобильные прокси."""
    if not config.proxy_string or not config.proxy_change_url:
        raise ValueError(
            "Нужны оба поля для мобильного прокси: proxy_string и proxy_change_url"
        )

    return MobileProxy(config.proxy_string, config.proxy_change_url)
