from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN, SENSOR_TYPES
from .websocket_api import get_sensor_value

import logging
_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = 60  # seconds

async def async_setup_entry(hass, config_entry, async_add_entities):
    ip = config_entry.data["ip"]
    sensors = []

    for sensor_id, sensor_type in SENSOR_TYPES.items():
        _LOGGER.debug("Adding GHL %s Sensor %d", sensor_type, sensor_id)
        sensors.append(GHLSensor(ip, sensor_id, sensor_type))

    async_add_entities(sensors, update_before_add=True)

class GHLSensor(SensorEntity):
    def __init__(self, ip, sensor_id, sensor_type):
        self._ip = ip
        self._sensor_id = sensor_id
        self._sensor_type = sensor_type

        self._attr_name = f"GHL {sensor_type.capitalize()} Sensor {sensor_id}"
        self._attr_unique_id = f"ghl_{sensor_type}_{sensor_id}"
        self._attr_native_unit_of_measurement = {
            "temperature": "°C",
            "ph": "pH",
        }.get(sensor_type)
        self._attr_native_value = None

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, ip)},
            name="GHL Aquarium Computer",
            manufacturer="GHL",
            model="ProfiLux",
        )

    async def async_update(self):
        self._attr_native_value = await get_sensor_value(self._ip, self._sensor_id)
