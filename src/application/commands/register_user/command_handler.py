from src.application.commands.register_user.command import RegisterUserCommand
from src.domain.aggregates.user_aggregate import UserAggregate
from src.domain.value_objects import Password, Email
from src.infrastructure.repositories.in_memory_user_repository import InMemoryUserRepository
from src.infrastructure.services.bcrypt_password_hashing_service import BcryptPasswordHashingService


def register_user_handler(command: RegisterUserCommand) -> dict:
    # Initialize services and repositories
    repository = InMemoryUserRepository()
    password_service = BcryptPasswordHashingService()

    # Set up aggregate with services
    aggregate = UserAggregate(password_service=password_service)

    # Convert command parameters to value objects
    email = Email(email=command.email)  # Updated to use named parameter
    password = Password(password=command.password)

    # Execute domain logic
    result = aggregate.register_user(email, password)

    # If successful, persist the user
    if result.success and aggregate.user:
        repository.save(aggregate.user)

    return result.model_dump()
