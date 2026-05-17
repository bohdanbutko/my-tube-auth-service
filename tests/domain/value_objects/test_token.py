import pytest
from src.domain.value_objects import Token


def test_token_creation():
    # Arrange & Act
    token = Token(access_token="jwt_token_string")

    # Assert
    assert token.access_token == "jwt_token_string"
    assert token.token_type == "bearer"  # Default value should be set


def test_token_with_custom_type():
    # Arrange & Act
    token = Token(access_token="jwt_token_string", token_type="custom")

    # Assert
    assert token.access_token == "jwt_token_string"
    assert token.token_type == "custom"


def test_token_immutability():
    # Arrange
    token = Token(access_token="jwt_token_string")

    # Act & Assert
    with pytest.raises(Exception):
        setattr(token, "access_token", "modified_token")

    with pytest.raises(Exception):
        setattr(token, "token_type", "modified_type")
