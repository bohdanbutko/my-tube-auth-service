from src.application.commands.verify_token.command import VerifyTokenCommand
from src.domain.exceptions import InvalidCredentialsException
from src.infrastructure.services.jwt_token_service import JWTTokenService
from src.domain.value_objects import OperationResult


def verify_token_handler(command: VerifyTokenCommand) -> dict:
    token_service = JWTTokenService(secret_key="your-secret-key-here", algorithm="HS256")

    # Verify token
    payload = token_service.verify_token(command.token)
    if not payload:
        raise InvalidCredentialsException()

    # Return success result
    return OperationResult(
        success=True,
        message="Token is valid",
        data=payload
    ).model_dump()
