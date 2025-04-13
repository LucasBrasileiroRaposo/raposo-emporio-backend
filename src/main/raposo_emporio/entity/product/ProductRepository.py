from database import db
from singleton.Singleton import Singleton
from entity.product.Product import Product
from sqlalchemy import or_, orm

class ProductRepository(Singleton):

    def save(self, product: Product):
        db.session.add(product)
        db.session.commit()
        return product

    def delete(self, product_id: int):
        Product.query.filter(Product.id == product_id).delete()
        db.session.commit()

    def find_by_name_or_code(self, name: list[str], code: list[str]):
        filters = []
        if name:
            filters.append(Product.name.in_(name))
        if code:
            filters.append(Product.code.in_(code))

        return Product.query.filter(or_(*filters)).all() if filters else []

    def find_all(self):
        return Product.query.options(orm.joinedload(Product.batches)).all()

    def find_by_id(self, product_id: int):
        return Product.query.get(product_id)
