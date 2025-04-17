from fastapi import FastAPI

from src.api.routes import auth_router
from src.api.exception_handlers import (
    user_not_found_exception_handler,
    invalid_credentials_exception_handler,
)
from src.domain.exceptions import UserNotFoundException, InvalidCredentialsException

app = FastAPI()

app.add_exception_handler(UserNotFoundException, user_not_found_exception_handler)
app.add_exception_handler(
    InvalidCredentialsException, invalid_credentials_exception_handler
)

app.include_router(router=auth_router, prefix="/api/v1")
