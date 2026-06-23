from typing import cast

from fastapi import FastAPI
from starlette.types import ExceptionHandler

from src.api.exception_handlers import (
    identity_already_exists_exception_handler,
    invalid_credentials_exception_handler,
    unknown_role_exception_handler,
)
from src.api.routes import auth_router
from src.domain.exceptions import (
    IdentityAlreadyExistsException,
    InvalidCredentialsException,
    UnknownRoleException,
)

app = FastAPI()

app.add_exception_handler(
    IdentityAlreadyExistsException,
    cast(ExceptionHandler, identity_already_exists_exception_handler),
)
app.add_exception_handler(
    InvalidCredentialsException,
    cast(ExceptionHandler, invalid_credentials_exception_handler),
)
app.add_exception_handler(
    UnknownRoleException,
    cast(ExceptionHandler, unknown_role_exception_handler),
)

app.include_router(router=auth_router, prefix="/api/v1")
