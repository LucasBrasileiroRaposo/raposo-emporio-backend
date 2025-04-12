from datetime import date
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional

class BatchRegisterDTO(BaseModel):
    expiration_date: date
    manufacture_date: date
    quantity: int = Field(..., gt=0)
    code: str = Field(..., min_length=1, max_length=50)
    product_id: Optional[int] = Field(default=None, exclude=True)

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