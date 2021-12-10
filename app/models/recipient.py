import sqlalchemy as sa
from sqlalchemy import orm

from app import db


class RecipientType(db.IdMixin, db.Base):
    def __str__(self):
        return {
            1: 'EHPAD',
            2: 'Asso',
        }.get(self.id)


class Recipient(db.IdMixin, db.TimedMixin, db.LocationMixin, db.Base):
    email = sa.Column(sa.String)
    type_id = sa.Column(sa.ForeignKey('recipient_type.id'))
    name = sa.Column(sa.String)
    receives_letters = sa.Column(sa.Boolean)
    # frequency
    # date

    type = orm.relationship('RecipientType', backref='recipients')
