import sqlalchemy as sa
from sqlalchemy import orm

from app import db


class Upload(db.TimedMixin, db.Base):
    hash = sa.Column(sa.String, primary_key=True, nullable=False)
    name = sa.Column(sa.String)
    extension = sa.Column(sa.String)


class HandwrittenLetter(db.TimedMixin, db.Base):
    hash = sa.Column(sa.String, primary_key=True, nullable=False)
    name = sa.Column(sa.String)
    extension = sa.Column(sa.String)
    writing_session_id = sa.Column(sa.ForeignKey('writing_sessions.id'))

    writing_session = orm.relationship('WritingSession', backref="handwritten_letters")
