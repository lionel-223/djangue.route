import sqlalchemy as sa

from app import db


LANGUAGES_NAMES = {
    'en': 'Anglais',
    'fr': 'Français',
    'es': 'Espagnol',
    'de': 'Allemand',
    'nl': 'Néerlandais',
}


class Language(db.TimedMixin, db.Base):
    # ISO 639-1 2 letters code
    # English = "en", we do not distinguis between British, American, Australian
    # See https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
    code = sa.Column(sa.String, nullable=False, primary_key=True)
    accepts_letters = sa.Column(sa.Boolean)
    has_translations = sa.Column(sa.Boolean)

    def __str__(self):
        return LANGUAGES_NAMES.get(self.code, repr(self))
