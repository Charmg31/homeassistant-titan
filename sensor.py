import asyncio
import aiohttp
import async_timeout
import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

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
        headers = {
            "Content-Type": "application/json",
            "Connection": "close",
            "User-Agent": "RT-Thread HTTP Agent"
        }
        try:
            with async_timeout.timeout(8):
                async with self._session.post(url, json={"config": config_param}, headers=headers) as response:
                    if response.status != 200:
                        raise UpdateFailed(f"Error fetching data: {response.status}")
                    data = await response.json()
                    return data
        except Exception as err:
            raise UpdateFailed(f"Error communicating with Izypower Titan: {err}")

async def async_setup_entry(hass, entry):
    session = aiohttp.ClientSession()
    coordinator = IzypowerCoordinator(hass, session, entry.data["host"], entry.data.get("port", 8080))
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault("izypower_titan", {})[entry.entry_id] = coordinator

    hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    return True

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


    async def async_update(self):
        await self.coordinator.async_request_refresh()


