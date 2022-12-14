"""set signature and language code to nullable

Revision ID: a4a8da004370
Revises: 696f758f794e
Create Date: 2022-05-21 14:54:19.956310

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4a8da004370'
down_revision = '696f758f794e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('letters', 'signature',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('letters', 'language_code',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('letters', 'language_code',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('letters', 'signature',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
