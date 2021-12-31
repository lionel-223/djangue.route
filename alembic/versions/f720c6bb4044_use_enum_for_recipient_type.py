"""Use enum for recipient type

Revision ID: f720c6bb4044
Revises: b64f686fc6c4
Create Date: 2021-12-23 03:07:14.033373

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f720c6bb4044'
down_revision = 'b64f686fc6c4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('fk_recipients_type_id_recipient_types', 'recipients', type_='foreignkey')
    op.drop_table('recipient_types')
    op.drop_column('recipients', 'type_id')
    op.add_column('recipients', sa.Column('type', sa.Enum('retirement_home', 'association', name='type', native_enum=False), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('recipients', sa.Column('type_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_table('recipient_types',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id', name='pk_recipient_types')
    )
    op.create_foreign_key('fk_recipients_type_id_recipient_types', 'recipients', 'recipient_types', ['type_id'], ['id'])
    op.drop_column('recipients', 'type')
    # ### end Alembic commands ###
