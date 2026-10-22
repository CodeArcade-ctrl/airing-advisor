"""Absolute humidity difference sensor."""

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity


DESCRIPTION = SensorEntityDescription(
    key="absolute_humidity_difference",
    translation_key="absolute_humidity_difference",
    native_unit_of_measurement="g/m³",
    state_class=SensorStateClass.MEASUREMENT,
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the difference sensor."""
    async_add_entities([HumidityDifferenceSensor(entry)])


class HumidityDifferenceSensor(CoordinatorEntity, SensorEntity):
    """Show indoor minus outdoor absolute humidity."""

    entity_description = DESCRIPTION
    _attr_has_entity_name = True

    def __init__(self, entry: ConfigEntry) -> None:
        """Initialize entity."""
        super().__init__(entry.runtime_data)
        self._attr_unique_id = f"{entry.entry_id}_humidity_difference"

    @property
    def native_value(self) -> float:
        """Return the humidity difference."""
        return self.coordinator.data["delta"]

    @property
    def extra_state_attributes(self) -> dict[str, float]:
        """Expose calculated absolute humidity and source readings."""
        return {
            "indoor_absolute_humidity": self.coordinator.data["indoor_absolute_humidity"],
            "outdoor_absolute_humidity": self.coordinator.data["outdoor_absolute_humidity"],
            "indoor_temperature_c": self.coordinator.data["indoor_temperature_c"],
            "outdoor_temperature_c": self.coordinator.data["outdoor_temperature_c"],
            "indoor_relative_humidity": self.coordinator.data["indoor_humidity"],
            "outdoor_relative_humidity": self.coordinator.data["outdoor_humidity"],
        }
