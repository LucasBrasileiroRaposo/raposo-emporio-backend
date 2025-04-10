from singleton.Singleton import Singleton
from entity.batch.Batch import Batch
from database import db

class BatchRepository(Singleton):

    def save(self, batch: Batch):
        db.session.add(batch)
        db.session.commit()
        return batch

    def saveAll(self, batches: list[Batch]):
        db.session.add_all(batches)
        db.session.commit()
        return batches

    def delete(self, batch_id: int):
        Batch.query.filter(Batch.id == batch_id).delete()
        db.session.commit()

    def find_by_id(self, batch_id: int):
        return Batch.query.get(batch_id)

    def find_all(self):
        return Batch.query.all()

    def find_by_product_id(self, product_id: int):
        return Batch.query.filter(Batch.product_id == product_id).all()

    def find_by_code(self, code: str):
        return Batch.query.filter(Batch.code == code).one_or_none()