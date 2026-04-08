# Общее описание

Данный проект предназначен для проведения простого performance-тестирования API DCImanager с использованием:
- pytest — запуск тестов
- httpx — HTTP-клиент
- кастомный ApiClient — авторизация, retry, timeout
CSV-логирования — для последующей загрузки в BI

# Архитектура
dci_perf_test/
  ├── clients/
  │     └── api_client.py
  ├── docs/
  │     └── dci_perf_test.md
  ├── helpers/
  │     ├── api_helper.py
  │     └── csv_logger.py
  ├── tests/
  │     ├──test_servers_load_time.py
        ├──test_rack_load_time.py
        ├──test_warehouse_load_time.py
        ├── conftest.py
        └──results/
            └──api_perf_<run_id>.csv
  
# ApiClient

Отвечает за:
- авторизацию (login/password → session + xsrf)
- хранение cookies
- retry при 401
- настройку timeout
- отключение SSL verify (self-signed)

Особенности:
- используется httpx.Client
- timeout настраивается через httpx.Timeout
- retry логика встроена в _request_with_reauth

# Helpers
run_logged_request()

Центральный метод:
- выполняет HTTP-запрос
- измеряет время
- парсит JSON
- извлекает метрики
- пишет результат в CSV
- обрабатывает ошибки

extract_response_metrics()

Извлекает:
- status_code
- response_bytes
- total_size
- returned_count

# CSV Logger

Отвечает за:
- генерацию run_id
- автогенерацию имени файла
- запись строк

# Формат CSV

Одна строка = один тестовый прогон 

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