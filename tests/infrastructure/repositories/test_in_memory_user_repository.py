import pytest
from uuid import uuid4
from src.domain.entities import User
from src.domain.value_objects import Email
from src.infrastructure.repositories import InMemoryUserRepository


@pytest.fixture
def repository():
    return InMemoryUserRepository()


@pytest.fixture
def sample_user():
    return User(
        id=uuid4(),
        email=Email(email="test@example.com"),
        hashed_password="hashed_password",
        roles=["user"],
    )


@pytest.fixture
def mocked_user(mocker):
    """Create a mock user with controlled uuid for predictable testing"""
    # Create a fixed UUID for testing
    fixed_uuid = uuid4()

    # We're not actually testing code that calls uuid4 in this test
    # We're just creating a user with a known ID for testing the repository
    user = User(
        id=fixed_uuid,
        email=Email(email="test@example.com"),
        hashed_password="hashed_password",
        roles=["user"],
    )
    return user


def test_save_new_user(repository, sample_user):
    # Arrange - repository and user are from fixtures

    # Act
    repository.save(sample_user)

    # Assert
    assert len(repository.users) == 1
    assert repository.users[0] == sample_user


def test_save_existing_user(repository, sample_user):
    # Arrange
    repository.save(sample_user)

    # Create an updated version of the same user (same ID)
    updated_user = User(
        id=sample_user.id,
        email=Email(email="updated@example.com"),
        hashed_password="new_hashed_password",
        roles=["user", "admin"],
    )

    # Act
    repository.save(updated_user)

    # Assert
    assert len(repository.users) == 1  # Should still have only one user
    assert repository.users[0].email == Email(email="updated@example.com")
    assert repository.users[0].hashed_password == "new_hashed_password"
    assert "admin" in repository.users[0].roles


def test_find_by_email_existing(repository, sample_user):
    # Arrange
    repository.save(sample_user)

    # Act
    found_user = repository.find_by_email("test@example.com")

    # Assert
    assert found_user is not None
    assert found_user.id == sample_user.id
    assert found_user.email == sample_user.email


def test_find_by_email_nonexistent(repository):
    # Arrange - empty repository

    # Act
    found_user = repository.find_by_email("nonexistent@example.com")

    # Assert
    assert found_user is None


def test_find_by_id_existing(repository, sample_user):
    # Arrange
    repository.save(sample_user)

    # Act
    found_user = repository.find_by_id(sample_user.id)

    # Assert
    assert found_user is not None
    assert found_user.id == sample_user.id
    assert found_user.email == sample_user.email


def test_find_by_id_nonexistent(repository):
    # Arrange - empty repository
    nonexistent_id = uuid4()

    # Act
    found_user = repository.find_by_id(nonexistent_id)

    # Assert
    assert found_user is None


def test_clear(repository, sample_user):
    # Arrange
    repository.save(sample_user)
    assert len(repository.users) == 1

    # Act
    repository.clear()

    # Assert
    assert len(repository.users) == 0


def test_save_with_mocked_user(repository, mocked_user):
    # Arrange
    user = mocked_user

    # Act
    repository.save(user)

    # Assert
    assert len(repository.users) == 1
    assert repository.users[0].id == user.id  # Compare with the UUID object
