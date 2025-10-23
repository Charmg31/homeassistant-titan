
from __future__ import annotations

"""Intégration Home Assistant pour Titan IzyPower."""

import logging
from typing import Any
from datetime import timedelta
import voluptuous as vol

from homeassistant.helpers import config_validation as cv
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN, PLATFORMS, DEFAULT_SCAN_INTERVAL
from .coordinator import TitanIzyPowerCoordinator

_LOGGER = logging.getLogger(__name__)

SERVICE_SCHEMA = vol.Schema({
    vol.Required("power"): cv.positive_int,
})

async def async_setup(hass: HomeAssistant, config: dict[str, Any]) -> bool:
    """Initialise l’intégration Titan IzyPower (configuration de base)."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Configure Titan IzyPower à partir d’une entrée de configuration."""
    hass.data.setdefault(DOMAIN, {})

    try:
        coordinator = TitanIzyPowerCoordinator(hass, entry)
        await coordinator.async_config_entry_first_refresh()
        hass.data[DOMAIN][entry.entry_id] = coordinator
        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
        entry.async_on_unload(entry.add_update_listener(async_update_listener))

        # --- SERVICES PERSONNALISÉS ---
        async def charge(call: ServiceCall) -> None:
            """Démarrer la charge de la batterie (depuis réseau ou solaire)."""
            power = call.data["power"]
            # Adapter cette ligne à l’API exacte de ton communicateur Titan
            await coordinator.api.send_command("charge", power=power)

        async def discharge(call: ServiceCall) -> None:
            """Déclencher la décharge de la batterie (alimentation maison)."""
            power = call.data["power"]
            await coordinator.api.send_command("discharge", power=power)

        async def stop(call: ServiceCall) -> None:
            """Met la batterie en veille (arrête charge/décharge)."""
            await coordinator.api.send_command("stop")

        async def set_realtime_mode(call: ServiceCall) -> None:
            """Active le contrôle temps réel sur Titan IzyPower."""
            await coordinator.api.send_command("set_realtime_mode")

        hass.services.async_register(DOMAIN, "charge", charge, schema=SERVICE_SCHEMA)
        hass.services.async_register(DOMAIN, "discharge", discharge, schema=SERVICE_SCHEMA)
        hass.services.async_register(DOMAIN, "stop", stop)
        hass.services.async_register(DOMAIN, "set_realtime_mode", set_realtime_mode)

        return True

    except Exception as err:
        _LOGGER.exception("Erreur inattendue lors de l’initialisation de l’entrée Titan IzyPower.")
        hass.data[DOMAIN].pop(entry.entry_id, None)
        raise ConfigEntryNotReady from err

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Désinstalle intégration Titan IzyPower et supprime les services."""
    if DOMAIN not in hass.data or entry.entry_id not in hass.data[DOMAIN]:
        return True

    hass.services.async_remove(DOMAIN, "charge")
    hass.services.async_remove(DOMAIN, "discharge")
    hass.services.async_remove(DOMAIN, "stop")
    hass.services.async_remove(DOMAIN, "set_realtime_mode")

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        coordinator = hass.data[DOMAIN].pop(entry.entry_id)
        await coordinator.async_shutdown()
        if not hass.data[DOMAIN]:
            hass.data.pop(DOMAIN)

    return unload_ok

async def async_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Met à jour l’intervalle de scan après changement d’options."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    new_interval = entry.options.get("scan_interval", DEFAULT_SCAN_INTERVAL)
    coordinator.update_interval = timedelta(seconds=new_interval)
    _LOGGER.info(f"Intervalle d’actualisation Titan IzyPower mis à jour : {new_interval} secondes.")

