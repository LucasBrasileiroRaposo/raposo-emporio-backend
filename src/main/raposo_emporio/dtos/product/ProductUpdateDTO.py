from pydantic import BaseModel, Field
from typing import Optional
from entity.product.category_enum.CategoryEnum import CategoryEnum

class ProductUpdateDTO(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1, max_length=255)
    code: Optional[int] = Field(None, ge=0)
    base_price: Optional[float] = Field(None, gt=0)
    image_url: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = Field(None)
    category: Optional[CategoryEnum] = Field(None)
