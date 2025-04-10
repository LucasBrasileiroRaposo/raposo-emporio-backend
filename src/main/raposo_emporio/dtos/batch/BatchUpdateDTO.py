from typing import Optional
from pydantic import BaseModel, Field
from datetime import date

class BatchUpdateDTO(BaseModel):
    expiration_date: Optional[date] = None
    manufacture_date: Optional[date] = None
    quantity: Optional[int] = Field(None, ge=0)
    code: Optional[str] = Field(None, min_length=1, max_length=50)
