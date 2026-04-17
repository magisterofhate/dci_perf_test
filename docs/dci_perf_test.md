# DCI Performance Test

## Оглавление
- [Общее описание](#общее-описание)
- [Архитектура](#архитектура)
- [Конфигурация (.env)](#конфигурация-env)
- [ApiClient](#apiclient)
- [DB Client](#db-client)
- [Helpers](#helpers)
- [CSV Logger](#csv-logger)
- [DB Logger](#db-logger)
- [Формат CSV](#формат-csv)
- [Fixtures](#fixtures)

---

## Общее описание

Проект предназначен для performance-тестирования API DCImanager.

Основные возможности:

- запуск тестов через pytest
- выполнение HTTP-запросов через httpx
- централизованный метод `run_logged_request()`
- логирование результатов в:
  - CSV (обязательно)
  - MySQL (опционально)
- управление поведением через `.env`

---

## Архитектура

```
dci_perf_test/
  ├── clients/
  │     ├── api_client.py
  │     └── mysql_client.py
  ├── config/
  │     └── settings.py
  ├── helpers/
  │     ├── api_helper.py
  │     ├── csv_logger.py
  │     └── mysql_logger.py
  ├── tests/
  │     ├── test_*.py
  │     ├── conftest.py
  │     └── results/
  │         └── api_perf_<run_id>.csv
  └── .env
```

---

## Конфигурация (.env)

Все параметры проекта задаются через `.env`.

### Пример:

```env
API_BASE_URL=https://1.1.1.222/
API_LOGIN=test
API_PASSWORD=secret
API_VERIFY_SSL=false
API_TIMEOUT=60

DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=perf_user
DB_PASSWORD=strong_password
DB_NAME=perf_tests

DEBUG_RESPONSE_LOG=false
ENABLE_DB_LOGGING=true
```

### Описание переменных

#### API

- `API_BASE_URL` — базовый URL API
- `API_LOGIN` — логин
- `API_PASSWORD` — пароль
- `API_VERIFY_SSL` — проверка SSL (true/false)
- `API_TIMEOUT` — таймаут запроса

#### БД

- `DB_HOST` — хост базы данных
- `DB_PORT` — порт
- `DB_USER` — пользователь
- `DB_PASSWORD` — пароль
- `DB_NAME` — имя базы

#### Debug / Logging

- `DEBUG_RESPONSE_LOG` — вывод ответов в консоль
- `ENABLE_DB_LOGGING` — включение записи в БД

---

## ApiClient

Отвечает за:

- авторизацию
- хранение cookies
- retry при 401
- timeout

---

## DB Client

Отвечает за:

- подключение к MySQL
- управление соединением

---

## Helpers

### run_logged_request()

Центральный метод:

- выполняет HTTP-запрос
- собирает метрики
- пишет результат в CSV
- опционально пишет результат в БД

Параметр:

```python
db_result_logger=None
```

---

## CSV Logger

Отвечает за:

- создание файла
- запись результатов

---

## DB Logger

Отдельный слой для записи результатов в MySQL.

Особенности:

- append-only
- не влияет на выполнение тестов
- ошибки логирования не валят тест

---

## Формат CSV

Поля:

- timestamp
- run_id
- test_name
- test_suite
- endpoint
- method
- status_code
- success
- duration_sec
- response_bytes
- total_size
- returned_count
- orderby
- where_clause
- limit
- error_type
- error_message

---

## Fixtures

Основные:

- `settings` — конфиг из `.env`
- `api` — API клиент
- `db` — подключение к БД
- `db_result_logger` — логер БД
- `csv_result_logger` — логер для CSV
- `debug_response_log_enabled` — debug-флаг, включающий отображение результатов теста в std-out

---

## Общая идея

- CSV — основной источник данных
- БД — дополнительное хранилище
- `.env` — единая точка управления
- логика разделена по слоям