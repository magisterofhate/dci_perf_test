import pytest
from helpers.api_helper import (
    BASE_PATH,
    build_params,
    log_response,
    run_logged_request,
)


@pytest.mark.parametrize(
    "where_clause",
    [
        "name CP '%Rack0001%'",
        "name CP '%Rack00011%'",
        "name CP '%Rack000%'",
    ],
)
def test_rack_with_where(api, where_clause, request, csv_result_logger,
                         db_result_logger, debug_response_log_enabled):
    params = build_params(where=where_clause, orderby='device_count desc')

    response, data, duration = run_logged_request(
        api=api,
        path=f'{BASE_PATH}/rack',
        params=params,
        csv_logger=csv_result_logger,
        db_logger=db_result_logger,
        request_node=request.node,
    )

    assert response.status_code == 200
    assert isinstance(data["list"], list)
    assert isinstance(data["size"], int)

    log_response(response, data, duration, enabled=debug_response_log_enabled, label="WHERE")


@pytest.mark.parametrize("limit", [5, 10, 25, 50, 100, 250, 2000])
def test_rack_with_front_limits(api, limit, request, csv_result_logger,
                                db_result_logger, debug_response_log_enabled):
    params = build_params(limit=limit, orderby='device_count desc')

    response, data, duration = run_logged_request(
        api=api,
        path=f'{BASE_PATH}/rack',
        params=params,
        csv_logger=csv_result_logger,
        db_logger=db_result_logger,
        request_node=request.node,
    )

    assert response.status_code == 200
    assert len(data["list"]) <= limit

    log_response(response, data, duration, enabled=debug_response_log_enabled, label=f"LIMIT={limit}")
