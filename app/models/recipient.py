import sqlalchemy as sa

from app import db


class Recipient(db.IdMixin, db.TimedMixin, db.LocationMixin, db.Base):
    email = sa.Column(sa.String)
    name = sa.Column(sa.String)
    receives_letters = sa.Column(sa.Boolean)
    # frequency
    # date
