from pydantic import BaseModel, Field
from typing import Optional


class OrderQueryParams(BaseModel):
    search: Optional[str] = Field(default="", description="Search by status")
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=10, ge=1)
