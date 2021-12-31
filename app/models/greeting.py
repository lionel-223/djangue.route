from app import db


GREETINGS_TEXTS = {
    'coucou': 'Coucou',
    'bonjour': 'Bonjour',
}


class Greeting(db.TimedMixin, db.KeyMixin, db.Base):
    def __str__(self):
        return GREETINGS_TEXTS.get(self.key, self.key)
