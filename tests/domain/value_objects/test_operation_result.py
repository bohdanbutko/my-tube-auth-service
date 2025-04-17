import pytest
from src.domain.value_objects import OperationResult


def test_success_operation_result():
    # Arrange & Act
    result = OperationResult(success=True, message="Operation succeeded")

    # Assert
    assert result.success is True
    assert result.message == "Operation succeeded"
    assert result.data is None


def test_operation_result_with_data():
    # Arrange & Act
    data = {"user_id": "123", "role": "admin"}
    result = OperationResult(success=True, message="Operation with data", data=data)

    # Assert
    assert result.success is True
    assert result.message == "Operation with data"
    assert result.data == data


def test_failure_operation_result():
    # Arrange & Act
    result = OperationResult(success=False, message="Operation failed")

    # Assert
    assert result.success is False
    assert result.message == "Operation failed"
    assert result.data is None


def test_operation_result_immutability():
    # Arrange
    result = OperationResult(success=True, message="Immutable operation")

    # Act & Assert
    with pytest.raises(Exception):
        result.success = False

    with pytest.raises(Exception):
        result.message = "Modified message"

    with pytest.raises(Exception):
        result.data = {"some": "data"}
