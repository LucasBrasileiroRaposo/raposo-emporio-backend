from flask import Blueprint, request, jsonify, make_response

from singleton.Singleton import Singleton
from business.jwt.JwtService import token_required
from business.batch.BatchService import BatchService
from dtos.batch.BatchRegisterDTO import BatchRegisterDTO
from dtos.batch.BatchRegisteredDTO import BatchRegisteredDTO
from dtos.batch.BatchUpdateDTO import BatchUpdateDTO

class BatchController(Singleton):
    BATCH__ROUTES_PREFIX = '/batch'

    def __init__(self):
        self.batch_service = BatchService()
        self.blueprint = Blueprint('batch', __name__)

    def register_routes(self):
        self.__register_routes()
        return self.blueprint

    def __register_routes(self):
        self.blueprint.add_url_rule('/', 'registerBatch', self.register_batch, methods=['POST'])
        self.blueprint.add_url_rule('/', 'getBatches', self.get_batches, methods=['GET'])
        self.blueprint.add_url_rule('/<id>', 'getBatchById', self.get_batch_by_id, methods=['GET'])
        self.blueprint.add_url_rule('/<id>', 'updateBatch', self.update_batch, methods=['PUT'])
        self.blueprint.add_url_rule('/<id>', 'deleteBatch', self.delete_batch, methods=['DELETE'])

    @token_required
    def register_batch(self, requester_id):
        try:
            data = request.get_json()
            batch_data = BatchRegisterDTO(**data)
            created_batch = self.batch_service.register_single_batch(batch_data, requester_id)
            response_batch = BatchRegisteredDTO(created_batch)
            return make_response(jsonify({'message': 'Batch created!', 'response': response_batch.deserialize()}), 201)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)

    def get_batch_by_id(self, id):
        try:
            batch = self.batch_service.get_batch_by_id(id)
            response_batch = BatchRegisteredDTO(batch).deserialize()
            return make_response(jsonify({'message': response_batch}), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)

    def get_batches(self):
        try:
            batches = self.batch_service.get_batches()
            response = [BatchRegisteredDTO(batch).deserialize() for batch in batches]
            return make_response(jsonify({'message': 'Success', 'response': response}), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)

    @token_required
    def update_batch(self, id, requester_id):
        try:
            data = request.get_json()
            to_update_data = BatchUpdateDTO(**data)
            updated_batch = self.batch_service.update_batch(id, requester_id, to_update_data)
            response_batch = BatchRegisteredDTO(updated_batch).deserialize()
            return make_response(jsonify({'message': 'Batch updated', 'response': response_batch}), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)

    @token_required
    def delete_batch(self, id, requester_id):
        try:
            self.batch_service.delete_batch(id, requester_id)
            return make_response(jsonify({'message': 'Batch deleted'}), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)
