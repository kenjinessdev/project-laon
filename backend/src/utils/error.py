from fastapi.responses import JSONResponse
from typing import List, Optional


def error_response(
    status_code: int,
    detail: str,
    field: Optional[str] = None,
    message: Optional[str] = None
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "detail": detail,
            "missing_fields": None,
            "format_errors": None,
            "other_errors": (
                [{"field": field, "message": message}]
                if field and message else None
            )
        }
    )
