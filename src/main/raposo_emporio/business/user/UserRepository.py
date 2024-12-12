from singleton.Singleton import Singleton
from business.user.User import User
from database import db

class UserRepository(Singleton):

    def save(self, user: User):
        db.session.add(user)
        db.session.commit()
        return user

    def delete(self, user_id: int):
        User.query.filter(User.id == user_id).delete()
        db.session.commit()

    def find_by_username(self, username: str):
        return User.query.filter_by(username=username).one_or_none()

    def find_all(self):
        return User.query.all()

    def find_by_id(self, user_id: int):
        return User.query.get(user_id)
