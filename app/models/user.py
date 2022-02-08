from flask_login import UserMixin
import sqlalchemy as sa
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


users_recipients = sa.Table(
    'users_recipients', db.Base.metadata,
    sa.Column('user_id', sa.ForeignKey('users.id')),
    sa.Column('recipient_id', sa.ForeignKey('recipients.id'))
)


class User(db.TimedMixin, db.IdMixin, UserMixin, db.Base):
    email = sa.Column(sa.String)
    password_hash = sa.Column(sa.String(128))
    can_moderate = sa.Column(sa.Boolean, default=False)
    can_see_stats = sa.Column(sa.Boolean, default=False)
    can_edit_recipients = sa.Column(sa.Boolean, default=False)

    recipients = orm.relationship("Recipient", secondary=users_recipients, backref="users", lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __str__(self):
        return self.email

    @property
    def admin_accesses(self):
        return {
            key: getattr(self, key) for key in ('can_moderate', 'can_see_stats', 'can_edit_recipients')
        }
