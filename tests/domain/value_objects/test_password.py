import pytest
from src.domain.value_objects import Password


def test_password_creation():
    # Arrange & Act
    password = Password(password="secure_password")

    # Assert
    assert password.password == "secure_password"


def test_password_immutability():
    # Arrange
    password = Password(password="secure_password")

    # Act & Assert
    with pytest.raises(Exception):
        password.password = "modified_password"
