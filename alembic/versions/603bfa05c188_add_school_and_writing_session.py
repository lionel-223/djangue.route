"""add_school_and_writing_session

Revision ID: 603bfa05c188
Revises: 090398e59893
Create Date: 2022-02-04 15:22:59.936354

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '603bfa05c188'
down_revision = '090398e59893'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('schools',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('zipcode', sa.String(), nullable=True),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('city', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('country_code', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['country_code'], ['countries.code'], name=op.f('fk_schools_country_code_countries')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_schools'))
    )
    op.create_table('schools_languages',
    sa.Column('school_id', sa.Integer(), nullable=True),
    sa.Column('language_code', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['language_code'], ['languages.code'], name=op.f('fk_schools_languages_language_code_languages')),
    sa.ForeignKeyConstraint(['school_id'], ['schools.id'], name=op.f('fk_schools_languages_school_id_schools'))
    )
    op.create_table('schools_teachers',
    sa.Column('school_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['school_id'], ['schools.id'], name=op.f('fk_schools_teachers_school_id_schools')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_schools_teachers_user_id_users'))
    )
    op.create_table('writing_sessions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('type', sa.Enum('teacher_moderation', 'classic_moderation', 'handwriting', name='type', native_enum=False), nullable=True),
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.Column('school_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['school_id'], ['schools.id'], name=op.f('fk_writing_sessions_school_id_schools')),
    sa.ForeignKeyConstraint(['teacher_id'], ['users.id'], name=op.f('fk_writing_sessions_teacher_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_writing_sessions'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('writing_sessions')
    op.drop_table('schools_teachers')
    op.drop_table('schools_languages')
    op.drop_table('schools')
    # ### end Alembic commands ###
