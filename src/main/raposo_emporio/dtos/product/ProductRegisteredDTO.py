from typing import Optional, List
from pydantic import BaseModel
from entity.product.category_enum.CategoryEnum import CategoryEnum
from entity.product.Product import Product
from dtos.batch.BatchRegisteredDTO import BatchRegisteredDTO

class ProductRegisteredDTO(BaseModel):
    id: Optional[int]
    name: str
    description: str
    code: int
    category: CategoryEnum
    base_price: float
    image_url: Optional[str]
    is_active: bool
    batches: Optional[List[BatchRegisteredDTO]] = []

    def __init__(self, product: Product):
        super().__init__(
            id=product.id,
            name=product.name,
            description=product.description,
            code=product.code,
            category=product.category,
            base_price=product.base_price,
            image_url=product.image_url,
            is_active=product.is_active,
            batches=[BatchRegisteredDTO.from_entity(batch).deserialize() for batch in product.batches] if product.batches else []
        )

    def deserialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "code": self.code,
            "category": self.category.name,
            "base_price": self.base_price,
            "image_url": self.image_url,
            "is_active": self.is_active,
            "batches": [batch.deserialize() for batch in self.batches]
        }
