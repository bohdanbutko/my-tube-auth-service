import pytest
from pydantic import ValidationError
from src.domain.value_objects import Email


def test_valid_email():
    # Valid email addresses should be accepted
    email = Email(email="test@example.com")
    assert email.email == "test@example.com"

    # Email constructor should accept valid email strings
    email2 = Email(email="another.valid+email@subdomain.example.co.uk")
    assert email2.email == "another.valid+email@subdomain.example.co.uk"


def test_invalid_email():
    # Invalid email addresses should raise ValidationError
    with pytest.raises(ValidationError):
        Email(email="not_an_email")

    with pytest.raises(ValidationError):
        Email(email="missing@tld")

    with pytest.raises(ValidationError):
        Email(email="@missingname.com")


def test_email_immutability():
    # Email should be immutable (frozen)
    email = Email(email="test@example.com")

    # Attempting to modify attributes should raise an exception
    with pytest.raises(Exception):
        email.email = "modified@example.com"
