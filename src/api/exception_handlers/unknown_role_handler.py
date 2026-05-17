from fastapi import Request
from fastapi.responses import JSONResponse

from src.domain.exceptions import UnknownRoleException


async def unknown_role_exception_handler(request: Request, exc: UnknownRoleException):
    return JSONResponse(
        status_code=400,
        content={"message": exc.message},
    )
