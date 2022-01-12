from datetime import datetime, timedelta
import enum

import sqlalchemy as sa
from sqlalchemy import orm

from app import db


class Letter(db.TimedMixin, db.IdMixin, db.LocationMixin, db.Base):
    class Status(enum.Enum):
        not_moderated = enum.auto()
        approved = enum.auto()
        rejected = enum.auto()

        def __str__(self):
            return {
                self.not_moderated: 'A modérer',
                self.approved: 'Approuvée',
                self.rejected: 'Refusée',
            }.get(self, self.name)

    email = sa.Column(sa.String, nullable=False)
    event = sa.Column(sa.String)
    content = sa.Column(sa.String, nullable=False)
    signature = sa.Column(sa.String, nullable=False)
    upload_id = sa.Column(sa.ForeignKey('users.id'))
    allow_reuse = sa.Column(sa.Boolean, nullable=False)
    specific_recipient_id = sa.Column(sa.ForeignKey('recipients.id'))
    language_code = sa.Column(sa.ForeignKey('languages.code'), nullable=False)
    greeting_key = sa.Column(sa.ForeignKey('greetings.key'), nullable=False)
    upload_hash = sa.Column(sa.ForeignKey('uploads.hash'))
    status = sa.Column(sa.Enum(Status, native_enum=False), server_default="not_moderated")
    moderation_time = sa.Column(sa.DateTime)

    language = orm.relationship('Language', backref='letters')
    greeting = orm.relationship('Greeting', backref='letters')
    upload = orm.relationship('Upload', backref='letters')
    specific_recipient = orm.relationship(
        'Recipient', backref='specific_letters'
    )

    @property
    def is_currently_reviewed(self):
        return self.status == "not_moderated" and self.moderation_time > datetime.utcnow() - timedelta(hours=1)
