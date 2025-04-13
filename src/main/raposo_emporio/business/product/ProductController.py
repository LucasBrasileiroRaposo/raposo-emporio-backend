from flask import Blueprint, request, jsonify, make_response

from singleton.Singleton import Singleton
from business.jwt.JwtService import token_required
from business.product.ProductService import ProductService
from dtos.product.ProductRegisterDTO import ProductRegisterDTO
from dtos.product.ProductRegisteredDTO import ProductRegisteredDTO
from dtos.product.ProductUpdateDTO import ProductUpdateDTO

class ProductController(Singleton):
    PRODUCT__ROUTES_PREFIX = '/product'

    def __init__(self):
        self.product_service = ProductService()
        self.blueprint = Blueprint('product', __name__)

    def register_routes(self):
        self.__register_routes()
        return self.blueprint

    def __register_routes(self):
        self.blueprint.add_url_rule('/', 'registerProduct', self.register_product, methods=['POST'])
        self.blueprint.add_url_rule('/', "getProducts", self.get_products, methods=['GET'])
        self.blueprint.add_url_rule('/<id>', 'getProductById', self.get_product_by_id, methods=['GET'])
        self.blueprint.add_url_rule('/<id>', 'updateProduct', self.update_product, methods=['PUT'])
        self.blueprint.add_url_rule('/<id>', 'deleteProduct', self.delete_product, methods=['DELETE'])

    @token_required
    def register_product(self, requester_id):
        try:
            data = request.get_json()
            product_data = ProductRegisterDTO(**data)
            created_product = self.product_service.register_product(product_data, requester_id)
            response_product = ProductRegisteredDTO(created_product)
            return make_response(jsonify({'message': 'Product created!', 'response': response_product.deserialize()}), 201)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)

    def get_product_by_id(self, id):
        try:
            product = self.product_service.get_product_by_id(id)
            product = ProductRegisteredDTO(product).deserialize()
            return make_response(jsonify({'message': product}), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)

    def get_products(self):
        try:
            products = self.product_service.get_products()
            return make_response(jsonify({'message': "Success", "response": products}), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)

    @token_required
    def update_product(self, id, requester_id):
        try:
            data = request.get_json()
            to_update_data = ProductUpdateDTO(**data)
            updated_product = self.product_service.update_product(id, to_update_data, requester_id)
            updated_product = ProductRegisteredDTO(updated_product)
            return make_response(jsonify({'message': 'Product updated', 'response': updated_product.deserialize()}), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)

    @token_required
    def delete_product(self, id, requester_id):
        try:
            self.product_service.delete_product(id, requester_id)
            return make_response(jsonify({'message': 'Product deleted'}), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)