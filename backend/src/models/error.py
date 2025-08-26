from pydantic import BaseModel
from typing import Optional, List


class FormatError(BaseModel):
    field: str
    message: str


class OtherError(BaseModel):
    field: str
    message: str


class ErrorResponse(BaseModel):
    detail: str
    missing_fields: Optional[List[str]] = None
    format_errors: Optional[List[FormatError]] = None
    other_errors: Optional[List[OtherError]] = None


class ValidationErrorResponse(ErrorResponse):
    detail: str = "Validation failed"


class BadRequestErrorResponse(ErrorResponse):
    detail: str = "Bad request"


class NotFoundErrorResponse(ErrorResponse):
    detail: str = "Resource not found"
