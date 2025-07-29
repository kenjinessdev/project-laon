from pydantic import BaseModel, EmailStr, constr, HttpUrl
from datetime import datetime, date
from typing import Optional, Literal
from src.models.address import Address


class UserBase(BaseModel):
    first_name: constr(max_length=100)
    middle_name: Optional[constr(max_length=100)] = None
    last_name: constr(max_length=100)
    suffix: Optional[constr(max_length=100)] = None
    profile_image_url: Optional[str] = None
    email: EmailStr
    password: constr(min_length=6)
    phone_number: str
    # You may use Literal for stricter values
    gender: Optional[constr(max_length=50)] = None
    birthday: date
    role: Literal['farmer', 'customer']


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: str
    created_at: datetime
    addresses: Optional[list[Address]] = []

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    suffix: Optional[str] = None
    profile_image_url: Optional[HttpUrl] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    gender: Optional[str] = None
    birthday: Optional[date] = None


class UserEmailUpdate(BaseModel):
    email: EmailStr


class PasswordChangeRequest(BaseModel):
    current_password: constr(min_length=6)
    new_password: constr(min_length=6)


class LoginSchema(BaseModel):
    email: EmailStr
    password: str
