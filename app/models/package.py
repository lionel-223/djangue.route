import sqlalchemy as sa
from sqlalchemy import orm

from app import db


packages_letters = sa.Table(
    'packages_letters', db.Base.metadata,
    sa.Column('letter_id', sa.ForeignKey('letters.id')),
    sa.Column('package_id', sa.ForeignKey('packages.id'))
)


class Package(db.Base, db.IdMixin, db.TimedMixin):
    """
    Model for the letter packages sent to the recipients
    """
    file = sa.Column(sa.String)  # Name of the file, not the path
    recipient_id = sa.Column(sa.ForeignKey('recipients.id'), nullable=False)
    is_complete = sa.Column(sa.Boolean)  # If there is not enough letters, we still send the package but we indicate it in the mail

    recipient = orm.relationship('Recipient', backref='packages')
    letters = orm.relationship('Letter', secondary=packages_letters, backref='packages')