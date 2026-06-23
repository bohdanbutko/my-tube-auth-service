from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.dialects.postgresql import UUID

metadata = MetaData()

identities_table = Table(
    "identities",
    metadata,
    Column("subject_id", UUID(as_uuid=True), primary_key=True),
    Column("email", String(320), nullable=False, unique=True, index=True),
    Column("hashed_password", String, nullable=False),
)

identity_channel_accesses_table = Table(
    "identity_channel_accesses",
    metadata,
    Column(
        "subject_id",
        UUID(as_uuid=True),
        ForeignKey("identities.subject_id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column("channel_id", UUID(as_uuid=True), primary_key=True),
    Column("role_name", String(64), nullable=False),
)
