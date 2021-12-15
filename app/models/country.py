import sqlalchemy as sa

from app import db


COUNTRY_NAMES = {
    'BE': 'Belgique',
    'FR': 'France',
    'GB': 'Royaume-Uni',
    'US': 'États-Unis',
}


class Country(db.Base):
    # ISO-3166-1 alpha-2: 2 letter code
    # See https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes
    code = sa.Column(sa.String, nullable=False, primary_key=True)

    def __str__(self):
        return COUNTRY_NAMES.get(self.code, repr(self))
