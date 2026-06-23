from uuid import uuid4

from src.infrastructure.repositories import PostgresIdentityRepository


def test_find_by_email_reuses_connection_when_loading_channel_accesses(mocker):
    subject_id = uuid4()
    channel_id = uuid4()
    identity_result = mocker.Mock()
    identity_result.mappings.return_value.one_or_none.return_value = {
        "subject_id": subject_id,
        "email": "test@example.com",
        "hashed_password": "hashed-password",
    }
    channel_access_result = mocker.Mock()
    channel_access_result.mappings.return_value.all.return_value = [
        {
            "subject_id": subject_id,
            "channel_id": channel_id,
            "role_name": "channel_viewer",
        }
    ]

    connection = mocker.Mock()
    connection.execute.side_effect = [identity_result, channel_access_result]
    engine = mocker.MagicMock()
    engine.connect.return_value.__enter__.return_value = connection
    repository = PostgresIdentityRepository(engine)

    identity = repository.find_by_email("test@example.com")

    assert identity is not None
    assert identity.subject_id == subject_id
    assert identity.channel_accesses[0].channel_id == channel_id
    engine.connect.assert_called_once_with()
    engine.begin.assert_not_called()
    assert connection.execute.call_count == 2
