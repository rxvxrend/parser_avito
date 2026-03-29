## Avito/Auto.ru/Cian Card Parser (минимальная сборка)

Парсер карточки Avito, Auto.ru или Cian, который принимает **одну ссылку извне** (из головного парсера), загружает страницу и возвращает:
- `title`
- `price`
- `description`
- `photos` (для Avito; список URL изображений)

## Использование

```python
from base_parser import BaseParser

parser = BaseParser("avito_abuse/config.toml")

product = parser.parse_card("https://cian.ru/sale/flat/...")
print(product.title, product.price, product.description, product.photos)
```

## Настройка `config.toml`

- `proxy_string` — мобильный прокси (`login:password@ip:port`).
- `proxy_change_url` — основной URL смены IP мобильного прокси.
- `proxy_change_urls` — опциональный список URL (основной + резервные), которые будут пробоваться по очереди при смене IP.
- `max_count_of_retry` — число повторов HTTP-запроса.

Если `proxy_string` или `proxy_change_url` пустые — запуск завершится ошибкой.