"""empty message

Revision ID: b64f686fc6c4
Revises: a643cdd996fc
Create Date: 2021-12-16 14:57:02.105261

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b64f686fc6c4'
down_revision = 'a643cdd996fc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('recipients_languages',
    sa.Column('recipient_id', sa.Integer(), nullable=True),
    sa.Column('language_code', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['language_code'], ['languages.code'], name=op.f('fk_recipients_languages_language_code_languages')),
    sa.ForeignKeyConstraint(['recipient_id'], ['recipients.id'], name=op.f('fk_recipients_languages_recipient_id_recipients'))
    )
    op.create_table('users_recipients',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('recipient_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['recipient_id'], ['recipients.id'], name=op.f('fk_users_recipients_recipient_id_recipients')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_users_recipients_user_id_users'))
    )
    op.add_column('letters', sa.Column('city', sa.String(), nullable=True))
    op.add_column('recipients', sa.Column('city', sa.String(), nullable=True))
    op.add_column('recipients', sa.Column('nb_letters', sa.Integer(), nullable=True))
    op.add_column('recipients', sa.Column('frequency', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('recipients', 'frequency')
    op.drop_column('recipients', 'nb_letters')
    op.drop_column('recipients', 'city')
    op.drop_column('letters', 'city')
    op.drop_table('users_recipients')
    op.drop_table('recipients_languages')
    # ### end Alembic commands ###