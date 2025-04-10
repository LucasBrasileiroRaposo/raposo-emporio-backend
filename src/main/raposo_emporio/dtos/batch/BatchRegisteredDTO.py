from typing import Optional
from pydantic import BaseModel
from datetime import date
from entity.batch.Batch import Batch

class BatchRegisteredDTO(BaseModel):
    id: Optional[int]
    expiration_date: date
    manufacture_date: date
    quantity: int
    code: str
    product_id: int

    def __init__(self, batch: Batch):
        super().__init__(
            id=batch.id,
            expiration_date=batch.expiration_date,
            manufacture_date=batch.manufacture_date,
            quantity=batch.quantity,
            code=batch.code,
            product_id=batch.product_id
        )

    def deserialize(self):
        return {
            "id": self.id,
            "expiration_date": self.expiration_date,
            "manufacture_date": self.manufacture_date,
            "quantity": self.quantity,
            "code": self.code,
            "product_id": self.product_id
        }
