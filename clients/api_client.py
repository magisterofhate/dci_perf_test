import httpx


class ApiClient:
    def __init__(
        self,
        base_url: str,
        login: str,
        password: str,
        verify_ssl: bool,
        timeout,
        auth_path: str = "/auth/v4/public/token",
    ):
        self.base_url = base_url.rstrip("/")
        self.login = login
        self.password = password
        self.auth_path = auth_path
        self.token: str | None = None

        client_timeout = httpx.Timeout(
            connect=10.0,
            read=timeout,
            write=30.0,
            pool=30.0,
        )

        self.client = httpx.Client(
            base_url=self.base_url,
            timeout=client_timeout,
            verify=verify_ssl,
        )

        self._authenticate()

    def _authenticate(self) -> None:
        response = self.client.post(
            self.auth_path,
            json={
                "email": self.login,
                "password": self.password,
            },
        )
        response.raise_for_status()

        data = response.json()
        token = data.get("access_token") or data.get("token")

        if not token:
            raise ValueError("Bearer token not found in auth response")

        self.token = token
        self.client.headers.update({
            "X-XSRF-Token": f'{self.token}'
        })

    def _request_with_reauth(self, method: str, url: str, **kwargs):
        response = self.client.request(method, url, **kwargs)

        if response.status_code == 401:
            # можно лог сюда
            print("401 → re-auth")

            self._authenticate()

            response = self.client.request(method, url, **kwargs)

        response.raise_for_status()
        return response

    def get(self, url: str, **kwargs) -> httpx.Response:
        return self._request_with_reauth("GET", url, **kwargs)

    def post(self, url: str, **kwargs) -> httpx.Response:
        return self._request_with_reauth("POST", url, **kwargs)

    def put(self, url: str, **kwargs) -> httpx.Response:
        return self._request_with_reauth("PUT", url, **kwargs)

    def delete(self, url: str, **kwargs) -> httpx.Response:
        return self._request_with_reauth("DELETE", url, **kwargs)

    def close(self) -> None:
        self.client.close()
