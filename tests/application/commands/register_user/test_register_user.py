from src.application.commands import RegisterUserCommand, register_user_handler


def test_register_user_success(mocker):
    # Mock the dependencies used inside the register_user_handler
    mock_repo = mocker.patch(
        "src.infrastructure.repositories.in_memory_user_repository.InMemoryUserRepository"
    )
    mock_password_service = mocker.patch(
        "src.infrastructure.services.bcrypt_password_hashing_service.BcryptPasswordHashingService"
    )

    # Configure the mock to return a service instance with a hash_password method
    mock_service_instance = mock_password_service.return_value
    mock_service_instance.hash_password.return_value = "hashed_password"

    # Create the command
    command = RegisterUserCommand(email="test@mail.com", password="password")

    # Execute the handler
    result = register_user_handler(command)

    # Assert the result
    assert result["success"] is True
    assert result["message"] == "User registered successfully"
