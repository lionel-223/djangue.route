import sqlalchemy as sa

from app import db


class User(db.TimedMixin, db.IdMixin, db.Base):
    email = sa.Column(sa.String)
