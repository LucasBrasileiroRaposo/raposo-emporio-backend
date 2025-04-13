from typing import List, Optional
from pydantic import BaseModel, Field
from entity.product.category_enum.CategoryEnum import CategoryEnum
from dtos.batch.BatchRegisterDTO import BatchRegisterDTO

class ProductRegisterDTO(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=255)
    code: int = Field(..., ge=0)
    category: CategoryEnum
    base_price: float = Field(..., gt=0)
    image_url: Optional[str] = Field(None, max_length=255)
    is_active: bool = Field(default=True)
    batches: Optional[List[BatchRegisterDTO]] = Field(default_factory=list)