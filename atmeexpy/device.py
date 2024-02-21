import traceback
import httpx
from dacite import from_dict

from .models import DeviceModel, DeviceSettingsSetModel

class Device:
    model: DeviceModel
    _http_client: httpx.AsyncClient
    
    def __init__(self, http_client: httpx.Client, data: dict):
        self._http_client = http_client
        self.model = from_dict(data_class=DeviceModel, data=data)

    async def _set_params(self, params: DeviceSettingsSetModel):
        resp = await self._http_client.put(f"/devices/{self.model.id}/params", json=params.dict())
        resp.raise_for_status()
        device_info = resp.json()
        try:
            model = from_dict(data_class=DeviceModel, data = device_info)
        except Exception:
            print(traceback.format_exc())
            print(device_info)

    async def set_heat_temp(self, temp: int):
        if temp < 100 or temp > 300:
            raise ValueError(f"set_heat_temp temp not between 100 and 300: {temp}")

        if temp % 10 not in [0, 5]:
            raise ValueError(f"set_heat_temp temp ends not with 0 or 5: {temp}")

        await self._set_params(DeviceSettingsSetModel(u_temp_room=temp))

    async def set_fan_speed(self, fan_speed: int):
        if fan_speed < 0 or fan_speed > 6:
            raise ValueError(f"set_fan_speed fan_speed not between 0 and 6: {fan_speed}")

        await self._set_params(DeviceSettingsSetModel(u_fan_speed=fan_speed))

    async def set_power(self, power: bool):
        if power:
            await self._set_params(DeviceSettingsSetModel(u_damp_pos=0, u_pwr_on=True))
        else:
            await self._set_params(DeviceSettingsSetModel(u_damp_pos=2, u_pwr_on=False))
