import asyncio
import aiohttp
import async_timeout
import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.core import callback

_LOGGER = logging.getLogger(__name__)

API_ENDPOINT = "/rpc/Indevolt.GetData?config="

SENSOR_CODES = {
    "dc_input_power_1": 1664,
    "dc_input_power_2": 1665,
    "dc_input_power_3": 1666,
    "dc_input_power_4": 1667,
    "battery_power": 6000,
    "battery_soc": 6002,
}

class IzypowerCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, session, host, port):
        super().__init__(hass, _LOGGER, name="Izypower Titan Data", update_interval=30)
        self._session = session
        self._host = host
        self._port = port

    async def _async_update_data(self):
        url = f"http://{self._host}:{self._port}{API_ENDPOINT}"
        codes = list(SENSOR_CODES.values())
        config_param = {"t": codes}
        try:
            with async_timeout.timeout(10):
                async with self._session.post(url, json={"config": config_param}) as response:
                    if response.status != 200:
                        raise UpdateFailed(f"Error fetching data: {response.status}")
                    data = await response.json()
                    return data
        except Exception as err:
            raise UpdateFailed(f"Error communicating with Izypower Titan: {err}")

class IzypowerSensor(SensorEntity):
    def __init__(self, coordinator, sensor_key):
        self.coordinator = coordinator
        self.sensor_key = sensor_key
        self._attr_name = f"Izypower Titan {sensor_key.replace('_', ' ').title()}"

    @property
    def native_value(self):
        data = self.coordinator.data
        keys = list(SENSOR_CODES.keys())
        try:
            index = keys.index(self.sensor_key)
            return data["data"][0]["value"][index]
        except (KeyError, IndexError, TypeError):
            return None

    async def async_update(self):
        await self.coordinator.async_request_refresh()

