import pytest
import jwt
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from src.domain.entities import User
from src.domain.value_objects import Email, Token
from src.infrastructure.services import JWTTokenService


@pytest.fixture
def sample_user():
    return User(
        id=uuid4(),
        email=Email(email="test@example.com"),
        hashed_password="hashed_password",
        roles=["user"],
    )


@pytest.fixture
def mocked_token_service(mocker):
    # Mock jwt.encode and jwt.decode
    mock_encode = mocker.patch("jwt.encode")
    mock_encode.return_value = "mocked.jwt.token"

    mock_decode = mocker.patch("jwt.decode")
    mock_decode.return_value = {
        "sub": "test-user-id",
        "email": "test@example.com",
        "roles": ["user"],
        "exp": datetime.now(timezone.utc).timestamp() + 3600,
    }

    service = JWTTokenService(secret_key="test_secret_key", algorithm="HS256")
    return service, mock_encode, mock_decode


def test_create_access_token_mocked(mocked_token_service, sample_user):
    # Arrange
    service, mock_encode, _ = mocked_token_service

    # Act
    token = service.create_access_token(sample_user)

    # Assert
    assert isinstance(token, Token)
    assert token.access_token == "mocked.jwt.token"
    assert token.token_type == "bearer"

    # Verify the mock was called with correct arguments
    mock_encode.assert_called_once()
    # Extract the first positional argument (the payload)
    args, _ = mock_encode.call_args
    payload = args[0]
    assert payload["sub"] == str(sample_user.id)
    assert payload["email"] == str(sample_user.email)
    assert payload["roles"] == sample_user.roles


def test_create_access_token_with_expiry_mocked(mocked_token_service, sample_user):
    # Arrange
    service, mock_encode, _ = mocked_token_service
    expires_delta = timedelta(minutes=30)

    # Act
    token = service.create_access_token(sample_user, expires_delta=expires_delta)

    # Assert
    assert isinstance(token, Token)
    assert token.access_token == "mocked.jwt.token"

    # Verify expiry was included in the payload
    mock_encode.assert_called_once()
    args, _ = mock_encode.call_args
    payload = args[0]
    assert "exp" in payload


def test_verify_token_success_mocked(mocked_token_service):
    # Arrange
    service, _, mock_decode = mocked_token_service
    mock_decode.return_value = {
        "sub": "test-user-id",
        "email": "test@example.com",
        "roles": ["user"],
    }

    # Act
    payload = service.verify_token("some.token.string")

    # Assert
    assert payload is not None
    assert payload["sub"] == "test-user-id"
    assert payload["email"] == "test@example.com"
    assert payload["roles"] == ["user"]
    mock_decode.assert_called_once_with(
        "some.token.string", "test_secret_key", algorithms=["HS256"]
    )


def test_verify_token_failure_invalid_token_mocked(mocked_token_service):
    # Arrange
    service, _, mock_decode = mocked_token_service
    mock_decode.side_effect = jwt.PyJWTError(
        "Invalid token"
    )  # Use the correct exception type

    # Act
    payload = service.verify_token("invalid.token")

    # Assert
    assert payload is None
    mock_decode.assert_called_once()
