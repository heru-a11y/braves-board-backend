"""add partial unique index on columns

Revision ID: c79501f8bd08
Revises: 9c9694347c17
Create Date: 2026-04-14 10:53:09.348375

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c79501f8bd08'
down_revision: Union[str, None] = '9c9694347c17'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop constraint lama (jika ada)
    op.drop_constraint(
        "uq_column_board_position",
        "columns",
        type_="unique"
    )

    # Buat partial unique index (hanya untuk data yang belum di-soft delete)
    op.create_index(
        "uq_column_board_position",
        "columns",
        ["board_id", "position"],
        unique=True,
        postgresql_where=sa.text("deleted_at IS NULL")
    )


def downgrade() -> None:
    # Hapus partial index
    op.drop_index(
        "uq_column_board_position",
        table_name="columns"
    )

    # Kembalikan constraint lama (tanpa kondisi)
    op.create_unique_constraint(
        "uq_column_board_position",
        "columns",
        ["board_id", "position"]
    )
