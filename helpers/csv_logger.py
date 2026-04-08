import csv
import uuid
from datetime import datetime, UTC
from pathlib import Path


CSV_HEADERS = [
    "timestamp",
    "run_id",
    "test_name",
    "test_suite",
    "endpoint",
    "method",
    "status_code",
    "success",
    "duration_sec",
    "response_bytes",
    "total_size",
    "returned_count",
    "orderby",
    "where_clause",
    "limit",
    "error_type",
    "error_message",
]


def generate_run_id() -> str:
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    short_uuid = uuid.uuid4().hex[:8]
    return f"{timestamp}_{short_uuid}"


def build_results_file_path(results_dir: str | Path, run_id: str) -> Path:
    results_dir = Path(results_dir)
    results_dir.mkdir(parents=True, exist_ok=True)
    return results_dir / f"api_perf_{run_id}.csv"


def ensure_csv_exists(file_path: str | Path) -> Path:
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if not path.exists():
        with path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=CSV_HEADERS)
            writer.writeheader()

    return path


def write_csv_result(
    file_path: str | Path,
    *,
    run_id: str,
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
) -> None:
    path = ensure_csv_exists(file_path)

    row = {
        "timestamp": datetime.now(UTC).isoformat(),
        "run_id": run_id,
        "test_name": test_name,
        "test_suite": test_suite,
        "endpoint": endpoint,
        "method": method,
        "status_code": status_code,
        "success": success,
        "duration_sec": round(duration_sec, 6),
        "response_bytes": response_bytes,
        "total_size": total_size,
        "returned_count": returned_count,
        "orderby": orderby,
        "where_clause": where_clause,
        "limit": limit,
        "error_type": error_type,
        "error_message": error_message,
    }

    with path.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_HEADERS)
        writer.writerow(row)
