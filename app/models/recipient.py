import enum
import sqlalchemy as sa
from sqlalchemy import orm

from app import db


recipients_languages = sa.Table(
    'recipients_languages', db.Base.metadata,
    sa.Column('recipient_id', sa.ForeignKey('recipients.id')),
    sa.Column('language_code', sa.ForeignKey('languages.code'))
)


class Recipient(db.IdMixin, db.TimedMixin, db.LocationMixin, db.Base):
    class Types(enum.Enum):
        retirement_home = enum.auto()
        association = enum.auto()

        def __str__(self):
            return {
                self.retirement_home: 'EHPAD',
                self.association: 'Association',
            }.get(self, self.name)

    email = sa.Column(sa.String)
    name = sa.Column(sa.String)
    receives_letters = sa.Column(sa.Boolean)
    nb_letters = sa.Column(sa.Integer)
    frequency = sa.Column(sa.Integer)  # Nb of months between each letters pack sent
    type = sa.Column(sa.Enum(Types, native_enum=False))

    languages = orm.relationship("Language", secondary=recipients_languages)

    def __str__(self):
        return f'{self.name} ({self.type})'
