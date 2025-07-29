from pydantic import BaseModel, Field
from typing import Optional


class OrderQueryParams(BaseModel):
    search: Optional[str] = Field(
        default="", description="Search by name etc.")
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=10, ge=1)


class OrderQueryParamsStatus(OrderQueryParams):
    status: Optional[str] = Field(default="", description="Search by status")
