"""Config flow for Airing Advisor."""

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers import selector

from .const import (
    CONF_INDOOR_HUMIDITY,
    CONF_INDOOR_TEMPERATURE,
    CONF_OUTDOOR_HUMIDITY,
    CONF_OUTDOOR_TEMPERATURE,
    DOMAIN,
)


class AiringAdvisorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Select the indoor and outdoor sensor pairs."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.FlowResult:
        """Handle initial setup."""
        if user_input is not None:
            await self.async_set_unique_id(
                "_".join(
                    (
                        user_input[CONF_INDOOR_TEMPERATURE],
                        user_input[CONF_INDOOR_HUMIDITY],
                        user_input[CONF_OUTDOOR_TEMPERATURE],
                        user_input[CONF_OUTDOOR_HUMIDITY],
                    )
                )
            )
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title="Airing Advisor", data=user_input)

        temperature_selector = selector.EntitySelector(
            selector.EntitySelectorConfig(
                filter=[{"domain": "sensor", "device_class": "temperature"}]
            )
        )
        humidity_selector = selector.EntitySelector(
            selector.EntitySelectorConfig(
                filter=[{"domain": "sensor", "device_class": "humidity"}]
            )
        )
        schema = vol.Schema(
            {
                vol.Required(CONF_INDOOR_TEMPERATURE): temperature_selector,
                vol.Required(CONF_INDOOR_HUMIDITY): humidity_selector,
                vol.Required(CONF_OUTDOOR_TEMPERATURE): temperature_selector,
                vol.Required(CONF_OUTDOOR_HUMIDITY): humidity_selector,
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema)
