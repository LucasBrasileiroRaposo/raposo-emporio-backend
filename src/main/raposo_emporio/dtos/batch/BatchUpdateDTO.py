from typing import Optional
from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import date

class BatchUpdateDTO(BaseModel):
    expiration_date: Optional[date] = None
    manufacture_date: Optional[date] = None
    quantity: Optional[int] = Field(None, ge=0)
    code: Optional[str] = Field(None, min_length=1, max_length=50)

    @model_validator(mode="after")
    def expiration_after_manufacture(cls, values):
        if values.expiration_date  <= values.manufacture_date:
            raise ValueError("Expiration date must be after manufacture date")
        return values

    @field_validator("manufacture_date")
    def manufacture_in_the_past(cls, value):
        today = date.today()
        if value >= today:
            raise ValueError("Manufacture date must be in the past")
        return value