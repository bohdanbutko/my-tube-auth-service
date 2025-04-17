from uuid import uuid4
from src.domain.entities import User
from src.domain.value_objects import Email, Password, OperationResult
from src.domain.services import PasswordHashingService


class UserAggregate:
    def __init__(
        self, user: User = None, password_service: PasswordHashingService = None
    ):
        self.user = user
        self.password_service = password_service

    def register_user(self, email: Email, password: Password) -> OperationResult:
        if not self.password_service:
            raise ValueError("Password service is required for user registration")

        hashed_password = self.password_service.hash_password(password.password)
        self.user = User(
            id=uuid4(), email=email, hashed_password=hashed_password, roles=["user"]
        )
        return OperationResult(success=True, message="User registered successfully")

    def update_email(self, email: Email) -> OperationResult:
        if not self.user:
            raise ValueError("User is not defined")
        self.user.email = email
        return OperationResult(success=True, message="Email updated successfully")

    def change_password(self, password: Password) -> OperationResult:
        if not self.user:
            raise ValueError("User is not defined")
        if not self.password_service:
            raise ValueError("Password service is required for password change")

        self.user.hashed_password = self.password_service.hash_password(
            password.password
        )
        return OperationResult(success=True, message="Password changed successfully")

    def add_role(self, role: str) -> OperationResult:
        if not self.user:
            raise ValueError("User is not defined")

        if role in self.user.roles:
            return OperationResult(success=False, message="Role already exists")
        self.user.roles.append(role)
        return OperationResult(success=True, message="Role added successfully")

    def remove_role(self, role: str) -> OperationResult:
        if not self.user:
            raise ValueError("User is not defined")

        if role not in self.user.roles:
            return OperationResult(success=False, message="Role does not exist")
        self.user.roles.remove(role)
        return OperationResult(success=True, message="Role removed successfully")

    def authenticate(self, password: Password) -> OperationResult:
        if not self.user:
            raise ValueError("User is not defined")
        if not self.password_service:
            raise ValueError("Password service is required for authentication")

        if self.user.check_password(self.password_service, password.password):
            return OperationResult(success=True, message="Authentication successful")
        else:
            return OperationResult(success=False, message="Invalid credentials")
