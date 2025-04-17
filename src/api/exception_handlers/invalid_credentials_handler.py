from fastapi import Request
from fastapi.responses import JSONResponse

from src.domain.exceptions import InvalidCredentialsException


async def invalid_credentials_exception_handler(
    request: Request, exc: InvalidCredentialsException
):
    return JSONResponse(
        status_code=401,
        content={"message": exc.message},
    )
