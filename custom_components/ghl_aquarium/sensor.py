from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator
from .const import DOMAIN, SENSOR_TYPES
from .websocket_api import get_sensor_value

SCAN_INTERVAL = 60  # seconds

async def async_setup_entry(hass, config_entry, async_add_entities):
    ip = config_entry.data["ip"]
    sensors = []

    for sensor_id, sensor_type in SENSOR_TYPES.items():
        sensors.append(GHLSensor(ip, sensor_id, sensor_type))

    async_add_entities(sensors)

class GHLSensor(SensorEntity):
    def __init__(self, ip, sensor_id, sensor_type):
        self._ip = ip
        self._sensor_id = sensor_id
        self._sensor_type = sensor_type
        self._attr_name = f"GHL {sensor_type} Sensor {sensor_id}"
        self._attr_unique_id = f"ghl_{sensor_type}_{sensor_id}"
        self._attr_native_unit_of_measurement = "°C" if sensor_type == "temperature" else None
        self._attr_native_value = None

    async def async_update(self):
        self._attr_native_value = await get_sensor_value(self._ip, self._sensor_id)
