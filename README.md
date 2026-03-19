## Avito Card Parser (минимальная сборка)

Парсер карточки Avito, который принимает **одну ссылку извне** (из головного парсера), загружает страницу и возвращает:
- `title`
- `price`
- `description`

## Использование

```python
from load_config import load_avito_config
from parser_cls import AvitoParse

config = load_avito_config("config.toml")
parser = AvitoParse(config)

product = parser.parse_url("https://www.avito.ru/...")
print(product.title, product.price, product.description)
```

## Настройка `config.toml`

- `proxy_string` — мобильный прокси (`login:password@ip:port` или `ip:port`).
- `proxy_change_url` — URL смены IP мобильного прокси.
- `max_count_of_retry` — число повторов HTTP-запроса.

Если `proxy_string` или `proxy_change_url` пустые — запуск завершится ошибкой.
