import voluptuous as vol
from homeassistant import config_entries

DOMAIN = "izypower_titan"

class IzypowerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            if not user_input.get("confirm_acknowledgement", False):
                errors["base"] = "acknowledgement_required"
            else:
                return self.async_create_entry(title="Izypower Titan", data=user_input)

        data_schema = vol.Schema(
            {
                vol.Required("host"): str,
                vol.Optional("port", default=8080): int,
                vol.Required("confirm_acknowledgement", default=False): bool,
            }
        )
        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "warning": "Attention : Ce composant est fait pour les batteries Izypower Titan uniquement. Utilisation à vos risques et périls. Nous déclinons toute responsabilité en cas de dommages."
            },
        )

