import os
from alembic import command
from alembic.config import Config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALEMBIC_INI_PATH = os.path.join(BASE_DIR, "alembic.ini")

def get_alembic_config():
    return Config(ALEMBIC_INI_PATH)

def upgrade():
    command.upgrade(get_alembic_config(), "head")

def downgrade():
    command.downgrade(get_alembic_config(), "-1")