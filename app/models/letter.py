from datetime import datetime, timedelta
import enum

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.orm import backref

from app import db


class Letter(db.TimedMixin, db.IdMixin, db.LocationMixin, db.Base):
    class Status(enum.Enum):
        not_corrected = enum.auto()
        not_moderated = enum.auto()
        approved = enum.auto()
        rejected = enum.auto()

        def __str__(self):
            return {
                self.not_corrected: 'A corriger par le prof',
                self.not_moderated: 'A modérer',
                self.approved: 'Approuvée',
                self.rejected: 'Refusée',
            }.get(self, self.name)

    class Theme(enum.Enum):
        travel = enum.auto()
        funny = enum.auto()
        emotional = enum.auto()
        other = enum.auto()

        def __str__(self):
            return {
                self.travel: 'Voyage',
                self.funny: 'Drôle',
                self.emotional: 'Émouvant',
                self.other: 'Autre',
            }.get(self, self.name)

    email = sa.Column(sa.String) # nullable due to legacy data
    event = sa.Column(sa.String)
    writing_session_id = sa.Column(sa.ForeignKey('writing_sessions.id'))
    is_male = sa.Column(sa.Boolean, nullable=False, server_default="1")
    is_young = sa.Column(sa.Boolean)
    content = sa.Column(sa.String, nullable=False)
    signature = sa.Column(sa.String) # nullable due to legacy data
    allow_reuse = sa.Column(sa.Boolean, nullable=False)
    specific_recipient_id = sa.Column(sa.ForeignKey('recipients.id'))
    language_code = sa.Column(sa.ForeignKey('languages.code')) # nullable due to legacy data
    upload_hash = sa.Column(sa.ForeignKey('uploads.hash'))
    status = sa.Column(sa.Enum(Status, native_enum=False), server_default="not_moderated")
    theme = sa.Column(sa.Enum(Theme, native_enum=False))    # If not null, it means the letter is marked as a "favorite"
    moderation_time = sa.Column(sa.DateTime)
    moderator_id = sa.Column(sa.ForeignKey('users.id'))

    language = orm.relationship('Language', backref='letters')
    writing_session = orm.relationship('WritingSession', backref=backref('letters', order_by='Letter.created_at'))
    upload = orm.relationship('Upload', backref='letters')
    specific_recipient = orm.relationship(
        'Recipient', backref='specific_letters'
    )
    moderator = orm.relationship('User', backref='moderated_letters')

    @property
    def is_currently_reviewed(self):
        return self.status == "not_moderated" and self.moderation_time > datetime.utcnow() - timedelta(hours=1)

    @property
    def is_favorite(self):
        return self.theme != None
