from datetime import datetime
import sqlalchemy as sa
from sqlalchemy import orm


@orm.declarative_mixin
class IdMixin:
    id = sa.Column(sa.Integer, primary_key=True)


@orm.declarative_mixin
class KeyMixin:
    key = sa.Column(sa.String, primary_key=True, nullable=False, unique=True)


@orm.declarative_mixin
class TimedMixin:
    created_at = sa.Column(sa.DateTime, default=datetime.utcnow)
    updated_at = sa.Column(sa.DateTime, onupdate=datetime.utcnow)


@orm.declarative_mixin
class LocationMixin:
    zipcode = sa.Column(sa.String)
    address = sa.Column(sa.String)
    city = sa.Column(sa.String)
    latitude = sa.Column(sa.Float)
    longitude = sa.Column(sa.Float)

    @orm.declared_attr
    def country_code(_cls):
        return sa.Column(sa.ForeignKey('countries.code'), nullable=False)

    @orm.declared_attr
    def country(_cls):
        return orm.relationship('Country')
