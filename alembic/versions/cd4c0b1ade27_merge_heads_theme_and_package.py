"""merge heads theme and package

Revision ID: cd4c0b1ade27
Revises: d54cd1104d13, 676d9ce4c9fd
Create Date: 2022-01-26 11:08:16.476755

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd4c0b1ade27'
down_revision = ('d54cd1104d13', '676d9ce4c9fd')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
