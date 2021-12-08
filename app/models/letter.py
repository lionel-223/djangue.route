import sqlalchemy as sa
from sqlalchemy import orm

from app import db


class Letter(db.TimedMixin, db.IdMixin, db.LocationMixin, db.Base):
    email = sa.Column(sa.String, nullable=False)
    event = sa.Column(sa.String)
    content = sa.Column(sa.String, nullable=False)
    signature = sa.Column(sa.String, nullable=False)
    upload_id = sa.Column(sa.ForeignKey('users.id'))
    allow_reuse = sa.Column(sa.Boolean, nullable=False)
    specific_recipient_id = sa.Column(sa.ForeignKey('recipients.id'))
    language_code = sa.Column(sa.ForeignKey('languages.code'), nullable=False)
    greeting_id = sa.Column(sa.ForeignKey('greetings.id'), nullable=False)

    language = orm.relationship('Language', back_populates='letters')
    greeting = orm.relationship('Greeting', back_populates='letters')
    upload = orm.relationship('Upload', back_populates='letters')
    specific_recipient = orm.relationship(
        'Recipient', back_populates='specific_letters'
    )
