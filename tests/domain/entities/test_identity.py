import pytest
from uuid import uuid4

from src.domain.entities import Identity
from src.domain.value_objects import ChannelAccess, Email, Password, Permission, Role


@pytest.fixture
def mock_password_service(mocker):
    mock_service = mocker.Mock()
    mock_service.hash_password.return_value = "mocked_hashed_password"
    mock_service.verify_password.side_effect = (
        lambda plain, hashed: plain == "correct_password"
    )
    return mock_service


@pytest.fixture
def user_role():
    return Role(
        name="channel_viewer",
        permissions=[Permission(name="channel:view", description="View channel data")],
    )


@pytest.fixture
def admin_role():
    return Role(
        name="channel_manager",
        permissions=[
            Permission(name="channel:view", description="View channel data"),
            Permission(name="video:publish", description="Publish content"),
        ],
    )


def test_identity_creation(user_role):
    subject_id = uuid4()
    channel_id = uuid4()
    email = Email(email="test@example.com")
    identity = Identity(
        subject_id=subject_id,
        email=email,
        hashed_password="hashed_password_123",
        channel_accesses=[ChannelAccess(channel_id=channel_id, role=user_role)],
    )

    assert identity.subject_id == subject_id
    assert identity.email == email
    assert identity.hashed_password == "hashed_password_123"
    assert identity.channel_accesses == [
        ChannelAccess(channel_id=channel_id, role=user_role)
    ]
    assert identity.channel_claims() == [
        {
            "channel_id": str(channel_id),
            "role": "channel_viewer",
            "permissions": ["channel:view"],
        }
    ]


def test_provision_identity(user_role, mock_password_service):
    subject_id = uuid4()
    channel_id = uuid4()

    identity = Identity.provision(
        subject_id=subject_id,
        email=Email(email="test@example.com"),
        password=Password(value="secure_password"),
        channel_accesses=[ChannelAccess(channel_id=channel_id, role=user_role)],
        password_service=mock_password_service,
    )

    assert identity.subject_id == subject_id
    assert identity.hashed_password == "mocked_hashed_password"
    assert identity.channel_accesses == [
        ChannelAccess(channel_id=channel_id, role=user_role)
    ]
    mock_password_service.hash_password.assert_called_once_with("secure_password")


def test_check_password(mock_password_service):
    identity = Identity(
        subject_id=uuid4(),
        email=Email(email="test@example.com"),
        hashed_password="hashed_password",
        channel_accesses=[],
    )

    assert identity.check_password(mock_password_service, "correct_password") is True
    assert identity.check_password(mock_password_service, "wrong_password") is False

    mock_password_service.verify_password.assert_any_call(
        "correct_password", "hashed_password"
    )
    mock_password_service.verify_password.assert_any_call(
        "wrong_password", "hashed_password"
    )


def test_change_password(user_role, mock_password_service):
    identity = Identity(
        subject_id=uuid4(),
        email=Email(email="existing@example.com"),
        hashed_password="hashed_password123",
        channel_accesses=[ChannelAccess(channel_id=uuid4(), role=user_role)],
    )

    result = identity.change_password(
        Password(value="new_secure_password"), mock_password_service
    )

    assert result.success is True
    assert result.message == "Password changed successfully"
    assert identity.hashed_password == "mocked_hashed_password"


def test_add_channel_access(user_role, admin_role):
    channel_id = uuid4()
    another_channel_id = uuid4()
    identity = Identity(
        subject_id=uuid4(),
        email=Email(email="existing@example.com"),
        hashed_password="hashed_password123",
        channel_accesses=[ChannelAccess(channel_id=channel_id, role=user_role)],
    )

    result = identity.add_channel_access(
        ChannelAccess(channel_id=another_channel_id, role=admin_role)
    )

    assert result.success is True
    assert identity.channel_claims()[1]["role"] == "channel_manager"


def test_add_existing_channel_access(user_role):
    channel_id = uuid4()
    identity = Identity(
        subject_id=uuid4(),
        email=Email(email="existing@example.com"),
        hashed_password="hashed_password123",
        channel_accesses=[ChannelAccess(channel_id=channel_id, role=user_role)],
    )

    result = identity.add_channel_access(
        ChannelAccess(channel_id=channel_id, role=user_role)
    )

    assert result.success is False
    assert result.message == "Channel access already exists"


def test_remove_channel_access(user_role):
    channel_id = uuid4()
    identity = Identity(
        subject_id=uuid4(),
        email=Email(email="existing@example.com"),
        hashed_password="hashed_password123",
        channel_accesses=[ChannelAccess(channel_id=channel_id, role=user_role)],
    )

    result = identity.remove_channel_access(channel_id)

    assert result.success is True
    assert identity.channel_accesses == []


def test_authenticate_success(user_role, mock_password_service):
    identity = Identity(
        subject_id=uuid4(),
        email=Email(email="existing@example.com"),
        hashed_password="some_hashed_password",
        channel_accesses=[ChannelAccess(channel_id=uuid4(), role=user_role)],
    )

    result = identity.authenticate(
        Password(value="correct_password"), mock_password_service
    )

    assert result.success is True
    assert result.message == "Authentication successful"
    mock_password_service.verify_password.assert_called_once_with(
        "correct_password", "some_hashed_password"
    )


def test_authenticate_failure(user_role, mock_password_service):
    identity = Identity(
        subject_id=uuid4(),
        email=Email(email="existing@example.com"),
        hashed_password="some_hashed_password",
        channel_accesses=[ChannelAccess(channel_id=uuid4(), role=user_role)],
    )
    mock_password_service.verify_password.side_effect = lambda plain, hashed: False

    result = identity.authenticate(
        Password(value="wrong_password"), mock_password_service
    )

    assert result.success is False
    assert result.message == "Invalid credentials"
    mock_password_service.verify_password.assert_called_once_with(
        "wrong_password", "some_hashed_password"
    )
