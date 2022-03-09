import enum

import sqlalchemy as sa

from app import db


class Setting(db.TimedMixin, db.IdMixin, db.Base):
    class Gender(enum.Enum):
        neutral = enum.auto()
        male = enum.auto()
        female = enum.auto()

        def __str__(self):
            return {
                self.neutral: 'Classique',
                self.male: 'Homme',
                self.female: 'Femme',
            }.get(self, self.name)

    partnership = sa.Column(sa.String)
    gender = sa.Column(sa.Enum(Gender, native_enum=False), server_default="neutral")
    school = sa.Column(sa.Boolean)
