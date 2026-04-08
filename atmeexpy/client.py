import httpx

from .auth import AtmeexAuth
from .const import COMMON_HEADERS, ATMEEX_API_BASE_URL
from .device import Device


class AtmeexClient:

    def __init__(self, http_client: httpx.AsyncClient | None = None) -> None:
        self.auth = AtmeexAuth()
        if http_client is not None:
            self.http_client = http_client
            self.http_client.auth = self.auth
            self.http_client.headers.update(COMMON_HEADERS)
            self.http_client.base_url = ATMEEX_API_BASE_URL
        else:
            self.http_client = httpx.AsyncClient(
                auth=self.auth, headers=COMMON_HEADERS, base_url=ATMEEX_API_BASE_URL
            )

    async def request_sms_code(self, phone: str) -> None:
        """Send SMS code to phone number."""
        request = AtmeexAuth.request_phone_code(phone)
        response = await self.http_client.send(request)
        response.raise_for_status()

    async def signin_with_phone(self, phone: str, code: str) -> None:
        """Sign in with phone and SMS code."""
        request = AtmeexAuth.signin_with_phone(phone, code)
        response = await self.http_client.send(request)
        response.raise_for_status()
        data = response.json()
        self.auth.access_token = data["access_token"]
        self.auth.refresh_token = data["refresh_token"]

    async def signin_with_email(self, email: str, password: str) -> None:
        """Sign in with email and password."""
        request = AtmeexAuth.signin_with_email(email, password)
        response = await self.http_client.send(request)
        response.raise_for_status()
        data = response.json()
        self.auth.access_token = data["access_token"]
        self.auth.refresh_token = data["refresh_token"]

    def restore_tokens(self, access_token: str, refresh_token: str) -> None:
        """Restore session from saved tokens."""
        self.auth.access_token = access_token
        self.auth.refresh_token = refresh_token

    @property
    def access_token(self) -> str | None:
        """Get the current access token."""
        return self.auth.access_token

    @property
    def refresh_token(self) -> str | None:
        """Get the current refresh token."""
        return self.auth.refresh_token

    async def get_devices(self):
        resp = await self.http_client.get("/devices")
        devices_list = resp.json()
        try:
            devices = [Device(self.http_client, device_dict) for device_dict in devices_list]
        except Exception as e:
            print(devices_list)
            return []
        return devices

    def set_temp(self, device_id, temp):
        pass
