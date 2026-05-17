import pytest
from src.domain.value_objects import Password


def test_password_creation():
    # Arrange & Act
    password = Password(value="secure_password")

    # Assert
    assert password.value == "secure_password"


def test_password_immutability():
    # Arrange
    password = Password(value="secure_password")

    # Act & Assert
    with pytest.raises(Exception):
        setattr(password, "value", "modified_password")
