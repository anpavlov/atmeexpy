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

### Авторизация

Библиотека поддерживает два способа авторизации: по email/паролю и по номеру телефона через SMS-код.

#### Email и пароль

```python
from atmeexpy.client import AtmeexClient

client = AtmeexClient()
await client.signin_with_email("your_email@example.com", "your_password")
```

#### Номер телефона (двухэтапная авторизация)

```python
from atmeexpy.client import AtmeexClient

client = AtmeexClient()

# Шаг 1: Отправка SMS-кода на номер
await client.request_sms_code("+79001234567")

# Шаг 2: Авторизация с кодом из SMS
code = "1234"  # код из SMS
await client.signin_with_phone("+79001234567", code)
```

### Базовый пример

```python
from atmeexpy.client import AtmeexClient

# Создание и авторизация клиента
client = AtmeexClient()
await client.signin_with_email("your_email@example.com", "your_password")

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
client = AtmeexClient()
await client.signin_with_email("your_email@example.com", "your_password")

# Сохраните токены в безопасном месте
access_token = client.auth._access_token
refresh_token = client.auth._refresh_token

# При следующем запуске восстановите сессию
client = AtmeexClient()
client.restore_tokens(access_token, refresh_token)
devices = await client.get_devices()
```

### Кастомный HTTP-клиент

Можно передать свой экземпляр `httpx.AsyncClient`:

```python
import httpx
from atmeexpy.client import AtmeexClient

custom_client = httpx.AsyncClient(timeout=30.0)
client = AtmeexClient(http_client=custom_client)
await client.signin_with_email("your_email@example.com", "your_password")
```

## Интеграция с Home Assistant

Библиотека используется в интеграции [atmeex_hacs](https://github.com/anpavlov/atmeex_hacs) для Home Assistant.

## Лицензия

MIT License

## Автор

Andrey Pavlov
