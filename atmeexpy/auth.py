import httpx
import typing

from .const import ATMEEX_API_BASE_URL


class AtmeexAuth(httpx.Auth):
    requires_response_body = True

    def __init__(self, email: str, password: str, access_token: str = "", refresh_token: str = ""):
        self.email = email
        self.password = password
        self._access_token = access_token
        self._refresh_token = refresh_token

    def auth_flow(self, request: httpx.Request) -> typing.Generator[httpx.Request, httpx.Response, None]:
        if self._access_token == "":
            yield from self.auth_with_email()

        request.headers["authorization"] = f"Bearer {self._access_token}"
        response = yield request

        if response.status_code == 401:
            yield from self.refresh_token()
            yield request

    def refresh_token(self) -> typing.Generator[httpx.Request, httpx.Response, None]:
        if self._refresh_token == "":
            yield from self.auth_with_email()
            return

        payload = {
            "grant_type": "refresh_token",
            "refresh_token": self._refresh_token,
        }
        response = yield httpx.Request("POST", ATMEEX_API_BASE_URL + "/auth/signin", json=payload, headers={"accept": "application/json", "user-agent": "okhttp/3.14.9"})
        self.handle_auth_response(response)

    def auth_with_email(self) -> typing.Generator[httpx.Request, httpx.Response, None]:
        payload = {
            "email": self.email,
            "password": self.password,
            "grant_type": "basic",
        }
        response = yield httpx.Request("POST", ATMEEX_API_BASE_URL + "/auth/signin", json=payload, headers={"accept": "application/json", "user-agent": "okhttp/3.14.9"})
        self.handle_auth_response(response)

    def handle_auth_response(self, response: httpx.Response):
        response.raise_for_status()

        data = response.json()
        self._refresh_token = data["refresh_token"]
        self._access_token = data["access_token"]