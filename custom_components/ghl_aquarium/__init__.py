from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

import logging
_LOGGER = logging.getLogger(__name__)

DOMAIN = "ghl_aquarium"
PLATFORMS = ["sensor"]  # ← ✅ REQUIRED!

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    hass.data[DOMAIN].pop(entry.entry_id)
    return True
