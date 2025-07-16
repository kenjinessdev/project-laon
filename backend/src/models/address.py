from pydantic import BaseModel, constr, StringConstraints
from typing import Optional, Any, Annotated


PostalCode = Annotated[
    str,
    StringConstraints(
        max_length=20,
        pattern=r"^\d{4,5}(-\d{4})?$"  # Accepts 4-5 digit ZIPs and ZIP+4
    )
]


class AddressBase(BaseModel):
    street: str
    street2: Optional[str] = None
    barangay: str
    city: constr(max_length=50)
    region: constr(max_length=50)
    postal_code: PostalCode
    user: Optional[Any] = None
    is_primary: bool


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
    barangay: Optional[str] = None
    city: Optional[constr(max_length=50)] = None
    region: Optional[constr(max_length=50)] = None
    postal_code: Optional[constr(max_length=20)] = None
    is_primary: Optional[bool] = False
