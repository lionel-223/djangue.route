"""add_settings_table

Revision ID: 323e1afa2336
Revises: 0d6a333d8025
Create Date: 2022-03-09 10:49:40.919670

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '323e1afa2336'
down_revision = '0d6a333d8025'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('settings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('partnership', sa.String(), nullable=True),
    sa.Column('gender', sa.Enum('neutral', 'male', 'female', name='gender', native_enum=False), server_default='neutral', nullable=True),
    sa.Column('school', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_settings'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('settings')
    # ### end Alembic commands ###
