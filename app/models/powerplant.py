from pydantic import BaseModel, ConfigDict, field_validator, model_validator

class PowerPlant(BaseModel):
    name: str
    type: str
    efficiency: float
    pmin: float
    pmax: float

    @field_validator('efficiency', 'pmin', 'pmax')
    def check_non_negative(cls, v, field):
        if v < 0:
            raise ValueError(f"{field} must be non-negative")
        return v

    @model_validator(mode='after')
    def check_pmax_gte_pmin(cls, values):
        pmin = values.pmin
        pmax = values.pmax
        if pmin is not None and pmax is not None and pmax < pmin:
            raise ValueError("pmax must be greater than or equal to pmin")
        return values

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True
    )