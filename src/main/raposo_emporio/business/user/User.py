from database import db
from sqlalchemy import Integer, String, Enum, Date
from sqlalchemy.orm import Mapped, mapped_column
import datetime
from business.user.enum.RoleEnum import RoleEnum
from typing import Optional


class User(db.Model):

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False )
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    birth_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    email: Mapped[str] = mapped_column(String(80), nullable=False)
    document: Mapped[str] = mapped_column(String(14), nullable=False)
    phone: Mapped[str] = mapped_column(String(15) ,nullable=False)
    country: Mapped[str] = mapped_column(nullable=False)
    state: Mapped[Optional[str]] = mapped_column(String(2))
    city: Mapped[Optional[str]] = mapped_column(String(50))
    role: Mapped[RoleEnum] = mapped_column(Enum(RoleEnum), nullable=False)

    def __init__(self,
                 username,
                 password,
                 first_name,
                 last_name,
                 birth_date,
                 email,
                 document,
                 phone,
                 country,
                 state,
                 city,
                 role):

        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.email = email
        self.document = document
        self.phone = phone
        self.country = country
        self.state = state
        self.city = city
        self.role = role