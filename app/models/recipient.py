from datetime import datetime
import enum
import sqlalchemy as sa
from sqlalchemy import orm

from app import db
from .package import Package

recipients_languages = sa.Table(
    'recipients_languages', db.Base.metadata,
    sa.Column('recipient_id', sa.ForeignKey('recipients.id')),
    sa.Column('language_code', sa.ForeignKey('languages.code'))
)


class Recipient(db.IdMixin, db.TimedMixin, db.LocationMixin, db.Base):
    class Types(enum.Enum):
        retirement_home = enum.auto()
        association = enum.auto()

        def __str__(self):
            return {
                self.retirement_home: 'EHPAD',
                self.association: 'Association',
            }.get(self, self.name)

    class Status(enum.Enum):
        not_moderated = enum.auto()
        approved = enum.auto()
        rejected = enum.auto()

        def __str__(self):
            return {
                self.not_moderated: 'A modérer',
                self.approved: 'Approuvé',
                self.rejected: 'Refusé',
            }.get(self, self.name)

    email = sa.Column(sa.String)
    name = sa.Column(sa.String)
    receives_letters = sa.Column(sa.Boolean)
    nb_letters = sa.Column(sa.Integer)
    frequency = sa.Column(sa.Integer)  # Nb of months between each letters pack sent
    type = sa.Column(sa.Enum(Types, native_enum=False))
    status = sa.Column(sa.Enum(Status, native_enum=False), server_default="not_moderated")

    languages = orm.relationship("Language", secondary=recipients_languages)

    def __str__(self):
        return f'{self.name} ({self.type})'

    @property
    def received_letters(self):
        return [letter.id for package in self.packages for letter in package]

    @property
    def needs_new_package(self):
        last_package = (
            db.session.query(Package).filter_by(recipient_id=self.id).order_by(Package.created_at.desc()).first()
        )
        if not last_package:
            return True
        this_month = datetime.utcnow().month
        return this_month - self.frequency >= last_package.created_at.month


