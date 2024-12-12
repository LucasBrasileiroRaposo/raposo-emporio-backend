from flask import Flask, Blueprint, request, jsonify, make_response

from singleton.Singleton import Singleton
from business.user.UserService import UserService
from dtos.user.UserRegisterDTO import UserRegisterDTO
from dtos.user.UserRegisteredDTO import UserRegisteredDTO
from dtos.user.UserLoginDTO import UserLoginDTO
from dtos.user.UserUpdateDTO import UserUpdateDTO
from business.jwt.JwtService import token_required


class UserController(Singleton):

    USER__ROUTES_PREFIX = '/user'

    def __init__(self):
        self.user_service = UserService()
        self.blueprint = Blueprint('user', __name__)

    def register_routes(self):
        self.__register_routes()
        return self.blueprint

    def __register_routes(self):
        self.blueprint.add_url_rule('/signUp', 'registerUser', self.register_user, methods=['POST'])
        self.blueprint.add_url_rule('/login', 'login', self.login, methods=['POST'])
        self.blueprint.add_url_rule('/', "getUsers", self.get_users, methods=['GET'])
        self.blueprint.add_url_rule('/<id>', 'getUserById', self.get_user_by_id, methods=['GET'])
        self.blueprint.add_url_rule('/<id>', 'updateUser', self.update_user, methods=['PUT'])
        self.blueprint.add_url_rule('/<id>', 'deleteUser', self.delete_user, methods=['DELETE'])

    def register_user(self):
        try:
            data = request.get_json()
            user = UserRegisterDTO(**data)
            user_registered = self.user_service.register_user(user)
            response_user = UserRegisteredDTO(user_registered)
            return make_response(jsonify({'message': 'User created!', 'response': response_user.deserialize()}), 201)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)

    def login(self):
        try:
            data = request.get_json()
            login_data = UserLoginDTO(**data)
            token = self.user_service.login(login_data)
            return make_response(jsonify({'message': f'Your token is: {token}'}), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)

    @token_required
    def get_users(self, username):
        try:
            users = self.user_service.get_users()
            return make_response(jsonify({'message': "Success", "response": users}), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)

    @token_required
    def get_user_by_id(self, id, username):
        try:
            user = self.user_service.get_user_by_id(id, username)
            user = UserRegisteredDTO(user).deserialize()
            return make_response(jsonify({'message': user}), 200)
        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 400)

    @token_required
    def update_user(self, id, username):
        try:
            data = request.get_json()
            to_update_data = UserUpdateDTO(**data)
            updated_user = self.user_service.update_user(id, username, to_update_data)
            updated_user = UserRegisteredDTO(updated_user)
            return make_response(jsonify({'message': 'User updated', 'response': updated_user.deserialize()}), 200)
        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 400)

    @token_required
    def delete_user(self, id, username):
        try:
            self.user_service.delete_user(id, username)
            return make_response(jsonify({'message': 'User deleted'}), 200)
        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 400)
