import uuid
from datetime import datetime, UTC
import pytest
from clients.api_client import ApiClient
from pathlib import Path
from clients.db_client import MySQLClient
from config.settings import Settings, load_settings

from helpers.csv_logger import (
    build_results_file_path,
    write_csv_result,
)
from helpers.db_logger import write_result_into_db

RESULTS_DIR = Path("results")


@pytest.fixture(scope="session")
def settings() -> Settings:
    return load_settings()


@pytest.fixture(scope="session")
def debug_response_log_enabled(settings: Settings) -> bool:
    return settings.debug.response_log_enabled


@pytest.fixture(scope="session")
def run_id():
    return generate_run_id()


@pytest.fixture(scope="session")
def api(settings : Settings):
    api = ApiClient(
        base_url=settings.api.base_url,
        login=settings.api.login,
        password=settings.api.password,
        verify_ssl=settings.api.verify_ssl,
        timeout=settings.api.timeout,
    )
    yield api
    api.close()


@pytest.fixture(scope="session")
def db(settings : Settings):
    client = MySQLClient(
        host=settings.db.host,
        port=settings.db.port,
        user=settings.db.user,
        password=settings.db.password,
        database=settings.db.database,
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
def db_result_logger(db, run_id, settings: Settings):
    if not settings.debug.db_logging_enabled:
        return None

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
