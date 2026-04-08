# DCI Performance Test

## Оглавление
- [Общее описание](#общее-описание)
- [Архитектура](#архитектура)
- [ApiClient](#apiclient)
- [Helpers](#helpers)
- [CSV Logger](#csv-logger)
- [Формат CSV](#формат-csv)
- [Выполняемые тесты](#выполняемые-тесты)
  - [Общие принципы](#общие-принципы)
  - [Servers API](#servers-api)
  - [Rack API](#rack-api)
  - [Warehouse API](#warehouse-api)
- [Fixtures](#fixtures)
- [Что фиксируется в результатах](#что-фиксируется-в-результатах)

---

## Общее описание

Данный проект предназначен для проведения простого performance-тестирования API DCImanager с использованием:

- pytest — запуск тестов  
- httpx — HTTP-клиент  
- кастомный ApiClient — авторизация, retry, timeout  
- CSV-логирования — для последующей загрузки в BI  

---

## Архитектура

```
dci_perf_test/
  ├── clients/
  │     └── api_client.py
  ├── docs/
  │     └── dci_perf_test.md
  ├── helpers/
  │     ├── api_helper.py
  │     └── csv_logger.py
  ├── tests/
  │     ├── test_servers_load_time.py
  │     ├── test_rack_load_time.py
  │     ├── test_warehouse_load_time.py
  │     ├── conftest.py
  │     └── results/
  │         └── api_perf_<run_id>.csv
```

---

## ApiClient

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

---

## Helpers

### run_logged_request()

Центральный метод:

- выполняет HTTP-запрос  
- измеряет время  
- парсит JSON  
- извлекает метрики  
- пишет результат в CSV  
- обрабатывает ошибки  

### extract_response_metrics()

Извлекает:

- status_code  
- response_bytes  
- total_size  
- returned_count  

---

## CSV Logger

Отвечает за:

- генерацию run_id  
- автогенерацию имени файла  
- запись строк  

---

## Формат CSV

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

---

## Выполняемые тесты

### Общие принципы

Все тесты:

- используют ApiClient  
- выполняются через run_logged_request()  
- логируют результаты в CSV  
- используют HTTP метод GET  
- явно задают параметры запроса  
- используют request.node для имени теста  

---

### Servers API

Endpoint:

```
{BASE_PATH}/server
```

Сортировка:

```
orderby = id desc
```

#### test_servers_with_where

Фильтрация серверов по имени:

```
name CP '%Srv-1768461385-450-7%'
name CP '%Srv-1768461385-450%'
```

Проверки:
- HTTP статус = 200  
- list — список  
- size — число  

---

#### test_servers_with_front_limits

Параметры:

```
limit = 5, 10, 25, 50, 100, 250
```

Проверки:
- HTTP статус = 200  
- len(list) <= limit  

---

#### test_servers_with_large_limits

Параметры:

```
limit = 1000, 5000, 10000, 15000
```

Проверки:
- HTTP статус = 200  
- len(list) <= limit  

---

### Rack API

Endpoint:

```
{BASE_PATH}/rack
```

Сортировка:

```
orderby = device_count desc
```

#### test_rack_with_where

```
name CP '%Rack0001%'
name CP '%Rack00011%'
name CP '%Rack000%'
```

Проверки:
- HTTP статус = 200  
- list — список  
- size — число  

---

#### test_rack_with_front_limits

```
limit = 5, 10, 25, 50, 100, 250, 2000
```

Проверки:
- HTTP статус = 200  
- len(list) <= limit  

---

### Warehouse API

Сортировка:

```
orderby = warehouse_status desc
```

#### test_warehouse_with_device_type

Параметры:

```
switch
pdu
ups
chassis
```

Endpoint:

```
{BASE_PATH}/warehouse/<device_type>
```

Проверки:
- HTTP статус = 200  
- list — список  

---

#### test_warehouse_spare_part_with_limit

Параметры:

```
limit = 1, 5, 25, 100
```

Endpoint:

```
{BASE_PATH}/warehouse/spare_part
```

Проверки:
- HTTP статус = 200  
- list — список  

---

## Fixtures

### api
- создаёт ApiClient на сессию  
- закрывает после тестов  

### run_id
- генерирует уникальный идентификатор прогона  

### results_csv_path
- формирует путь к CSV  
- выводит путь и run_id  

### csv_result_logger
- записывает результаты тестов в CSV  

---

## Что фиксируется в результатах

Каждый прогон записывает:

- длительность выполнения  
- размер ответа  
- количество элементов  
- общее количество (size)  
- параметры запроса  
- статус выполнения  
- ошибки (если есть)  
