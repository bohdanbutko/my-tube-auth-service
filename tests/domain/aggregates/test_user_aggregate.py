import pytest
from uuid import uuid4
from src.domain.aggregates import UserAggregate
from src.domain.entities import User
from src.domain.value_objects import Email, Password


@pytest.fixture
def mock_password_service(mocker):
    """Create a mock password service for testing the UserAggregate."""
    mock_service = mocker.Mock()
    mock_service.hash_password.return_value = "mocked_hashed_password"
    mock_service.verify_password.side_effect = (
        lambda plain, hashed: plain == "correct_password"
    )
    return mock_service


@pytest.fixture
def user():
    return User(
        id=uuid4(),
        email=Email(email="existing@example.com"),
        hashed_password="hashed_password123",
        roles=["user"],
    )


def test_register_user(mock_password_service):
    # Arrange
    aggregate = UserAggregate(password_service=mock_password_service)
    email = Email(email="test@example.com")
    password = Password(password="secure_password")

    # Act
    result = aggregate.register_user(email, password)

    # Assert
    assert result.success is True
    assert result.message == "User registered successfully"
    assert aggregate.user is not None
    assert aggregate.user.email == email
    assert aggregate.user.hashed_password == "mocked_hashed_password"
    assert "user" in aggregate.user.roles

    # Verify mock was called correctly
    mock_password_service.hash_password.assert_called_once_with("secure_password")


def test_register_user_without_password_service():
    # Arrange
    aggregate = UserAggregate()
    email = Email(email="test@example.com")
    password = Password(password="secure_password")

    # Act & Assert
    with pytest.raises(
        ValueError, match="Password service is required for user registration"
    ):
        aggregate.register_user(email, password)


def test_update_email(user, mock_password_service):
    # Arrange
    aggregate = UserAggregate(user=user, password_service=mock_password_service)
    new_email = Email(email="new@example.com")

    # Act
    result = aggregate.update_email(new_email)

    # Assert
    assert result.success is True
    assert result.message == "Email updated successfully"
    assert aggregate.user.email == new_email


def test_change_password(user, mock_password_service):
    # Arrange
    aggregate = UserAggregate(user=user, password_service=mock_password_service)
    new_password = Password(password="new_secure_password")

    # Act
    result = aggregate.change_password(new_password)

    # Assert
    assert result.success is True
    assert result.message == "Password changed successfully"
    assert aggregate.user.hashed_password == "mocked_hashed_password"


def test_add_role(user, mock_password_service):
    # Arrange
    aggregate = UserAggregate(user=user, password_service=mock_password_service)

    # Act
    result = aggregate.add_role("admin")

    # Assert
    assert result.success is True
    assert result.message == "Role added successfully"
    assert "admin" in aggregate.user.roles
    assert "user" in aggregate.user.roles  # Original role should still be there


def test_add_existing_role(user, mock_password_service):
    # Arrange
    aggregate = UserAggregate(user=user, password_service=mock_password_service)

    # Act
    result = aggregate.add_role("user")  # "user" role already exists

    # Assert
    assert result.success is False
    assert result.message == "Role already exists"


def test_remove_role(user, mock_password_service):
    # Arrange
    aggregate = UserAggregate(user=user, password_service=mock_password_service)

    # Act
    result = aggregate.remove_role("user")

    # Assert
    assert result.success is True
    assert result.message == "Role removed successfully"
    assert "user" not in aggregate.user.roles


def test_remove_nonexistent_role(user, mock_password_service):
    # Arrange
    aggregate = UserAggregate(user=user, password_service=mock_password_service)

    # Act
    result = aggregate.remove_role("admin")  # "admin" role doesn't exist

    # Assert
    assert result.success is False
    assert result.message == "Role does not exist"


def test_authenticate_success(user, mock_password_service):
    # Arrange
    user.hashed_password = "some_hashed_password"
    aggregate = UserAggregate(user=user, password_service=mock_password_service)
    password = Password(password="correct_password")

    # Act
    result = aggregate.authenticate(password)

    # Assert
    assert result.success is True
    assert result.message == "Authentication successful"

    # Verify mock was called correctly
    mock_password_service.verify_password.assert_called_once_with(
        "correct_password", "some_hashed_password"
    )


def test_authenticate_failure(user, mock_password_service):
    # Arrange
    user.hashed_password = "some_hashed_password"
    aggregate = UserAggregate(user=user, password_service=mock_password_service)
    # Configure mock to fail this time
    mock_password_service.verify_password.side_effect = lambda plain, hashed: False
    password = Password(password="wrong_password")

    # Act
    result = aggregate.authenticate(password)

    # Assert
    assert result.success is False
    assert result.message == "Invalid credentials"

    # Verify mock was called correctly
    mock_password_service.verify_password.assert_called_once_with(
        "wrong_password", "some_hashed_password"
    )
