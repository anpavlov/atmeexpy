# Atmeex API
Controling Atmeex airnanny breezers with python using atmeex cloud.

You need to create user in Atmeex mobile app and add your breezers. Next you can start getting information about breezers and control them with this library.

```python
from atmeexpy.client import AtmeexClient

atmeex = AtmeexClient(email, password)
devices = await atmeex.get_devices()

await devices[0].set_fan_speed(3)
await devices[0].set_heat_temp(200)
await devices[0].set_power(False)

if not device[0].model.settings.u_pwr_on:
  print("breezer is off!")
```
