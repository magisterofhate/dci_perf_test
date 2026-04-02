import pytest
from helpers.api_helper import (
    BASE_PATH,
    build_params,
    perform_request,
    log_response,
)


@pytest.mark.parametrize(
    "where_clause",
    [
        "name CP '%Rack0001%'",
        "name CP '%Rack00011%'",
        "name CP '%Rack000%'",
    ],
)
def test_rack_with_where(api, where_clause):
    params = build_params(where=where_clause, orderby='device_count desc')

    response, data, duration = perform_request(api, f'{BASE_PATH}/rack', params)

    assert response.status_code == 200
    assert isinstance(data["list"], list)
    assert isinstance(data["size"], int)

    log_response(response, data, duration, label="WHERE")


@pytest.mark.parametrize("limit", [5, 10, 25, 50, 100, 250, 2000])
def test_rack_with_front_limits(api, limit):
    params = build_params(limit=limit, orderby='device_count desc')

    response, data, duration = perform_request(api, f'{BASE_PATH}/rack', params)

    assert response.status_code == 200
    assert len(data["list"]) <= limit

    log_response(response, data, duration, label=f"LIMIT={limit}")
