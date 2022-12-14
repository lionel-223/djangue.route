"""Remove language name

Revision ID: 904a362f6318
Revises: ed00e9053bc0
Create Date: 2021-12-08 16:06:16.400212

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '904a362f6318'
down_revision = 'ed00e9053bc0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('languages', 'name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('languages', sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
