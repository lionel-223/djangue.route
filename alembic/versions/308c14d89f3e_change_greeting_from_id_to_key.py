"""Change greeting from id to key

Revision ID: 308c14d89f3e
Revises: f720c6bb4044
Create Date: 2021-12-31 17:07:39.041006

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '308c14d89f3e'
down_revision = 'f720c6bb4044'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('fk_letters_greeting_id_greetings', 'letters', type_='foreignkey')
    op.drop_column('greetings', 'id')
    op.drop_column('letters', 'greeting_id')
    op.add_column('greetings', sa.Column('key', sa.String(), nullable=False))
    op.create_unique_constraint(op.f('uq_greetings_key'), 'greetings', ['key'])
    op.add_column('letters', sa.Column('greeting_key', sa.String(), nullable=False))
    op.create_foreign_key(op.f('fk_letters_greeting_key_greetings'), 'letters', 'greetings', ['greeting_key'], ['key'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('fk_letters_greeting_key_greetings'), 'letters', type_='foreignkey')
    op.drop_constraint(op.f('uq_greetings_key'), 'greetings', type_='unique')
    op.drop_column('letters', 'greeting_key')
    op.drop_column('greetings', 'key')
    op.add_column('letters', sa.Column('greeting_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('greetings', sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('greetings_id_seq'::regclass)"), autoincrement=True, nullable=False))
    op.create_foreign_key('fk_letters_greeting_id_greetings', 'letters', 'greetings', ['greeting_id'], ['id'])
    # ### end Alembic commands ###