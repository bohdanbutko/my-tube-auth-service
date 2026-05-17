from uuid import uuid4

import pytest

from src.application.commands import (
    ProvisionIdentityCommand,
    provision_identity_handler,
)
from src.application.commands.provision_identity import ChannelAccessAssignmentCommand
from src.domain.exceptions import IdentityAlreadyExistsException, UnknownRoleException
from src.infrastructure.repositories import InMemoryIdentityRepository


@pytest.fixture(autouse=True)
def clear_repository():
    InMemoryIdentityRepository().clear()


def test_provision_identity_success():
    channel_id = uuid4()
    command = ProvisionIdentityCommand(
        subject_id=uuid4(),
        email="test@mail.com",
        password="password",
        channel_accesses=[
            ChannelAccessAssignmentCommand(
                channel_id=channel_id, role="channel_viewer"
            ),
        ],
    )

    result = provision_identity_handler(command)

    assert result["success"] is True
    assert result["message"] == "Identity provisioned successfully"


def test_provision_identity_duplicate_email():
    channel_id = uuid4()
    subject_id = uuid4()
    command = ProvisionIdentityCommand(
        subject_id=subject_id,
        email="test@mail.com",
        password="password",
        channel_accesses=[
            ChannelAccessAssignmentCommand(
                channel_id=channel_id, role="channel_viewer"
            ),
        ],
    )
    provision_identity_handler(command)

    with pytest.raises(IdentityAlreadyExistsException):
        provision_identity_handler(
            ProvisionIdentityCommand(
                subject_id=uuid4(),
                email="test@mail.com",
                password="password",
                channel_accesses=[
                    ChannelAccessAssignmentCommand(
                        channel_id=uuid4(), role="channel_viewer"
                    ),
                ],
            )
        )


def test_provision_identity_unknown_role():
    with pytest.raises(UnknownRoleException):
        provision_identity_handler(
            ProvisionIdentityCommand(
                subject_id=uuid4(),
                email="test@mail.com",
                password="password",
                channel_accesses=[
                    ChannelAccessAssignmentCommand(
                        channel_id=uuid4(), role="missing-role"
                    ),
                ],
            )
        )
