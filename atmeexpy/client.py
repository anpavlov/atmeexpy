import httpx

from .auth import AtmeexAuth
from .const import COMMON_HEADERS, ATMEEX_API_BASE_URL
from .device import Device

class AtmeexClient:

    def __init__(self, email: str, password: str) -> None:
        self.auth = AtmeexAuth(email, password)
        self.http_client = httpx.AsyncClient(auth=self.auth, headers=COMMON_HEADERS, base_url=ATMEEX_API_BASE_URL)

    def restore_tokens(self, access_token: str, refresh_token: str):
        self.auth._access_token = access_token
        self.auth._refresh_token = refresh_token

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