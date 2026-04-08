import pytest
from clients.api_client import ApiClient
from pathlib import Path

from helpers.csv_logger import (
    build_results_file_path,
    generate_run_id,
    write_csv_result,
)

RESULTS_DIR = Path("results")


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
def results_csv_path(run_id):
    path = build_results_file_path(RESULTS_DIR, run_id)
    print(f"\nCSV results file: {path}")
    print(f"Run ID: {run_id}")
    return path


@pytest.fixture
def csv_result_logger(results_csv_path, run_id):
    def _log(
        *,
        test_name: str,
        test_suite: str,
        endpoint: str,
        method: str,
        status_code: int | None,
        success: bool,
        duration_sec: float,
        response_bytes: int | None = None,
        total_size: int | None = None,
        returned_count: int | None = None,
        orderby: str | None = None,
        where_clause: str | None = None,
        limit: int | None = None,
        error_type: str | None = None,
        error_message: str | None = None,
    ):
        write_csv_result(
            results_csv_path,
            run_id=run_id,
            test_name=test_name,
            test_suite=test_suite,
            endpoint=endpoint,
            method=method,
            status_code=status_code,
            success=success,
            duration_sec=duration_sec,
            response_bytes=response_bytes,
            total_size=total_size,
            returned_count=returned_count,
            orderby=orderby,
            where_clause=where_clause,
            limit=limit,
            error_type=error_type,
            error_message=error_message,
        )

    return _log
