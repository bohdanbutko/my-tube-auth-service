import pytest
from uuid import uuid4

from src.domain.entities import Identity
from src.domain.value_objects import ChannelAccess, Email, Permission, Role
from src.infrastructure.repositories import InMemoryIdentityRepository


@pytest.fixture
def repository():
    repository = InMemoryIdentityRepository()
    repository.clear()
    return repository


@pytest.fixture
def sample_identity():
    return Identity(
        subject_id=uuid4(),
        email=Email(email="test@example.com"),
        hashed_password="hashed_password",
        channel_accesses=[
            ChannelAccess(
                channel_id=uuid4(),
                role=Role(
                    name="channel_viewer",
                    permissions=[
                        Permission(name="channel:view", description="View channel data")
                    ],
                ),
            )
        ],
    )


def test_save_new_identity(repository, sample_identity):
    repository.save(sample_identity)

    assert repository.find_by_subject_id(sample_identity.subject_id) == sample_identity


def test_save_existing_identity(repository, sample_identity):
    repository.save(sample_identity)
    updated_identity = Identity(
        subject_id=sample_identity.subject_id,
        email=Email(email="updated@example.com"),
        hashed_password="new_hashed_password",
        channel_accesses=[
            ChannelAccess(
                channel_id=uuid4(),
                role=Role(
                    name="channel_viewer",
                    permissions=[
                        Permission(name="channel:view", description="View channel data")
                    ],
                ),
            ),
            ChannelAccess(
                channel_id=uuid4(),
                role=Role(
                    name="channel_manager",
                    permissions=[
                        Permission(
                            name="channel:view", description="View channel data"
                        ),
                        Permission(name="video:publish", description="Publish content"),
                    ],
                ),
            ),
        ],
    )

    repository.save(updated_identity)

    found_identity = repository.find_by_subject_id(sample_identity.subject_id)
    assert found_identity == updated_identity
    assert repository.find_by_email("test@example.com") is None


def test_find_by_email_existing(repository, sample_identity):
    repository.save(sample_identity)

    found_identity = repository.find_by_email("test@example.com")

    assert found_identity is not None
    assert found_identity.subject_id == sample_identity.subject_id


def test_find_by_subject_id_existing(repository, sample_identity):
    repository.save(sample_identity)

    found_identity = repository.find_by_subject_id(sample_identity.subject_id)

    assert found_identity is not None
    assert found_identity.email == sample_identity.email


def test_repository_state_is_shared_between_instances(repository, sample_identity):
    repository.save(sample_identity)
    another_repository = InMemoryIdentityRepository()

    assert another_repository.find_by_email("test@example.com") == sample_identity
