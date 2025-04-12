import datetime
from database import db
from sqlalchemy import Integer, String, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entity.product.Product import Product

class Batch(db.Model):

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    expiration_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    manufacture_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('product.id', ondelete='CASCADE'), nullable=False)
    product: Mapped["Product"] =  relationship("Product", back_populates="batches")
