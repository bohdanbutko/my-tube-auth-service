from fastapi import Request
from fastapi.responses import JSONResponse

from src.domain.exceptions import IdentityAlreadyExistsException


async def identity_already_exists_exception_handler(
    request: Request, exc: IdentityAlreadyExistsException
):
    return JSONResponse(
        status_code=409,
        content={"message": exc.message},
    )
