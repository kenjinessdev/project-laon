from pydantic import BaseModel, EmailStr, constr
from datetime import datetime, date
from typing import Optional, Literal


class AddressBase(BaseModel):
    street: Optional[str] = None
    street2: Optional[str] = None
    city: Optional[constr(max_length=50)] = None
    region: Optional[constr(max_length=50)] = None
    postal_code: Optional[constr(max_length=20)] = None
    is_primary: Optional[bool] = False


class AddressCreate(AddressBase):
    user_id: int


class Address(AddressBase):
    address_id: int
    user_id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    first_name: constr(max_length=100)
    middle_name: Optional[constr(max_length=100)] = None
    last_name: constr(max_length=100)
    suffix: Optional[constr(max_length=100)] = None
    profile_image_url: Optional[str] = None
    email: EmailStr
    password: constr(min_length=8)
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


class LoginSchema(BaseModel):
    email: EmailStr
    password: str
