import sqlalchemy as sa
from sqlalchemy import orm

from app import db


recipients_languages = sa.Table(
    'recipients_languages', db.Base.metadata,
    sa.Column('recipient_id', sa.ForeignKey('recipients.id')),
    sa.Column('language_code', sa.ForeignKey('languages.code'))
)


class RecipientType(db.IdMixin, db.Base):
    def __str__(self):
        return {
            1: 'EHPAD',
            2: 'Asso',
        }.get(self.id)


class Recipient(db.IdMixin, db.TimedMixin, db.LocationMixin, db.Base):
    email = sa.Column(sa.String)
    type_id = sa.Column(sa.ForeignKey('recipient_types.id'))
    name = sa.Column(sa.String)
    receives_letters = sa.Column(sa.Boolean)
    nb_letters = sa.Column(sa.Integer)
    frequency = sa.Column(sa.Integer)  # Nb of months between each letters pack sent

    languages = orm.relationship("Language", secondary=recipients_languages)
    type = orm.relationship('RecipientType', backref='recipients')

    def __str__(self):
        return f'{self.name} ({self.type})'
