## Avito Card Parser (минимальная сборка)

Максимально упрощённый репозиторий для встраивания в любой проект.

### Что делает
1. Принимает ссылку(и) на карточку товара Avito (`urls` в `config.toml`).
2. Загружает страницу через `curl_cffi` с `impersonate="chrome"`.
3. Работает только через **мобильный прокси** и при блокировках (401/403/429) делает ротацию IP через `proxy_change_url`.
4. Из карточки извлекает только:
   - `Название`
   - `Цена`
   - `Описание`
5. Сохраняет результат в `result/avito.xlsx`.

## Быстрый старт

```bash
pip install -r requirements.txt
python parser_cls.py
```

## Настройка `config.toml`

- `urls` — ссылки на карточки товаров Avito.
- `proxy_string` — мобильный прокси (`login:password@ip:port` или `ip:port`).
- `proxy_change_url` — URL смены IP мобильного прокси.  
- `max_count_of_retry` — кол-во повторов запроса.
- `pause_between_links` — пауза между карточками.

Если `proxy_string` или `proxy_change_url` пустые — запуск завершится ошибкой.
