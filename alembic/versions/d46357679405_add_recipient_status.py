"""add_recipient_status

Revision ID: d46357679405
Revises: 766c68796ed1
Create Date: 2022-01-13 14:55:00.083831

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd46357679405'
down_revision = '766c68796ed1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('recipients', sa.Column('status', sa.Enum('not_moderated', 'approved', 'rejected', name='status', native_enum=False), server_default='not_moderated', nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('recipients', 'status')
    # ### end Alembic commands ###