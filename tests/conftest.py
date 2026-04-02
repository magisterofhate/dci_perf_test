import pytest
from clients.api_client import ApiClient


@pytest.fixture(scope="session")
def api():
    api = ApiClient(
        base_url="https://172.31.48.29/",
        login="test@test.com",
        password="Ru77Kq67",
    )
    yield api
    api.close()

