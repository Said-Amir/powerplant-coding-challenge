from pydantic import BaseModel, field_validator, AliasChoices, Field, model_validator
from typing import List
from .powerplant import PowerPlant

class Fuels(BaseModel):
    gas: float = Field(validation_alias=AliasChoices("gas(euro/MWh)", "gas"))
    kerosine: float = Field(validation_alias=AliasChoices("kerosine(euro/MWh)", "kerosine"))
    co2: float = Field(validation_alias=AliasChoices("co2(euro/ton)", "co2"))
    wind: float = Field(validation_alias=AliasChoices("wind(%)", "wind"))

    @field_validator('*')
    def check_positive(cls, v, info):
        if v < 0:
            raise ValueError(f"{info.field_name} values must be non-negative")
        return v

class Payload(BaseModel):
    load: float
    fuels: Fuels
    powerplants: List[PowerPlant]

    @field_validator('load')
    def check_non_negative_load(cls, v):
        if v < 0:
            raise ValueError('Load must be non-negative')
        return v
    
    @field_validator('powerplants')
    def check_non_empty_powerplants(cls, v):
        if len(v) == 0:
            raise ValueError('Powerplants list must not be empty')
        return v

@model_validator(mode='after')
def check_load_against_pmin(cls, values):
    load = values.load
    fuels = values.fuels
    powerplants = values.powerplants

    if powerplants:
        # Determine the minimum pmin, excluding wind turbines if wind is 0
        min_pmin = float('inf')
        for plant in powerplants:
            plant_type = plant.type
            plant_pmin = plant.pmin
            wind = fuels.wind

            if plant_type != 'windturbine' or wind != 0:
                min_pmin = min(min_pmin, plant_pmin)

        if load < min_pmin:
            raise ValueError(f'Load {load} is less than the minimum pmin {min_pmin} of the powerplants')

    return values
