from pydantic import BaseModel, constr
from typing import Optional, Any


class AddressBase(BaseModel):
    street: str
    street2: Optional[str] = None
    city: constr(max_length=50)
    region: constr(max_length=50)
    postal_code: constr(max_length=20)
    is_primary: bool = False
    user: Optional[Any] = None


class AddressCreate(AddressBase):
    user_id: int


class Address(AddressBase):
    id: int
    user_id: str

    class Config:
        from_attributes = True


class AddressIn(AddressBase):
    class Config:
        from_attributes = True


class AddressUpdate(BaseModel):
    street: Optional[str] = None
    street2: Optional[str] = None
    city: Optional[constr(max_length=50)] = None
    region: Optional[constr(max_length=50)] = None
    postal_code: Optional[constr(max_length=20)] = None
    is_primary: Optional[bool] = False
