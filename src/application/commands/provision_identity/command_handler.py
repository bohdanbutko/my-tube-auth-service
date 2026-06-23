from src.application.commands.provision_identity.command import ProvisionIdentityCommand
from src.domain.entities import Identity
from src.domain.exceptions import IdentityAlreadyExistsException, UnknownRoleException
from src.domain.policies import RoleCatalog
from src.domain.value_objects import (
    ChannelAccess,
    Email,
    OperationResult,
    Password,
    Role,
)
from src.infrastructure.repositories import get_identity_repository
from src.infrastructure.services import BcryptPasswordHashingService


def provision_identity_handler(command: ProvisionIdentityCommand) -> dict:
    repository = get_identity_repository()
    if repository.find_by_email(str(command.email)):
        raise IdentityAlreadyExistsException(str(command.email))

    if repository.find_by_subject_id(command.subject_id):
        raise IdentityAlreadyExistsException(str(command.email))

    password_service = BcryptPasswordHashingService()

    email = Email(email=command.email)
    password = Password(value=command.password)
    channel_accesses = _resolve_channel_accesses(command.channel_accesses)
    identity = Identity.provision(
        subject_id=command.subject_id,
        email=email,
        password=password,
        channel_accesses=channel_accesses,
        password_service=password_service,
    )
    repository.save(identity)
    result = OperationResult(
        success=True,
        message="Identity provisioned successfully",
        data={"subject_id": str(identity.subject_id)},
    )

    return result.to_dict()


def _resolve_channel_accesses(
    assignments: list,
) -> list[ChannelAccess]:
    channel_accesses: list[ChannelAccess] = []
    seen_channel_ids: set = set()
    for assignment in assignments:
        if assignment.channel_id in seen_channel_ids:
            continue

        role = _resolve_role(assignment.role)
        if not role:
            raise UnknownRoleException(assignment.role)
        channel_accesses.append(
            ChannelAccess(channel_id=assignment.channel_id, role=role)
        )
        seen_channel_ids.add(assignment.channel_id)

    return channel_accesses


def _resolve_role(role_name: str) -> Role | None:
    return RoleCatalog.find_by_name(role_name)
