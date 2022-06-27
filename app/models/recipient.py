from datetime import datetime
import enum
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.sql.expression import func

from app import db
from . import Letter
from .package import Package
from ..utils.get_lat_long import get_lat_long

recipients_languages = sa.Table(
    'recipients_languages', db.Base.metadata,
    sa.Column('recipient_id', sa.ForeignKey('recipients.id')),
    sa.Column('language_code', sa.ForeignKey('languages.code'))
)


class Recipient(db.IdMixin, db.TimedMixin, db.LocationMixin, db.Base):
    class Types(enum.Enum):
        RETIREMENT_HOME = enum.auto()
        ASSOCIATION = enum.auto()

        def __str__(self):
            return {
                self.RETIREMENT_HOME: 'EHPAD',
                self.ASSOCIATION: 'ASsociation',
            }.get(self, self.name)

    class Status(enum.Enum):
        NOT_MODERATED = enum.auto()
        APPROVED = enum.auto()
        REJECTED = enum.auto()

        def __str__(self):
            return {
                self.NOT_MODERATED: 'A modérer',
                self.APPROVED: 'Approuvé',
                self.REJECTED: 'Refusé',
            }.get(self, self.name)

    email = sa.Column(sa.String)
    name = sa.Column(sa.String)
    phone = sa.Column(sa.String) # Should be validated as E.164 standard
    receives_letters = sa.Column(sa.Boolean)
    nb_letters = sa.Column(sa.Integer)
    frequency = sa.Column(sa.Integer)  # Nb of months between each letters pack sent
    type = sa.Column(sa.Enum(Types, native_enum=False))
    status = sa.Column(sa.Enum(Status, native_enum=False), server_default="not_moderated")

    languages = orm.relationship("Language", secondary=recipients_languages)

    def __str__(self):
        return f'{self.name} ({self.type})'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if (
            ('latitude' not in kwargs and 'longitude' not in kwargs)
            and (self.address and self.city and self.zipcode and self.country_code)
        ):
            self.latitude, self.longitude = get_lat_long(self.address, self.city, self.zipcode, self.country_code)

    @property
    def received_letters(self):
        return [letter.id for package in self.packages for letter in package.letters]

    @property
    def needs_new_package(self):
        last_package = (
            db.session.query(Package).filter_by(recipient_id=self.id).order_by(Package.created_at.desc()).first()
        )
        if not last_package:
            return True
        this_month = datetime.utcnow().month
        return this_month - self.frequency >= last_package.created_at.month

    def generate_package(self, limit_date=None):
        letters = db.session.query(Letter).filter((Letter.status == Letter.Status.approved) &
                                                  (~Letter.is_young) &
                                                  (Letter.id.not_in(self.received_letters)) &
                                                  (Letter.language_code.in_([
                                                      language.code for language in self.languages
                                                  ])))
        if limit_date:
            letters = letters.filter(Letter.created_at >= limit_date)
        specific_letters = letters.filter_by(specific_recipient=self)
        nb_specific_letters = specific_letters.count()
        letters = letters.except_(specific_letters).order_by(func.random()).limit(
            self.nb_letters - nb_specific_letters)
        # TODO faire des packages équilibrés hommes/femmes
        package = letters.union(specific_letters)
        if not package.first():  # No letters found
            return None, None
        is_complete = (package.count() == self.nb_letters)
        return package, is_complete
