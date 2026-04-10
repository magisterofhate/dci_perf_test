from datetime import datetime, UTC
from typing import Any


INSERT_RESULT_SQL = """
INSERT INTO api_perf_results (
    timestamp,
    run_id,
    test_name,
    test_suite,
    endpoint,
    method,
    status_code,
    success,
    duration_sec,
    response_bytes,
    total_size,
    returned_count,
    orderby,
    where_clause,
    limit_value,
    error_type,
    error_message
) VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
);
"""


def write_result_into_db(
    connection,
    *,
    timestamp=datetime.now(UTC).isoformat(),
    run_id: str,
    test_name: str,
    test_suite: str,
    endpoint: str,
    method: str,
    status_code: int | None,
    success: bool,
    duration_sec: float,
    response_bytes: int | None,
    total_size: int | None,
    returned_count: int | None,
    orderby: str | None,
    where_clause: str | None,
    limit: int | None,
    error_type: str | None,
    error_message: str | None,
) -> None:
    values = (
        timestamp,
        run_id,
        test_name,
        test_suite,
        endpoint,
        method,
        status_code,
        success,
        duration_sec,
        response_bytes,
        total_size,
        returned_count,
        orderby,
        where_clause,
        limit,
        error_type,
        error_message,
    )

    with connection.cursor() as cursor:
        cursor.execute(INSERT_RESULT_SQL, values)

    connection.commit()
