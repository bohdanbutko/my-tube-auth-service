from datetime import timedelta
from src.application.commands.login.command import LoginCommand
from src.domain.aggregates.user_aggregate import UserAggregate
from src.domain.value_objects import Password, Email, OperationResult
from src.domain.exceptions import InvalidCredentialsException
from src.infrastructure.repositories.in_memory_user_repository import InMemoryUserRepository
from src.infrastructure.services.bcrypt_password_hashing_service import BcryptPasswordHashingService
from src.infrastructure.services.jwt_token_service import JWTTokenService


def login_handler(command: LoginCommand) -> dict:
    # Initialize services and repositories
    repository = InMemoryUserRepository()
    password_service = BcryptPasswordHashingService()
    token_service = JWTTokenService(secret_key="your-secret-key-here", algorithm="HS256")

    # Find user by email
    user = repository.find_by_email(command.email)
    if not user:
        raise InvalidCredentialsException()

    # Set up aggregate with user and password service
    aggregate = UserAggregate(user=user, password_service=password_service)

    # Create password value object
    password = Password(password=command.password)

    # Authenticate user
    auth_result = aggregate.authenticate(password)
    if not auth_result.success:
        raise InvalidCredentialsException()

    # Generate JWT token
    token = token_service.create_access_token(
        user=user, expires_delta=timedelta(minutes=30)
    )

    # Return token
    return token.model_dump()
