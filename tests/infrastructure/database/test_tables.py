from src.infrastructure.database import (
    identities_table,
    identity_channel_accesses_table,
    metadata,
)


def test_identity_tables_are_registered_in_metadata():
    assert identities_table.name in metadata.tables
    assert identity_channel_accesses_table.name in metadata.tables


def test_identities_table_columns():
    assert set(identities_table.c.keys()) == {
        "subject_id",
        "email",
        "hashed_password",
    }
    assert identities_table.c.subject_id.primary_key
    assert not identities_table.c.email.nullable
    assert not identities_table.c.hashed_password.nullable


def test_identity_channel_accesses_table_columns():
    assert set(identity_channel_accesses_table.c.keys()) == {
        "subject_id",
        "channel_id",
        "role_name",
    }
    assert identity_channel_accesses_table.c.subject_id.primary_key
    assert identity_channel_accesses_table.c.channel_id.primary_key
    assert not identity_channel_accesses_table.c.role_name.nullable
