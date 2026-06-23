from uuid import UUID

from sqlalchemy import Connection, Engine, delete, select
from sqlalchemy.dialects.postgresql import insert

from src.domain.entities import Identity
from src.domain.policies import RoleCatalog
from src.domain.repositories import IdentityRepository
from src.domain.value_objects import ChannelAccess, Email
from src.infrastructure.database import (
    identities_table,
    identity_channel_accesses_table,
)


class PostgresIdentityRepository(IdentityRepository):
    def __init__(self, engine: Engine):
        self.engine = engine

    def save(self, identity: Identity) -> None:
        with self.engine.begin() as connection:
            connection.execute(
                insert(identities_table)
                .values(
                    subject_id=identity.subject_id,
                    email=str(identity.email),
                    hashed_password=identity.hashed_password,
                )
                .on_conflict_do_update(
                    index_elements=[identities_table.c.subject_id],
                    set_={
                        "email": str(identity.email),
                        "hashed_password": identity.hashed_password,
                    },
                )
            )
            connection.execute(
                delete(identity_channel_accesses_table).where(
                    identity_channel_accesses_table.c.subject_id == identity.subject_id
                )
            )
            if identity.channel_accesses:
                connection.execute(
                    insert(identity_channel_accesses_table),
                    [
                        {
                            "subject_id": identity.subject_id,
                            "channel_id": channel_access.channel_id,
                            "role_name": channel_access.role.name,
                        }
                        for channel_access in identity.channel_accesses
                    ],
                )

    def find_by_email(self, email: str) -> Identity | None:
        statement = select(identities_table).where(identities_table.c.email == email)

        with self.engine.connect() as connection:
            row = connection.execute(statement).mappings().one_or_none()
            if not row:
                return None

            return self._to_identity(connection, row)

    def find_by_subject_id(self, subject_id: UUID) -> Identity | None:
        statement = select(identities_table).where(
            identities_table.c.subject_id == subject_id
        )

        with self.engine.connect() as connection:
            row = connection.execute(statement).mappings().one_or_none()
            if not row:
                return None

            return self._to_identity(connection, row)

    def _to_identity(self, connection: Connection, identity_row) -> Identity:
        channel_accesses_statement = select(identity_channel_accesses_table).where(
            identity_channel_accesses_table.c.subject_id == identity_row["subject_id"]
        )
        channel_access_rows = (
            connection.execute(channel_accesses_statement).mappings().all()
        )

        channel_accesses = []
        for channel_access_row in channel_access_rows:
            role = RoleCatalog.find_by_name(channel_access_row["role_name"])
            if not role:
                continue
            channel_accesses.append(
                ChannelAccess(
                    channel_id=channel_access_row["channel_id"],
                    role=role,
                )
            )

        return Identity(
            subject_id=identity_row["subject_id"],
            email=Email(email=identity_row["email"]),
            hashed_password=identity_row["hashed_password"],
            channel_accesses=channel_accesses,
        )
