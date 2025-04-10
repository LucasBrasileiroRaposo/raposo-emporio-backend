from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional
from entity.user.enum.RoleEnum import RoleEnum
from entity.user.User import User

class UserRegisteredDTO(BaseModel):
    id: Optional[int]
    username: str
    first_name: str
    last_name: str
    birth_date: date
    email: EmailStr
    document: str
    phone: str
    country: str
    state: Optional[str]
    city: Optional[str]
    role: RoleEnum

    def __init__(self, user: User):
        super().__init__(
            id=user.id,
            username=user.username,
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

    def deserialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birth_date": self.birth_date,
            "email": self.email,
            "document": self.document,
            "phone": self.phone,
            "country": self.country,
            "state": self.state,
            "city": self.city,
            "role": self.role.name
        }