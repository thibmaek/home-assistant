"""The VRT Services integration."""
import asyncio

import voluptuous as vol

import pyvrt.weather as weather

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import TEMP_CELSIUS
from homeassistant.core import HomeAssistant
from homeassistant.components.weather import WeatherEntity

from .const import DOMAIN, CONF_REGION

CONFIG_SCHEMA = vol.Schema({DOMAIN: vol.Schema({})}, extra=vol.ALLOW_EXTRA)

PLATFORMS = ["weather"]


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the VRT Services component."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up VRT Services from a config entry."""
    # TODO Store an API object for your platforms to access
    # hass.data[DOMAIN][entry.entry_id] = MyApi(...)
    # hass.data[DOMAIN][entry.entry_id] = None

    async_add_entities([VRTWeather(hass, entry.data)], False)

    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )

    return True


class VRTWeather(WeatherEntity):
    def __init__(self, config):
        """Initialise the platform."""
        region = config.get(CONF_REGION)
        self._region = region

        self._unique_id = "{:2.6f}".format(region)

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"VRT Weather ({self._region})"

    @property
    def unique_id(self):
        """Return the unique id."""
        return self._unique_id

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    @property
    def temperature(self):
        """Return the current temperature."""
        return self._data.temperature


# async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
#     """Unload a config entry."""
#     unload_ok = all(
#         await asyncio.gather(
#             *[
#                 hass.config_entries.async_forward_entry_unload(entry, component)
#                 for component in PLATFORMS
#             ]
#         )
#     )
#     if unload_ok:
#         hass.data[DOMAIN].pop(entry.entry_id)

#     return unload_ok
