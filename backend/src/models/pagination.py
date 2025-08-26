from pydantic import BaseModel
from typing import Optional, List


class Pagination(BaseModel):
    skip: int = 0
    take: int = 10
    total: Optional[int] = None
