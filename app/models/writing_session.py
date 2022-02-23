import enum

import sqlalchemy as sa
from sqlalchemy import orm

from app import db


class WritingSession(db.Base, db.IdMixin, db.TimedMixin):
    """
    This model represents a writing session or exercise created by a teacher for his class.
    """
    class Type(enum.Enum):
        """
        The letters can either be written online or on paper by the students. If they are written on paper,
        the teacher uploads the pictures of the letters. If not, he can either be the moderator of the letters
        or let them go through the classic letter loop.
        """
        teacher_moderation = enum.auto()
        classic_moderation = enum.auto()
        handwriting = enum.auto()

        def __str__(self):
            return {
                self.teacher_moderation: 'Lettres en ligne corrigées par le professeur',
                self.classic_moderation: 'Lettres en lignes modérées par 1l1s',
                self.handwriting: 'Lettres manuscrites'
            }.get(self, self.name)

    type = sa.Column(sa.Enum(Type, native_enum=False))
    teacher_id = sa.Column(sa.ForeignKey('users.id'))
    school_id = sa.Column(sa.ForeignKey('schools.id'))
    title = sa.Column(sa.String)

    teacher = orm.relationship('User', backref='writing_sessions')
    school = orm.relationship('School', backref='writing_sessions')
