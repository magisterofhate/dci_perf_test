import time
from typing import Tuple, Dict, Any
import httpx


BASE_PATH = "/dci/v3"


def build_params(**extra) -> dict:
    """
    Базовые параметры для запросов к servers API.
    """
    params = {}
    params.update(extra)
    return params


def perform_request(api, path: str, params: dict) -> Tuple[Any, Dict, float]:
    """
    Универсальный helper:
    - выполняет запрос
    - меряет время
    - возвращает (response, json, duration)
    """
    start = time.perf_counter()

    response = api.get(path, params=params)

    duration = time.perf_counter() - start

    data = response.json()

    return response, data, duration


def extract_response_metrics(response, data: dict) -> dict:
    return {
        "status_code": response.status_code,
        "response_bytes": len(response.content),
        "total_size": data.get("size"),
        "returned_count": len(data.get("list", [])),
    }


def log_response(response, data, duration, label: str = ""):
    """
    Логирование в std_out
    """
    print(
        f"\n[{label}] "
        f"status={response.status_code} | "
        f"size={data.get('size')} | "
        f"returned={len(data.get('list', []))} | "
        f"bytes={len(response.content)} | "
        f"time={duration:.3f}s"
    )


def generate_result_payload(request_node, path, method, metrics, success, duration, params,
                            error_type=None, error_message=None):
    return {
        "test_name": request_node.name,
        "test_suite": request_node.fspath.basename,
        "endpoint": path,
        "method": method,
        "status_code": metrics["status_code"],
        "success": success,
        "duration_sec": duration,
        "response_bytes": metrics["response_bytes"],
        "total_size": metrics["total_size"],
        "returned_count": metrics["returned_count"],
        "orderby": params.get("orderby"),
        "where_clause": params.get("where"),
        "limit": params.get("limit"),
        "error_type": error_type,
        "error_message": error_message,
    }


def run_logged_request(
    *,
    api,
    path: str,
    params: dict,
    csv_logger,
    request_node,
    method: str = "GET",
    timeout=None,
    db_logger=None,
):
    """
        Метод по умолчанию логирует результаты в CSV файл. Если указан db_logger, то и в БД
    """
    start = time.perf_counter()

    try:
        if method != "GET":
            raise ValueError(f"Unsupported method for now: {method}")

        response = api.get(path, params=params, timeout=timeout)
        duration = time.perf_counter() - start
        data = response.json()

        metrics = extract_response_metrics(response, data)
        success = True

        result_payload = generate_result_payload(request_node, path, method, metrics, success, duration, params)

        csv_logger(**result_payload)

        if db_logger is not None:
            db_logger(**result_payload)

        return response, data, duration

    except Exception(httpx.HTTPStatusError) as exc:
        duration = time.perf_counter() - start

        metrics = extract_response_metrics(exc.response, data={})
        success = False

        result_payload = generate_result_payload(request_node, path, method, metrics, success, duration, params,
                                                 error_type=type(exc).__name__, error_message=str(exc))

        csv_logger(**result_payload)

        if db_logger is not None:
            db_logger(**result_payload)

        raise
