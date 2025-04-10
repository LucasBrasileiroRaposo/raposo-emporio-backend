from datetime import date
from pydantic import BaseModel, Field, field_validator


class BatchRegisterDTO(BaseModel):
    expiration_date: date
    manufacture_date: date
    quantity: int = Field(..., gt=0)
    code: str = Field(..., min_length=1, max_length=50)

    @field_validator("expiration_date")
    def expiration_after_manufacture(cls, value, values):
        manufacture_date = values.get("manufacture_date")
        if manufacture_date and value <= manufacture_date:
            raise ValueError("Expiration date must be after manufacture date")
        return value

    @field_validator("manufacture_date")
    def manufacture_in_the_past(cls, value):
        today = date.today()
        if value >= today:
            raise ValueError("Manufacture date must be in the past")
        return value