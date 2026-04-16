import pytest
from helpers.api_helper import (
    BASE_PATH,
    build_params,
    log_response,
    run_logged_request,
)


@pytest.mark.parametrize(
    "device_type",
    [
        "switch",
        "pdu",
        "ups",
        "chassis",
    ],
)
def test_warehouse_with_device_type(api, device_type, request, csv_result_logger,
                                    db_result_logger, debug_response_log_enabled):
    params = build_params(orderby='warehouse_status desc')

    response, data, duration = run_logged_request(
        api=api,
        path=f'{BASE_PATH}/warehouse/{device_type}',
        params=params,
        csv_logger=csv_result_logger,
        db_logger=db_result_logger,
        request_node=request.node,
    )

    assert response.status_code == 200
    assert isinstance(data["list"], list)

    log_response(response, data, duration, enabled=debug_response_log_enabled, label="WHERE")


@pytest.mark.parametrize("limit", [1, 5, 25, 100])
def test_warehouse_spare_part_with_limit(api, limit, request, csv_result_logger,
                                         db_result_logger, debug_response_log_enabled):
    params = build_params(orderby='warehouse_status desc', limit=limit)

    response, data, duration = run_logged_request(
        api=api,
        path=f'{BASE_PATH}/warehouse/spare_part',
        params=params,
        csv_logger=csv_result_logger,
        db_logger=db_result_logger,
        request_node=request.node,
    )

    assert response.status_code == 200
    assert isinstance(data["list"], list)

    log_response(response, data, duration, enabled=debug_response_log_enabled, label=f'LIMIT = {limit}')
