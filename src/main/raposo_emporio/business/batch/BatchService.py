from singleton.Singleton import Singleton
from business.user.UserService import UserService
from entity.batch.BatchRepository import BatchRepository
from entity.batch.Batch import Batch
from dtos.batch.BatchRegisterDTO import BatchRegisterDTO
from dtos.batch.BatchRegisteredDTO import BatchRegisteredDTO
from dtos.batch.BatchUpdateDTO import BatchUpdateDTO
from typing import List

class BatchService(Singleton):

    ADMIN_USER_ROLE = 'ADMIN'

    def __init__(self):
        self.user_service = UserService()
        self.batch_repository = BatchRepository()

    def register_batch(self, batches: List[BatchRegisterDTO], product_id: int, requester_id: int):
        self.user_service.check_user_permission(requester_id, [self.ADMIN_USER_ROLE])
        new_batches = []
        for batch_dto in batches:
            if self.batch_repository.find_by_code(batch_dto.code):
                raise Exception('Batch already registered with this code')

            new_batch = Batch(
                expiration_date=batch_dto.expiration_date,
                manufacture_date=batch_dto.manufacture_date,
                quantity=batch_dto.quantity,
                code=batch_dto.code,
                product_id=product_id
            )
            new_batches.append(new_batch)

        saved_batches = self.batch_repository.save_all(new_batches)
        return [BatchRegisteredDTO.from_entity(batch) for batch in saved_batches]

    def get_batches(self):
        return self.batch_repository.find_all()

    def get_batch_by_id(self, batch_id: int):
        batch = self.batch_repository.find_by_id(batch_id)
        if not batch:
            raise Exception('Batch not found')
        return BatchRegisteredDTO.from_entity(batch)

    def update_batch(self, batch_id: int, requester_id: int, batch_update: BatchUpdateDTO):
        self.user_service.check_user_permission(requester_id, [self.ADMIN_USER_ROLE])
        batch = self.batch_repository.find_by_id(batch_id)
        if not batch:
            raise Exception('Batch not found')

        if batch_update.code and self.batch_repository.find_by_code(batch_update.code):
            raise Exception('Batch code already registered')

        batch.code = (batch_update.code if batch_update.code else batch.code)
        batch.expiration_date = (batch_update.expiration_date if batch_update.expiration_date else batch.expiration_date)
        batch.manufacture_date = (batch_update.manufacture_date if batch_update.manufacture_date else batch.manufacture_date)
        batch.quantity = (batch_update.quantity if batch_update.quantity else batch.quantity)

        return self.batch_repository.save(batch)

    def delete_batch(self, batch_id: int, requester_id:int):
        self.user_service.check_user_permission(requester_id, [self.ADMIN_USER_ROLE])
        batch = self.batch_repository.find_by_id(batch_id)
        if not batch:
            raise Exception('Batch not found')
        return self.batch_repository.delete(batch_id)

