from database import db
from sqlalchemy import Integer, String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from entity.product.category_enum.CategoryEnum import CategoryEnum
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from entity.batch.Batch import Batch

class Product(db.Model):

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    category: Mapped[CategoryEnum] = mapped_column(Enum(CategoryEnum), nullable=False)
    base_price: Mapped[float] = mapped_column(nullable=False)
    image_url: Mapped[str] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    batches: Mapped[List["Batch"]]= relationship("Batch", back_populates="product", cascade="all, delete-orphan", passive_deletes=True)

    def __init__(self, name, description, code, category, base_price, image_url, is_active):
        self.name = name
        self.description = description
        self.code = code
        self.category = category
        self.base_price = base_price
        self.image_url = image_url
        self.isActive = is_active

