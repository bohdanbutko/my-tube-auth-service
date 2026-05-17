from fastapi import FastAPI

from src.api.exception_handlers import (
    invalid_credentials_exception_handler,
    user_not_found_exception_handler,
)
from src.api.routes import auth_router
from src.domain.exceptions import InvalidCredentialsException, UserNotFoundException

app = FastAPI()

app.add_exception_handler(UserNotFoundException, user_not_found_exception_handler)
app.add_exception_handler(
    InvalidCredentialsException, invalid_credentials_exception_handler
)

app.include_router(router=auth_router, prefix="/api/v1")
