from dataclasses import dataclass, asdict
from typing import Optional

from dacite import from_dict

# u_pwr_on - питание вентилятора
# 
# u_damp_pos:
# 0 - открыта заслонка
# 1 - смешанный режим
# 2 - закрыта заслонка
# например можно послать {"u_pwr_on": false, "u_damp_pos": 0}
# и будет режим пассивного проветривания
# 
# u_temp_room - установка нагрева - температура * 10
# температура от 10 до 30 с шагом 0.5
# установка температуры -1000 выключает обогрев
# 
# u_fan_speed - скорость вентилятора - от 0 до 6

class Model:
    dict = asdict

@dataclass
class DeviceSettingsModel(Model):
    id: int
    device_id: int
    u_pwr_on: bool
    u_fan_speed: int
    u_damp_pos: int
    u_hum_stg: int
    u_temp_room: int
    u_auto: bool
    u_night: bool
    u_cool_mode: bool
    u_night_start: str
    u_night_stop: str
    u_time_zone: Optional[str]

    @staticmethod
    def fromdict(data):
        return from_dict(data_class=DeviceSettingsModel, data=data)

@dataclass
class DeviceSettingsSetModel(Model):
    u_pwr_on: Optional[bool]
    u_fan_speed: Optional[int]
    u_damp_pos: Optional[int]
    u_temp_room: Optional[int]

    def __init__(self, u_pwr_on=None, u_fan_speed=None, u_damp_pos=None, u_temp_room=None):
        self.u_damp_pos = u_damp_pos
        self.u_fan_speed = u_fan_speed
        self.u_pwr_on = u_pwr_on
        self.u_temp_room = u_temp_room

    def dict(self):
        d = asdict(self, dict_factory=lambda x:
                   {k: v for (k, v) in x if v is not None})
        if len(d) == 0:
            raise ValueError("Can't serialize DeviceSettingsSet when every field is None")

        return d

@dataclass
class DeviceConditionModel(Model):
    time: str
    pwr_on: int
    no_water: int
    co2_ppm: int
    temp_in: int
    temp_room: int
    fan_speed: int
    damp_pos: int
    hum_room: int
    hum_stg: int
    firmware_version: str
    server_time: str
    device_id: int
    created_at: str

    @staticmethod
    def fromdict(data):
        return from_dict(data_class=DeviceConditionModel, data=data)

@dataclass
class DeviceModel(Model):
    id: int
    mac: str
    type: int
    name: str
    room_id: int
    owner_id: int
    created_at: str
    socket_id: str
    fw_ver: str
    model: str
    online: Optional[bool]
    settings: DeviceSettingsModel
    condition: Optional[DeviceConditionModel]

    @staticmethod
    def fromdict(data):
        return from_dict(data_class=DeviceModel, data=data)