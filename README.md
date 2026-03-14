# atmeexpy

Python библиотека для работы с облачным API систем вентиляции Atmeex и управления бризерами Airnanny A7

## Установка

```bash
pip install atmeexpy
```

Или из исходников:

```bash
git clone https://github.com/anpavlov/atmeexpy.git
cd atmeexpy
pip install .
```

## Использование

### Базовый пример

```python
from atmeexpy.client import AtmeexClient

# Создание клиента
client = AtmeexClient("your_email@example.com", "your_password")

# Получение списка устройств
devices = await client.get_devices()

for device in devices:
    print(f"Устройство: {device.model.name}")
    print(f"  ID: {device.model.id}")
    print(f"  MAC: {device.model.mac}")
    print(f"  Онлайн: {device.model.online}")

    # Текущие настройки
    settings = device.model.settings
    print(f"  Питание: {'Вкл' if settings.u_pwr_on else 'Выкл'}")
    print(f"  Скорость вентилятора: {settings.u_fan_speed + 1}")
    print(f"  Позиция заслонки: {settings.u_damp_pos}")

```

### Управление устройством

```python
# Включение питания
await device.set_power_only(True)

# Выключение питания
await device.set_power_only(False)

# Установка скорости вентилятора (0-6, где 0 - минимальная)
await device.set_fan_speed(3)

# Управление заслонкой:
# 0 - открыта (приток с улицы)
# 1 - смешанный режим
# 2 - закрыта (рециркуляция)
await device.set_damp_pos(0)

# Установка температуры нагрева (в десятых долях градуса с шагом 0.5)
# Например, 225 = 22.5°C
await device.set_heat_temp(225)

# Выключение нагревателя (спец значение)
await device.set_heat_temp(-1000)

# Комбинированное управление питанием и заслонкой
await device.set_power_and_damp(True, 0)
```

### Сохранение и восстановление токенов

Для повторного входа можно сохранять и восстанавливать токены:

```python
client = AtmeexClient("your_email@example.com", "your_password")

# Первый вход - токены получены автоматически
devices = await client.get_devices()

# Сохраните токены в безопасном месте
access_token = client.auth._access_token
refresh_token = client.auth._refresh_token

# При следующем запуске восстановите токены
client2 = AtmeexClient("your_email@example.com", "your_password")
client2.restore_tokens(access_token, refresh_token)

# Теперь можно работать без повторной аутентификации
devices = await client2.get_devices()
```

## Интеграция с Home Assistant

Библиотека используется в интеграции [atmeex_hacs](https://github.com/anpavlov/atmeex_hacs) для Home Assistant.

## Лицензия

MIT License

## Автор

Andrey Pavlov
