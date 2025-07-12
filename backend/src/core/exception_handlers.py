from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    missing_fields = []
    for error in exc.errors():
        if error["type"] == "missing":
            field = ".".join(str(loc) for loc in error["loc"][1:])
            missing_fields.append(field)

    return JSONResponse(
        status_code=422,
        content={
            "detail": "Missing required fields",
            "missing_fields": missing_fields
        }
    )
