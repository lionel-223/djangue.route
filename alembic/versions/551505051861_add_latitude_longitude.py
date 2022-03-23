"""add_latitude_longitude

Revision ID: 551505051861
Revises: 56604e11d48c
Create Date: 2022-03-22 14:38:46.785109

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '551505051861'
down_revision = '56604e11d48c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('letters', sa.Column('latitude', sa.Float(), nullable=True))
    op.add_column('letters', sa.Column('longitude', sa.Float(), nullable=True))
    op.add_column('recipients', sa.Column('latitude', sa.Float(), nullable=True))
    op.add_column('recipients', sa.Column('longitude', sa.Float(), nullable=True))
    op.add_column('schools', sa.Column('latitude', sa.Float(), nullable=True))
    op.add_column('schools', sa.Column('longitude', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('schools', 'longitude')
    op.drop_column('schools', 'latitude')
    op.drop_column('recipients', 'longitude')
    op.drop_column('recipients', 'latitude')
    op.drop_column('letters', 'longitude')
    op.drop_column('letters', 'latitude')
    # ### end Alembic commands ###
