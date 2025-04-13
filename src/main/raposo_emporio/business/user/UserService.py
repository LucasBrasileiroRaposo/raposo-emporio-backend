import datetime
import os
import bcrypt
import jwt
from typing import List
from singleton.Singleton import Singleton
from entity.user.UserRepository import UserRepository
from entity.user.User import User
from dtos.user.UserRegisterDTO import UserRegisterDTO
from dtos.user.UserRegisteredDTO import UserRegisteredDTO
from dtos.user.UserUpdateDTO import UserUpdateDTO
from dtos.user.UserLoginDTO import UserLoginDTO

class UserService(Singleton):

    def __init__(self):
        self.user_repository = UserRepository()

    def register_user(self, user:UserRegisterDTO):

        if self.user_repository.find_by_username(user.username):
            raise Exception('Username already registered')

        encrypted_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        newUser = User(
            username=user.username,
            password=encrypted_password,
            first_name=user.first_name,
            last_name=user.last_name,
            birth_date=user.birth_date,
            email=user.email,
            document=user.document,
            phone=user.phone,
            address=user.address,
            state=user.state,
            city=user.city,
            role=user.role
        )

        return self.user_repository.save(newUser)

    def login(self, user:UserLoginDTO):

        user_found = self.user_repository.find_by_username(user.username)

        if not user_found:
            raise Exception('User not found')

        if not bcrypt.checkpw(user.password.encode('utf-8'), user_found.password.encode('utf-8')):
            raise Exception('Invalid password')

        payload = {
            "id": user_found.id,
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
        }

        secret_key = os.environ.get("SECRET_KEY")
        token = jwt.encode(payload, secret_key, algorithm="HS256")

        return {"token":token, "id": user_found.id}

    def get_users(self, requester_id):

        requester_role = self.__find_requester_role(requester_id)
        user_dtos = []

        if requester_role != 'ADMIN':
            users = self.user_repository.find_all_by_role(requester_role)
        else:
            users = self.user_repository.find_all()

        for user in users:
            user_dtos.append(UserRegisteredDTO(user).deserialize())

        return user_dtos

    def get_user_by_id(self, user_id, requester_id):

        user_found = self.user_repository.find_by_id(user_id)

        if not user_found:
            raise Exception('User not found')

        requester_role = self.__find_requester_role(requester_id)

        if user_found.id != requester_id and requester_role != 'ADMIN':
            raise Exception('Unauthorized, you can only see your own data')

        user_found = UserRegisteredDTO(user_found)
        return user_found

    def update_user(self, user_id, requester_id, user:UserUpdateDTO):

        user_found = self.user_repository.find_by_id(user_id)

        if not user_found:
            raise Exception('User not found')

        requester_role = self.__find_requester_role(requester_id)

        if user_found.id != requester_id:
            raise Exception('Unauthorized, you can only update your own data')

        user_found.username = (user.username if user.username else user_found.username)
        user_found.password = (bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8') if user.password else user_found.password)
        user_found.first_name = (user.first_name if user.first_name else user_found.first_name)
        user_found.last_name = (user.last_name if user.last_name else user_found.last_name)
        user_found.birth_date = (user.birth_date if user.birth_date else user_found.birth_date)
        user_found.email = (user.email if user.email else user_found.email)
        user_found.document = (user.document.upper() if user.document else user_found.document)
        user_found.phone = (user.phone if user.phone else user_found.phone)
        user_found.address = (user.address if user.address else user_found.address)
        user_found.state = (user.state.upper() if user.state else user_found.state)
        user_found.city = (user.city.upper() if user.city else user_found.city)
        user_found.role = (user.role if user.role and requester_role != "USER" else user_found.role)

        return self.user_repository.save(user_found)

    def delete_user(self, user_id, requester_id):

        user_found = self.user_repository.find_by_id(user_id)

        if not user_found:
            raise Exception('User not found')

        requester_role = self.__find_requester_role(requester_id)

        if user_found.id != requester_id and requester_role != 'ADMIN':
            raise Exception('Unauthorized, you can delete see your own account')

        return self.user_repository.delete(user_id)

    def check_user_permission(self, requester_id, authorized_roles: List[str]):
        requester_role = self.__find_requester_role(requester_id)

        if requester_role not in authorized_roles:
            raise Exception('Unauthorized, you do not have permission to perform this action')

    def __find_requester_role(self, id):
        requester = self.user_repository.find_by_id(id)
        return requester.role.name