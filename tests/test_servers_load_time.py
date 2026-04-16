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
        "name CP '%Srv-1768461385-450-7%'",
        "name CP '%Srv-1768461385-450%'",
    ],
)
def test_servers_with_where(api, where_clause, request, csv_result_logger,
                            db_result_logger, debug_response_log_enabled):
    params = build_params(where=where_clause, orderby='id desc')

    response, data, duration = run_logged_request(
        api=api,
        path=f'{BASE_PATH}/server',
        params=params,
        csv_logger=csv_result_logger,
        db_logger=db_result_logger,
        request_node=request.node,
    )

    assert response.status_code == 200
    assert isinstance(data["list"], list)
    assert isinstance(data["size"], int)

    log_response(response, data, duration, enabled=debug_response_log_enabled, label="WHERE")


@pytest.mark.parametrize("limit", [5, 10, 25, 50, 100, 250])
def test_servers_with_front_limits(api, limit, request, csv_result_logger,
                                   db_result_logger, debug_response_log_enabled):
    params = build_params(limit=limit, orderby='id desc')

    response, data, duration = run_logged_request(
        api=api,
        path=f'{BASE_PATH}/server',
        params=params,
        csv_logger=csv_result_logger,
        db_logger=db_result_logger,
        request_node=request.node,
    )

    assert response.status_code == 200
    assert len(data["list"]) <= limit

    log_response(response, data, duration, enabled=debug_response_log_enabled, label=f"LIMIT={limit}")


@pytest.mark.parametrize("limit", [1000, 5000, 10000, 15000])
def test_servers_with_large_limits(api, limit, request, csv_result_logger,
                                   db_result_logger, debug_response_log_enabled):
    params = build_params(limit=limit, orderby='id desc')

    response, data, duration = run_logged_request(
        api=api,
        path=f'{BASE_PATH}/server',
        params=params,
        csv_logger=csv_result_logger,
        db_logger=db_result_logger,
        request_node=request.node,
    )

    assert response.status_code == 200
    assert len(data["list"]) <= limit

    log_response(response, data, duration, enabled=debug_response_log_enabled, label=f"LARGE LIMIT={limit}")
