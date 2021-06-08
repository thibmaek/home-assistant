"""The VRT Services integration."""
import asyncio

import voluptuous as vol

import pyvrt.weather as weather

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import TEMP_CELSIUS
from homeassistant.core import HomeAssistant
from homeassistant.components.weather import (
    WeatherEntity,
    ATTR_FORECAST_TIME,
    ATTR_FORECAST_CONDITION,
)

from .const import DOMAIN, CONF_REGION

CONFIG_SCHEMA = vol.Schema({DOMAIN: vol.Schema({})}, extra=vol.ALLOW_EXTRA)

PLATFORMS = ["weather"]


def setup(hass: HomeAssistant, config: dict):
    """Set up the VRT Services component."""
    return True


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
):
    """Set up VRT Services from a config entry."""
    # hass.data[DOMAIN][entry.entry_id] = VRTWeather(hass, entry.data)

    async_add_entities([VRTWeather(hass, entry.data)], False)


class VRTWeather(WeatherEntity):
    def __init__(self, config):
        """Initialise the platform."""
        region = config.get(CONF_REGION)

        self._data = self.get_current()
        self._forecast = self.get_forecast()
        self._region = region
        self._unique_id = "{:2.6f}".format(region)

    def get_current(self):
        current = weather.current(zone=self._region)
        return current

    def get_forecast(self):
        fc = weather.forecast(zone=self._region)
        return fc

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
    def wind_speed(self):
        """Return the current windspeed in km/h."""
        wind = self._data["wind"]

        if wind.get("speed"):
            return wind["speed"]

        return None

    @property
    def condition(self):
        """Return the current condition."""
        return self._data["weathertype"]

    @property
    def wind_bearing(self):
        """Return the current wind bearing"""
        wind = self._data["wind"]
        return wind["direction"]

    @property
    def temperature(self):
        """Return the current temperature."""
        current = self.get_current()
        return current["temperature"]

    # @property
    # def forecast(self):
    #     """Return the forecast array."""
    #     if not self._forecast:
    #         return None

    #     forecast_data = []

    #     for fcs in self._forecast["forecasts"]:
    #         forecast_data.append(
    #             {
    #                 ATTR_FORECAST_TIME: fcs.get("beginDate"),
    #                 ATTR_FORECAST_CONDITION: fcs.get("weathertype"),
    #             }
    #         )

    #     return forecast_data

    # fcdata_out = []
    # cond = self.hass.data[DATA_CONDITION]

    # if not self._data.forecast:
    #     return None

    # for data_in in self._data.forecast:
    #     # remap keys from external library to
    #     # keys understood by the weather component:
    #     condcode = data_in.get(CONDITION, []).get(CONDCODE)
    #     data_out = {
    #         ATTR_FORECAST_TIME: data_in.get(DATETIME),
    #         ATTR_FORECAST_CONDITION: cond[condcode],
    #         ATTR_FORECAST_TEMP_LOW: data_in.get(MIN_TEMP),
    #         ATTR_FORECAST_TEMP: data_in.get(MAX_TEMP),
    #         ATTR_FORECAST_PRECIPITATION: data_in.get(RAIN),
    #         ATTR_FORECAST_WIND_BEARING: data_in.get(WINDAZIMUTH),
    #         ATTR_FORECAST_WIND_SPEED: round(data_in.get(WINDSPEED) * 3.6, 1),
    #     }

    #     fcdata_out.append(data_out)

    # return fcdata_out
