from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorEntityDescription, SensorStateClass
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import EntityCategory
from .utils import get_device_gen
from .const import DOMAIN
from dataclasses import dataclass, field
from typing import Final
from homeassistant.const import (
    UnitOfEnergy,
    UnitOfPower,
    PERCENTAGE
)
import logging

_LOGGER = logging.getLogger(__name__)

@dataclass(frozen=True, kw_only=True)
class TitanIzyPowerSensorEntityDescription(SensorEntityDescription):
    name: str = ""
    coefficient: float = 1.0
    state_mapping: dict[int, str] = field(default_factory=dict)
    translation_key: str | None = None
    entity_category: EntityCategory | None = None

SENSORS_GEN1: Final = (
    TitanIzyPowerSensorEntityDescription(
        key="1001",  # à remplacer par les vrais codes Titan
        name="Entrée PV1",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT
    ),
    # Ajoute les autres sensors avec les clés/documentation spécifiques Titan IzyPower…
)

SENSORS_GEN2: Final = (
    # Idem pour Gen2...
)

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities = []
    if get_device_gen(coordinator.config_entry.data.get("device_model")) == 1:
        for desc in SENSORS_GEN1:
            entities.append(TitanIzyPowerSensorEntity(coordinator=coordinator, description=desc))
    else:
        for desc in SENSORS_GEN2:
            entities.append(TitanIzyPowerSensorEntity(coordinator=coordinator, description=desc))
    async_add_entities(entities)

class TitanIzyPowerSensorEntity(CoordinatorEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator, description: TitanIzyPowerSensorEntityDescription):
        super().__init__(coordinator)
        self.entity_description = description
        sn = coordinator.config_entry.data.get("sn", "unknown")
        model = coordinator.config_entry.data.get("device_model", "unknown")
        self._attr_unique_id = f"{DOMAIN}_{sn}_{coordinator.config_entry.entry_id}_{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.config_entry.entry_id)},
            manufacturer="TITAN IZYPOWER",
            name=f"TITAN IZYPOWER {model}",
            serial_number=sn,
            model=model,
            sw_version=coordinator.config_entry.data.get("fw_version", "unknown"),
        )
        if description.device_class == SensorDeviceClass.ENUM:
            self._attr_options = list(set(description.state_mapping.values()))

    @property
    def native_value(self):
        raw_value = self.coordinator.data.get(self.entity_description.key)
        if raw_value is None:
            return None
        if self.entity_description.device_class == SensorDeviceClass.ENUM:
            return self.entity_description.state_mapping.get(raw_value)
        return raw_value * self.entity_description.coefficient
