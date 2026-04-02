import pytest
from helpers.api_helper import (
    BASE_PATH,
    build_params,
    perform_request,
    log_response,
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
def test_warehouse_with_device_type(api, device_type):
    params = build_params(orderby='warehouse_status desc')

    response, data, duration = perform_request(api, f'{BASE_PATH}/warehouse/{device_type}', params)

    assert response.status_code == 200
    assert isinstance(data["list"], list)

    log_response(response, data, duration, label="WHERE")


@pytest.mark.parametrize("limit", [1, 5, 25, 100])
def test_warehouse_spare_part_with_limit(api, limit):
    params = build_params(orderby='warehouse_status desc', limit=limit)

    response, data, duration = perform_request(api, f'{BASE_PATH}/warehouse/spare_part', params)

    assert response.status_code == 200
    assert isinstance(data["list"], list)
    # assert isinstance(data["size"], int)

    log_response(response, data, duration, label=f'LIMIT = {limit}')
