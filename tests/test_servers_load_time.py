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
        "name CP '%Srv-1768461385-450-7%'",
        "name CP '%Srv-1768461385-450%'",
    ],
    # ids=[
    #     "where_partial_name",
    #     "where_exact_like_name",
    # ],
)
def test_servers_with_where(api, where_clause):
    params = build_params(where=where_clause, orderby='id desc')

    response, data, duration = perform_request(api, f'{BASE_PATH}/server', params)

    assert response.status_code == 200
    assert isinstance(data["list"], list)
    assert isinstance(data["size"], int)

    log_response(response, data, duration, label="WHERE")

@pytest.mark.parametrize("limit", [5, 10, 25, 50, 100, 250])
def test_servers_with_front_limits(api, limit):
    params = build_params(limit=limit, orderby='id desc')

    response, data, duration = perform_request(api, f'{BASE_PATH}/server', params)

    assert response.status_code == 200
    assert len(data["list"]) <= limit

    log_response(response, data, duration, label=f"LIMIT={limit}")

@pytest.mark.parametrize("limit", [1000, 5000, 10000])
def test_servers_with_large_limits(api, limit):
    params = build_params(limit=limit, orderby='id desc')

    response, data, duration = perform_request(api, f'{BASE_PATH}/server', params)

    assert response.status_code == 200
    assert len(data["list"]) <= limit

    log_response(response, data, duration, label=f"LARGE LIMIT={limit}")