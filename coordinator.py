from __future__ import annotations

import logging
from typing import Any, Dict
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, DEFAULT_SCAN_INTERVAL
from .titanizypower_api import TitanIzyPowerAPI
from .utils import get_device_gen

_LOGGER = logging.getLogger(__name__)

class TitanIzyPowerCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, entry: ConfigEntry):

        scan_interval = entry.options.get(
            "scan_interval",
            entry.data.get("scan_interval", DEFAULT_SCAN_INTERVAL)
        )

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=scan_interval),
        )

        self.config_entry = entry
        self.session = async_get_clientsession(hass)

        self.api = TitanIzyPowerAPI(
            host=entry.data['host'],
            port=entry.data['port'],
            session=async_get_clientsession(self.hass)
        )

    @property
    def config(self) -> dict:
        return {**self.config_entry.data, **self.config_entry.options}

    async def _async_update_data(self) -> Dict[str, Any]:
        try:
            keys = []
            if get_device_gen(self.config["device_model"]) == 1:
                keys = [/* Clés spécifiques Gen 1 Titan, à adapter selon la doc */]
            else:
                keys = [/* Clés spécifiques Gen 2 Titan, à adapter selon la doc */]

            data: Dict[str, Any] = {}
            for key in keys:
                result = await self.api.fetch_data([key])
                data.update(result)

            return data

        except Exception as err:
            _LOGGER.error("API request failed: %s", str(err))
            return self.data or {}

        except Exception as err:
            _LOGGER.exception("Unexpected update error")
            raise UpdateFailed(f"Update failed: {err}") from err
