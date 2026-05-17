import re
from dataclasses import dataclass


EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@dataclass(frozen=True)
class Email:
    email: str

    def __post_init__(self) -> None:
        if not EMAIL_PATTERN.match(self.email):
            raise ValueError(f"Invalid email address: {self.email}")

    def __str__(self) -> str:
        return self.email

    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            return self.email == other
        if isinstance(other, Email):
            return self.email == other.email
        return False
