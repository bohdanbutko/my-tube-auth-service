import pytest
from uuid import uuid4
from src.domain.entities import User
from src.domain.value_objects import Email


@pytest.fixture
def mock_password_service(mocker):
    """Create a mock password service for testing the User entity."""
    mock_service = mocker.Mock()
    mock_service.verify_password.side_effect = (
        lambda plain, hashed: plain == "correct_password"
    )
    return mock_service


def test_user_creation():
    # Arrange
    user_id = uuid4()
    email = Email(email="test@example.com")
    hashed_password = "hashed_password_123"
    roles = ["user"]

    # Act
    user = User(id=user_id, email=email, hashed_password=hashed_password, roles=roles)

    # Assert
    assert user.id == user_id
    assert user.email == email
    assert user.hashed_password == hashed_password
    assert user.roles == roles


def test_check_password(mock_password_service):
    # Arrange
    user = User(
        id=uuid4(),
        email=Email(email="test@example.com"),
        hashed_password="hashed_password",
        roles=["user"],
    )

    # Act & Assert
    assert user.check_password(mock_password_service, "correct_password") is True
    assert user.check_password(mock_password_service, "wrong_password") is False

    # Verify mock was called correctly
    mock_password_service.verify_password.assert_any_call(
        "correct_password", "hashed_password"
    )
    mock_password_service.verify_password.assert_any_call(
        "wrong_password", "hashed_password"
    )
