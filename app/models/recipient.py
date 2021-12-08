import sqlalchemy as sa

from app import db


class Recipient(db.IdMixin, db.TimedMixin, db.LocationMixin, db.Base):
    email = sa.Column(sa.String)
    receive_letters = sa.Column(sa.Boolean)
    # frequency
    # date
