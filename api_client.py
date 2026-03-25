import httpx


class ApiClient:
    def __init__(
        self,
        base_url: str,
        login: str,
        password: str,
        auth_path: str = "/auth/v4/public/token",
        timeout: float = 10.0,
    ):
        self.base_url = base_url.rstrip("/")
        self.login = login
        self.password = password
        self.auth_path = auth_path
        self.token: str | None = None

        self.client = httpx.Client(
            base_url=self.base_url,
            timeout=timeout,
            verify=False,
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

    def get(self, url: str, **kwargs) -> httpx.Response:
        response = self.client.get(url, **kwargs)
        response.raise_for_status()
        return response

    def post(self, url: str, **kwargs) -> httpx.Response:
        response = self.client.post(url, **kwargs)
        response.raise_for_status()
        return response

    def put(self, url: str, **kwargs) -> httpx.Response:
        response = self.client.put(url, **kwargs)
        response.raise_for_status()
        return response

    def delete(self, url: str, **kwargs) -> httpx.Response:
        response = self.client.delete(url, **kwargs)
        response.raise_for_status()
        return response

    def close(self) -> None:
        self.client.close()