from uuid import UUID

from src.domain.entities import User
from src.domain.repositories import UserRepository


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self.users: list[User] = []

    def save(self, user: User) -> None:
        # Check if user already exists (by ID), if so update it
        for i, existing_user in enumerate(self.users):
            if existing_user.id == user.id:
                self.users[i] = user
                return

        # If not found, add a new user
        self.users.append(user)

    def find_by_email(self, email: str) -> User | None:
        for user in self.users:
            if user.email == email:
                return user
        return None

    def find_by_id(self, user_id: UUID) -> User | None:
        for user in self.users:
            if user.id == user_id:
                return user
        return None

    # For testing/debugging
    def clear(self) -> None:
        self.users = []
