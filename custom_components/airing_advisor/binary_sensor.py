"""Ventilation recommendation binary sensor."""

from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity


DESCRIPTION = BinarySensorEntityDescription(
    key="ventilation_recommended",
    translation_key="ventilation_recommended",
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the ventilation recommendation entity."""
    async_add_entities([VentilationRecommendationSensor(entry)])


class VentilationRecommendationSensor(CoordinatorEntity, BinarySensorEntity):
    """Turn on when airing out may reduce indoor moisture."""

    entity_description = DESCRIPTION
    _attr_has_entity_name = True

    def __init__(self, entry: ConfigEntry) -> None:
        """Initialize entity."""
        super().__init__(entry.runtime_data)
        self._attr_unique_id = f"{entry.entry_id}_ventilation_recommended"

    @property
    def is_on(self) -> bool:
        """Return whether outside absolute humidity is sufficiently lower."""
        return self.coordinator.data["recommend"]
