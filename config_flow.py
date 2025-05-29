from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector
import voluptuous as vol
from .const import DOMAIN
from .websocket_api import get_sensor_value

class GHLConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            ip = user_input["ip"]

            # Validate connection
            try:
                value = await get_sensor_value(ip, sensor_id=0)  # Try temperature sensor 0
                if value is None:
                    errors["base"] = "cannot_connect"
                else:
                    return self.async_create_entry(title=f"GHL Aquarium ({ip})", data={"ip": ip})
            except Exception:
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("ip"): str,
            }),
            errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return GHLConfigOptionsFlowHandler(config_entry)

class GHLConfigOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        return self.async_show_form(step_id="init", data_schema=vol.Schema({}))
