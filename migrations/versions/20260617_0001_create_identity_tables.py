"""create identity tables

Revision ID: 20260617_0001
Revises:
Create Date: 2026-06-17
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260617_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "identities",
        sa.Column("subject_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("subject_id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index("ix_identities_email", "identities", ["email"])

    op.create_table(
        "identity_channel_accesses",
        sa.Column("subject_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("channel_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("role_name", sa.String(length=64), nullable=False),
        sa.ForeignKeyConstraint(
            ["subject_id"],
            ["identities.subject_id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("subject_id", "channel_id"),
    )


def downgrade() -> None:
    op.drop_table("identity_channel_accesses")
    op.drop_index("ix_identities_email", table_name="identities")
    op.drop_table("identities")
