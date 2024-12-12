from singleton.Singleton import Singleton
from business.user.UserRepository import UserRepository
from dtos.user.UserRegisterDTO import UserRegisterDTO
from dtos.user.UserRegisteredDTO import UserRegisteredDTO
from dtos.user.UserUpdateDTO import UserUpdateDTO
from dtos.user.UserLoginDTO import UserLoginDTO
from business.user.User import User
import bcrypt
import jwt
import os
import datetime

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
            country=user.country,
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
            "username": user.username,
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
        }

        secret_key = os.environ.get("SECRET_KEY")
        token = jwt.encode(payload, secret_key, algorithm="HS256")

        return token

    def get_users(self):

        user_dtos = []
        users = self.user_repository.find_all()
        for user in users:
            user_dtos.append(UserRegisteredDTO(user).deserialize())

        return user_dtos

    def get_user_by_id(self, user_id, username):

        user_found = self.user_repository.find_by_id(user_id)

        if not user_found:
            raise Exception('User not found')

        requester_role = self.__find_requester_role(username)

        if user_found.username != username and requester_role != 'ADMIN':
            raise Exception('Unauthorized, you can only see your own data')

        user_found = UserRegisteredDTO(user_found)
        return user_found

    def update_user(self, user_id, username, user:UserUpdateDTO):

        user_found = self.user_repository.find_by_id(user_id)

        if not user_found:
            raise Exception('User not found')

        requester_role = self.__find_requester_role(username)

        if user_found.username != username and requester_role != 'ADMIN':
            raise Exception('Unauthorized, you can only update your own data')

        user_found.username = (user.username if user.username else user_found.username)
        user_found.first_name = (user.first_name if user.first_name else user_found.first_name)
        user_found.last_name = (user.last_name if user.last_name else user_found.last_name)
        user_found.birth_date = (user.birth_date if user.birth_date else user_found.birth_date)
        user_found.email = (user.email if user.email else user_found.email)
        user_found.document = (user.document if user.document else user_found.document)
        user_found.phone = (user.phone if user.phone else user_found.phone)
        user_found.country = (user.country if user.country else user_found.country)
        user_found.state = (user.state if user.state else user_found.state)
        user_found.city = (user.city if user.city else user_found.city)
        user_found.role = (user.role if user.role and requester_role != "USER" else user_found.role)

        return self.user_repository.save(user_found)

    def delete_user(self, user_id, username):

        user_found = self.user_repository.find_by_id(user_id)

        if not user_found:
            raise Exception('User not found')

        requester_role = self.__find_requester_role(username)

        if user_found.username != username and requester_role != 'ADMIN':
            raise Exception('Unauthorized, you can delete see your own account')

        return self.user_repository.delete(user_id)

    def __find_requester_role(self, username):
        requester = self.user_repository.find_by_username(username)
        return requester.role.name