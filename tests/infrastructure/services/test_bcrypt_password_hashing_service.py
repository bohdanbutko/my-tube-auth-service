import pytest
from src.infrastructure.services import BcryptPasswordHashingService


@pytest.fixture
def password_service():
    return BcryptPasswordHashingService()


@pytest.fixture
def mocked_password_service(mocker):
    # Mock the CryptContext from passlib
    mock_crypt_context = mocker.patch(
        "src.infrastructure.services.bcrypt_password_hashing_service.CryptContext"
    )

    # Configure the mock's instance methods
    mock_context_instance = mock_crypt_context.return_value
    mock_context_instance.hash.return_value = "mocked_hashed_password"
    mock_context_instance.verify.side_effect = (
        lambda plain, hashed: plain == "correct_password"
        and hashed == "mocked_hashed_password"
    )

    # Return the service with mocked dependencies
    return BcryptPasswordHashingService(), mock_context_instance


def test_hash_password(password_service):
    # Arrange
    plain_password = "secure_password"

    # Act
    hashed = password_service.hash_password(plain_password)

    # Assert
    assert hashed != plain_password  # Hash should be different from original
    assert len(hashed) > 20  # Bcrypt hashes are typically long


def test_verify_password_success(password_service):
    # Arrange
    plain_password = "secure_password"
    hashed = password_service.hash_password(plain_password)

    # Act
    result = password_service.verify_password(plain_password, hashed)

    # Assert
    assert result is True


def test_verify_password_failure(password_service):
    # Arrange
    plain_password = "secure_password"
    wrong_password = "wrong_password"
    hashed = password_service.hash_password(plain_password)

    # Act
    result = password_service.verify_password(wrong_password, hashed)

    # Assert
    assert result is False


def test_different_passwords_have_different_hashes(password_service):
    # Arrange
    password1 = "password1"
    password2 = "password2"

    # Act
    hash1 = password_service.hash_password(password1)
    hash2 = password_service.hash_password(password2)

    # Assert
    assert hash1 != hash2


def test_same_password_has_different_salts(password_service):
    # Arrange
    password = "same_password"

    # Act
    hash1 = password_service.hash_password(password)
    hash2 = password_service.hash_password(password)

    # Assert
    assert hash1 != hash2  # Due to different salts, the hashes should be different

    # But both should verify successfully
    assert password_service.verify_password(password, hash1) is True
    assert password_service.verify_password(password, hash2) is True


def test_hash_password_mocked(mocked_password_service):
    # Arrange
    service, mock_context = mocked_password_service

    # Act
    hashed = service.hash_password("secure_password")

    # Assert
    assert hashed == "mocked_hashed_password"
    mock_context.hash.assert_called_once_with("secure_password")


def test_verify_password_success_mocked(mocked_password_service):
    # Arrange
    service, mock_context = mocked_password_service

    # Act
    result = service.verify_password("correct_password", "mocked_hashed_password")

    # Assert
    assert result is True
    mock_context.verify.assert_called_once_with(
        "correct_password", "mocked_hashed_password"
    )


def test_verify_password_failure_mocked(mocked_password_service):
    # Arrange
    service, mock_context = mocked_password_service
    mock_context.verify.side_effect = lambda plain, hashed: False

    # Act
    result = service.verify_password("wrong_password", "mocked_hashed_password")

    # Assert
    assert result is False
    mock_context.verify.assert_called_once_with(
        "wrong_password", "mocked_hashed_password"
    )
