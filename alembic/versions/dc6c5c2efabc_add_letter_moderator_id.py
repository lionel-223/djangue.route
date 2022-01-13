"""add_letter_moderator_id

Revision ID: dc6c5c2efabc
Revises: 766c68796ed1
Create Date: 2022-01-13 14:28:05.176447

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc6c5c2efabc'
down_revision = '766c68796ed1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('letters', sa.Column('moderator_id', sa.Integer(), nullable=True))
    op.drop_constraint('fk_letters_upload_id_users', 'letters', type_='foreignkey')
    op.create_foreign_key(op.f('fk_letters_moderator_id_users'), 'letters', 'users', ['moderator_id'], ['id'])
    op.drop_column('letters', 'upload_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('letters', sa.Column('upload_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(op.f('fk_letters_moderator_id_users'), 'letters', type_='foreignkey')
    op.create_foreign_key('fk_letters_upload_id_users', 'letters', 'users', ['upload_id'], ['id'])
    op.drop_column('letters', 'moderator_id')
    # ### end Alembic commands ###