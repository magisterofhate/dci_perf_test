import time
from typing import Tuple, Dict, Any


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