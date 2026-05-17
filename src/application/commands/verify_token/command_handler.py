from src.application.commands.verify_token.command import VerifyTokenCommand
from src.domain.exceptions import InvalidCredentialsException
from src.domain.value_objects import OperationResult
from src.infrastructure.services import JWTTokenService


def verify_token_handler(command: VerifyTokenCommand) -> dict:
    token_service = JWTTokenService.from_env()

    payload = token_service.verify_token(command.token)
    if not payload:
        raise InvalidCredentialsException()

    return OperationResult(
        success=True, message="Token is valid", data=payload
    ).to_dict()
