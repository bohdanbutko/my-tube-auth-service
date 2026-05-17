from datetime import timedelta

from src.application.commands.login.command import LoginCommand
from src.domain.exceptions import InvalidCredentialsException
from src.domain.value_objects import Password
from src.infrastructure.repositories import InMemoryIdentityRepository
from src.infrastructure.services import BcryptPasswordHashingService, JWTTokenService


def login_handler(command: LoginCommand) -> dict:
    repository = InMemoryIdentityRepository()
    password_service = BcryptPasswordHashingService()
    token_service = JWTTokenService.from_env()

    identity = repository.find_by_email(str(command.email))
    if not identity:
        raise InvalidCredentialsException()

    password = Password(value=command.password)
    auth_result = identity.authenticate(password, password_service)
    if not auth_result.success:
        raise InvalidCredentialsException()

    token = token_service.create_access_token(
        identity=identity, expires_delta=timedelta(minutes=30)
    )
    return token.to_dict()
