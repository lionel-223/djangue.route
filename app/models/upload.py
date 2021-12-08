import sqlalchemy as sa

from app import db


class Upload(db.TimedMixin, db.Base):
    hash = sa.Column(sa.String, primary_key=True, nullable=False)
    name = sa.Column(sa.String)
    extension = sa.Column(sa.String)
