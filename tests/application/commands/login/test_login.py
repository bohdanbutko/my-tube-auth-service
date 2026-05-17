from uuid import uuid4

import pytest

from src.application.commands import (
    LoginCommand,
    ProvisionIdentityCommand,
    login_handler,
    provision_identity_handler,
)
from src.application.commands.provision_identity import ChannelAccessAssignmentCommand
from src.domain.exceptions import InvalidCredentialsException
from src.infrastructure.repositories import InMemoryIdentityRepository


@pytest.fixture(autouse=True)
def clear_repository():
    InMemoryIdentityRepository().clear()


def test_login_success_after_identity_provisioning():
    channel_id = uuid4()
    provision_identity_handler(
        ProvisionIdentityCommand(
            subject_id=uuid4(),
            email="test@mail.com",
            password="password",
            channel_accesses=[
                ChannelAccessAssignmentCommand(
                    channel_id=channel_id, role="channel_viewer"
                ),
            ],
        )
    )

    result = login_handler(LoginCommand(email="test@mail.com", password="password"))

    assert result["access_token"]
    assert result["token_type"] == "bearer"


def test_login_invalid_credentials():
    channel_id = uuid4()
    provision_identity_handler(
        ProvisionIdentityCommand(
            subject_id=uuid4(),
            email="test@mail.com",
            password="password",
            channel_accesses=[
                ChannelAccessAssignmentCommand(
                    channel_id=channel_id, role="channel_viewer"
                ),
            ],
        )
    )

    with pytest.raises(InvalidCredentialsException):
        login_handler(LoginCommand(email="test@mail.com", password="wrong-password"))
