import httpx
import typing

from .const import ATMEEX_API_BASE_URL, COMMON_HEADERS
from .exceptions import AtmeexAuthError

_NOT_AUTHENTICATED_MSG = "Not authenticated. Call client.signin_with_email() or client.request_sms_code() + signin_with_phone() first"


class AtmeexAuth(httpx.Auth):
    requires_response_body = True

    def __init__(self, access_token: str = "", refresh_token: str = ""):
        self._access_token_value = access_token
        self._refresh_token_value = refresh_token

    @property
    def access_token(self) -> str:
        """Get the current access token."""
        return self._access_token_value

    @access_token.setter
    def access_token(self, value: str) -> None:
        """Set the access token."""
        self._access_token_value = value

    @property
    def refresh_token(self) -> str:
        """Get the current refresh token."""
        return self._refresh_token_value

    @refresh_token.setter
    def refresh_token(self, value: str) -> None:
        """Set the refresh token."""
        self._refresh_token_value = value

    @staticmethod
    def request_phone_code(phone: str) -> httpx.Request:
        """Create request to send SMS code to phone number."""
        payload = {
            "grant_type": "phone_code",
            "phone": phone,
        }
        return httpx.Request(
            "POST", ATMEEX_API_BASE_URL + "/auth/signup", json=payload, headers=COMMON_HEADERS
        )

    @staticmethod
    def signin_with_phone(phone: str, phone_code: str) -> httpx.Request:
        """Create request to sign in with phone and SMS code."""
        payload = {
            "grant_type": "phone_code",
            "phone": phone,
            "phone_code": phone_code,
        }
        return httpx.Request(
            "POST", ATMEEX_API_BASE_URL + "/auth/signin", json=payload, headers=COMMON_HEADERS
        )

    @staticmethod
    def signin_with_email(email: str, password: str) -> httpx.Request:
        """Create request to sign in with email and password."""
        payload = {
            "email": email,
            "password": password,
            "grant_type": "basic",
        }
        return httpx.Request(
            "POST", ATMEEX_API_BASE_URL + "/auth/signin", json=payload, headers=COMMON_HEADERS
        )

    def auth_flow(self, request: httpx.Request) -> typing.Generator[httpx.Request, httpx.Response, None]:
        # Skip auth for authentication endpoints
        if "/auth/" in str(request.url):
            yield request
            return

        if self._access_token_value == "":
            raise AtmeexAuthError(_NOT_AUTHENTICATED_MSG)

        request.headers["authorization"] = f"Bearer {self._access_token_value}"
        response = yield request

        if response.status_code == 401:
            yield from self._refresh_token()
            request.headers["authorization"] = f"Bearer {self._access_token_value}"
            yield request

    def _refresh_token(self) -> typing.Generator[httpx.Request, httpx.Response, None]:
        if self._refresh_token_value == "":
            raise AtmeexAuthError(_NOT_AUTHENTICATED_MSG)

        payload = {
            "grant_type": "refresh_token",
            "refresh_token": self._refresh_token_value,
        }
        response = yield httpx.Request("POST", ATMEEX_API_BASE_URL + "/auth/signin", json=payload, headers=COMMON_HEADERS)
        if response.status_code == 401:
            raise AtmeexAuthError("Session expired. Please sign in again.")
        else:
            self._handle_auth_response(response)

    def _handle_auth_response(self, response: httpx.Response):
        response.raise_for_status()
        data = response.json()
        self._refresh_token_value = data["refresh_token"]
        self._access_token_value = data["access_token"]
