from clients.api_client import ApiClient
import time

api = ApiClient(
    base_url="https://172.31.48.29/",
    login="test@test.com",
    password="Ru77Kq67",
)

# resp = api.get("/auth/v4/self/session")
# print(resp.json())

start = time.perf_counter()

resp = api.get(
    "/dci/v3/server",
    params={
        # "where": "name CP '%Srv-1768461385-450%'",
        "limit": "100"
    },
)


end = time.perf_counter()
data = resp.json()
print(data["size"])
print(len(data["list"]))
print(f"Request time: {end - start:.3f} sec")