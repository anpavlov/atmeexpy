from dataclasses import dataclass

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
# 
# u_fan_speed - скорость вентилятора - от 0 до 6




@dataclass
class DeviceSettings:
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
    u_time_zone: str

@dataclass
class DeviceCondition:
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

@dataclass
class Device:
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
    online: bool
    settings: DeviceSettings
    condition: DeviceCondition