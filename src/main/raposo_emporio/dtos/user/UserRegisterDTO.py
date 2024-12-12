from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import date, timedelta
from business.user.enum.RoleEnum import RoleEnum


class UserRegisterDTO(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    first_name: str = Field(..., min_length=3, max_length=50)
    last_name: str = Field(..., min_length=3, max_length=50)
    birth_date: date
    email: EmailStr
    password: str = Field(..., min_length=8)
    document: str = Field(..., min_length=11, max_length=14)
    phone: str = Field(..., min_length=10, max_length=15)
    country: str = Field(..., min_length=3, max_length=50)
    state: Optional[str] = Field(None, min_length=2, max_length=2)
    city: Optional[str] = Field(None, min_length=3, max_length=50)
    role: RoleEnum

    @field_validator("birth_date")
    def validate_birth_date(cls, value):
        today = date.today()
        if value >= today:
            raise ValueError("Birth date must be in the past.")
        if value.year < 1900:
            raise ValueError("Birth date cannot be earlier than 1900.")
        if today - value < timedelta(days=15 * 365):
            raise ValueError("User must be at least 15 years old.")
        return value

    @field_validator("role")
    def validate_role(cls, value):
        if value not in RoleEnum:
            raise ValueError(f"Invalid role, valid roles are {', '.join([role.name for role in RoleEnum])}.")
        return value