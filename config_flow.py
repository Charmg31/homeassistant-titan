import voluptuous as vol
from homeassistant.config_entries import ConfigFlow, OptionsFlow, ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import DOMAIN, DEFAULT_PORT, DEFAULT_SCAN_INTERVAL, SUPPORTED_MODELS
from .utils import get_device_gen
import logging
import asyncio
from .izypower_api import IzyPowerAPI  # Remplacer par votre API Titan IzyPower

_LOGGER = logging.getLogger(__name__)

class IzyPowerConfigFlow(ConfigFlow, domain=DOMAIN):
    """[translate:Configuration] flow pour l'intégration Titan IzyPower."""

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        """Retourne le gestionnaire du flow des options."""
        return IzyPowerOptionsFlowHandler(config_entry)

    async def async_step_user(self, user_input=None):
        """Gère la première étape de configuration."""
        errors = {}
        if user_input is not None:
            host = user_input["host"]
            port = user_input.get("port", DEFAULT_PORT)
            scan_interval = user_input.get("scan_interval", DEFAULT_SCAN_INTERVAL)
            device_model = user_input["device_model"]

            api = IzyPowerAPI(host, port, async_get_clientsession(self.hass))
            device_gen = get_device_gen(device_model)

            try:
                # Simulation de récupération version firmware spécifique Titan
                if device_gen == 1:
                    fw_version = "Titan_IzyPower_V1.0.0"
                else:
                    fw_version = "Titan_IzyPower_V2.0.0"

                # Exemple d'appel API pour récupérer numéro de série
                data = await api.fetch_data(["serial_number"])
                device_sn = data.get("serial_number")

                return self.async_create_entry(
                    title=f"TITAN IZYPOWER {device_model} ({host})",
                    data={
                        "host": host,
                        "port": port,
                        "scan_interval": scan_interval,
                        "sn": device_sn,
                        "device_model": device_model,
                        "fw_version": fw_version
                    }
                )

            except asyncio.TimeoutError:
                errors["base"] = "timeout"
            except Exception as e:
                _LOGGER.error("Erreur inconnue lors de la validation du dispositif: %s", str(e), exc_info=True)
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("host"): str,
                vol.Optional("port", default=DEFAULT_PORT): int,
                vol.Optional("scan_interval", default=DEFAULT_SCAN_INTERVAL): int,
                vol.Required("device_model"): vol.In(SUPPORTED_MODELS),
            }),
            errors=errors
        )

class IzyPowerOptionsFlowHandler(OptionsFlow):
    """Gestionnaire du flow d'options pour Titan IzyPower."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional(
                    "scan_interval",
                    default=self.config_entry.options.get(
                        "scan_interval",
                        self.config_entry.data.get("scan_interval", DEFAULT_SCAN_INTERVAL)
                    ),
                ): int,
            }),
        )
