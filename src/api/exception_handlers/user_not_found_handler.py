from fastapi import Request
from fastapi.responses import JSONResponse

from src.domain.exceptions import UserNotFoundException


async def user_not_found_exception_handler(
    request: Request, exc: UserNotFoundException
):
    return JSONResponse(
        status_code=404,
        content={"message": exc.message},
    )
