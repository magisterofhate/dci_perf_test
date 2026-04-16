import uuid
from datetime import datetime, UTC
import os
from dotenv import load_dotenv

import pytest
from clients.api_client import ApiClient
from pathlib import Path
from clients.db_client import MySQLClient

from helpers.csv_logger import (
    build_results_file_path,
    write_csv_result,
)
from helpers.db_logger import write_result_into_db

RESULTS_DIR = Path("results")


load_dotenv()

def _get_bool_env(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@pytest.fixture(scope="session")
def debug_response_log_enabled() -> bool:
    return _get_bool_env("DEBUG_RESPONSE_LOG")


@pytest.fixture(scope="session")
def run_id():
    return generate_run_id()


@pytest.fixture(scope="session")
def api():
    api = ApiClient(
        base_url="https://172.31.48.29/",
        login="test@test.com",
        password="Ru77Kq67",
    )
    yield api
    api.close()


@pytest.fixture(scope="session")
def db():
    client = MySQLClient(
        host="172.31.36.82",
        port=3306,
        user="perf_user",
        password="strong_password",
        database="perf_tests",
    )
    connection = client.connect()
    yield connection
    connection.close()


@pytest.fixture(scope="session")
def results_csv_path(run_id):
    path = build_results_file_path(RESULTS_DIR, run_id)
    print(f"\nCSV results file: {path}")
    print(f"Run ID: {run_id}")
    return path


@pytest.fixture
def csv_result_logger(results_csv_path, run_id):
    def _log(**result_payload):
        write_csv_result(
            results_csv_path,
            run_id=run_id,
            **result_payload,
        )

    return _log


@pytest.fixture
def db_result_logger(db, run_id):
    def _log(**result_payload):
        write_result_into_db(
            db,
            run_id=run_id,
            **result_payload,
        )

    return _log


def generate_run_id() -> str:
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    short_uuid = uuid.uuid4().hex[:8]
    return f"{timestamp}_{short_uuid}"
