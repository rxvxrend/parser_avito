## Avito/Auto.ru Card Parser (минимальная сборка)

Парсер карточки Avito или Auto.ru, который принимает **одну ссылку извне** (из головного парсера), загружает страницу и возвращает:
- `title`
- `price`
- `description`
- `photos` (для Avito; список URL изображений)

## Использование

```python
from base_parser import BaseParser

parser = BaseParser("avito_abuse/config.toml")

product = parser.parse_card("https://auto.ru/cars/used/sale/...")
print(product.title, product.price, product.description, product.photos)
```

## Настройка `config.toml`

- `proxy_string` — мобильный прокси (`login:password@ip:port`).
- `proxy_change_url` — URL смены IP мобильного прокси.
- `max_count_of_retry` — число повторов HTTP-запроса.

Если `proxy_string` или `proxy_change_url` пустые — запуск завершится ошибкой.