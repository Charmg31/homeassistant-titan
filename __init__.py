"""Izypower Titan battery integration."""

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Initial setup if needed."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up integration from config flow entry."""
    hass.data.setdefault("izypower_titan", {})

    # Load platforms (sensor, switch, etc.)
    hass.config_entries.async_setup_platforms(entry, ["sensor", "switch"])
    return True
