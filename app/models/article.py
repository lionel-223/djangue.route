import sqlalchemy as sa
from sqlalchemy import orm

from app import db


class Article(db.TimedMixin, db.IdMixin, db.Base):
    title = sa.Column(sa.String, nullable=False)
    content = sa.Column(sa.String, nullable=False)
    author_id = sa.Column(sa.ForeignKey('users.id'))
    upload_hash = sa.Column(sa.ForeignKey('uploads.hash'))

    author = orm.relationship('User', backref='article')
    upload = orm.relationship('Upload', backref='article')
