from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
import re
from src.models.error import ValidationErrorResponse
from src.models.error import BadRequestErrorResponse


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    missing_fields = []
    format_errors = []
    other_errors = []

    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"][1:])
        msg = error["msg"].lower()

        # Catch missing required fields
        if "field required" in msg:
            missing_fields.append(field)

        # Catch format-related issues (like regex validation)
        elif re.search(r"(should match pattern|regex|format)", msg):
            format_errors.append({
                "field": field,
                "message": error["msg"]
            })

        # All other types of validation errors
        else:
            other_errors.append({
                "field": field,
                "message": error["msg"]
            })

    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation failed",
            "missing_fields": missing_fields or None,
            "format_errors": format_errors or None,
            "other_errors": other_errors or None
        }
    )


async def http_exception_handler(request: Request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )
