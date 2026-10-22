"""Calculate absolute humidity for indoor and outdoor sensor pairs."""

from datetime import timedelta
import logging
import math
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    CONF_INDOOR_HUMIDITY,
    CONF_INDOOR_TEMPERATURE,
    CONF_OUTDOOR_HUMIDITY,
    CONF_OUTDOOR_TEMPERATURE,
    DOMAIN,
    VENTILATION_DELTA_G_M3,
)

_LOGGER = logging.getLogger(__name__)


def _read_value(hass: HomeAssistant, entity_id: str, kind: str) -> tuple[float, str]:
    """Read a numeric state and its unit."""
    state = hass.states.get(entity_id)
    if state is None or state.state in ("unknown", "unavailable"):
        raise UpdateFailed(f"The selected {kind} sensor is unavailable")
    try:
        value = float(state.state)
    except (TypeError, ValueError) as err:
        raise UpdateFailed(f"The selected {kind} sensor is not numeric") from err
    if not math.isfinite(value):
        raise UpdateFailed(f"The selected {kind} sensor has an invalid value")
    return value, state.attributes.get("unit_of_measurement", "")


def _absolute_humidity(temp_c: float, relative_humidity: float) -> float:
    """Calculate approximate absolute humidity in grams per cubic meter."""
    vapor_pressure = 6.112 * math.exp((17.62 * temp_c) / (243.12 + temp_c))
    return 216.7 * (vapor_pressure * relative_humidity / 100) / (273.15 + temp_c)


async def async_update_readings(
    hass: HomeAssistant, config: dict[str, Any]
) -> dict[str, Any]:
    """Read all four source sensors and calculate ventilation recommendation."""
    indoor_temp, indoor_temp_unit = _read_value(
        hass, config[CONF_INDOOR_TEMPERATURE], "indoor temperature"
    )
    outdoor_temp, outdoor_temp_unit = _read_value(
        hass, config[CONF_OUTDOOR_TEMPERATURE], "outdoor temperature"
    )
    indoor_rh, indoor_rh_unit = _read_value(
        hass, config[CONF_INDOOR_HUMIDITY], "indoor humidity"
    )
    outdoor_rh, outdoor_rh_unit = _read_value(
        hass, config[CONF_OUTDOOR_HUMIDITY], "outdoor humidity"
    )

    for label, value, unit in (
        ("indoor", indoor_temp, indoor_temp_unit),
        ("outdoor", outdoor_temp, outdoor_temp_unit),
    ):
        if unit in ("°F", "F"):
            if label == "indoor":
                indoor_temp = (value - 32) * 5 / 9
            else:
                outdoor_temp = (value - 32) * 5 / 9
        elif unit not in ("°C", "C"):
            raise UpdateFailed("Temperature sensors must report °C or °F")
    if not -100 <= indoor_temp <= 100 or not -100 <= outdoor_temp <= 100:
        raise UpdateFailed("Temperature values are outside the supported range")

    if indoor_rh_unit != "%" or outdoor_rh_unit != "%":
        raise UpdateFailed("Humidity sensors must report a percentage")
    if not 0 <= indoor_rh <= 100 or not 0 <= outdoor_rh <= 100:
        raise UpdateFailed("Humidity values must be between 0 and 100 percent")

    indoor_ah = _absolute_humidity(indoor_temp, indoor_rh)
    outdoor_ah = _absolute_humidity(outdoor_temp, outdoor_rh)
    delta = indoor_ah - outdoor_ah
    return {
        "indoor_absolute_humidity": round(indoor_ah, 2),
        "outdoor_absolute_humidity": round(outdoor_ah, 2),
        "delta": round(delta, 2),
        "recommend": delta >= VENTILATION_DELTA_G_M3,
        "indoor_temperature_c": round(indoor_temp, 1),
        "outdoor_temperature_c": round(outdoor_temp, 1),
        "indoor_humidity": round(indoor_rh, 1),
        "outdoor_humidity": round(outdoor_rh, 1),
    }


def create_coordinator(hass: HomeAssistant, config: dict[str, Any]) -> DataUpdateCoordinator:
    """Create the shared 60-second update coordinator."""
    return DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=lambda: async_update_readings(hass, config),
        update_interval=timedelta(seconds=60),
    )
