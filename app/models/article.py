import sqlalchemy as sa
from sqlalchemy import orm

from app import db


class Article(db.TimedMixin, db.IdMixin, db.Base):
    title = sa.Column(sa.String, nullable=False)
    content = sa.Column(sa.String, nullable=False)
    author_id = sa.Column(sa.ForeignKey('users.id'))

    author = orm.relationship('User', backref='article')
