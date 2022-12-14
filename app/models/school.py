import sqlalchemy as sa
from sqlalchemy import orm

from app import db
from app.utils.get_lat_long import get_lat_long


schools_teachers = sa.Table(
    'schools_teachers', db.Base.metadata,
    sa.Column('school_id', sa.ForeignKey('schools.id')),
    sa.Column('user_id', sa.ForeignKey('users.id'))
)

schools_languages = sa.Table(
    'schools_languages', db.Base.metadata,
    sa.Column('school_id', sa.ForeignKey('schools.id')),
    sa.Column('language_code', sa.ForeignKey('languages.code'))
)


class School(db.Base, db.IdMixin, db.LocationMixin, db.TimedMixin):
    name = sa.Column(sa.String)
    recipient_id = sa.Column(sa.ForeignKey('recipients.id'))

    associated_recipient = orm.relationship('Recipient', backref='associated_school')
    teachers = orm.relationship('User', secondary=schools_teachers, backref='schools')
    languages = orm.relationship('Language', secondary=schools_languages, backref='schools')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.latitude, self.longitude = get_lat_long(self.address, self.city, self.zipcode, self.country_code)
