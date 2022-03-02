"""add_handwritten_letters

Revision ID: 0d6a333d8025
Revises: be5589e42eef
Create Date: 2022-03-02 15:09:39.194328

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d6a333d8025'
down_revision = 'be5589e42eef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('handwritten_letters',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('hash', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('extension', sa.String(), nullable=True),
    sa.Column('writing_session_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['writing_session_id'], ['writing_sessions.id'], name=op.f('fk_handwritten_letters_writing_session_id_writing_sessions')),
    sa.PrimaryKeyConstraint('hash', name=op.f('pk_handwritten_letters'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('handwritten_letters')
    # ### end Alembic commands ###
