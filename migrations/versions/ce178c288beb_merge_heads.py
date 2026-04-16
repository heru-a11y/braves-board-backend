"""merge heads

Revision ID: ce178c288beb
Revises: a5a1094f1464, c79501f8bd08
Create Date: 2026-04-16 04:11:56.561284

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ce178c288beb'
down_revision: Union[str, None] = ('a5a1094f1464', 'c79501f8bd08')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
