from app import db


GREETINGS_TEXTS = {
    1: 'Coucou',
    2: 'Bonjour',
}


class Greeting(db.TimedMixin, db.IdMixin, db.Base):
    def __str__(self):
        return GREETINGS_TEXTS.get(self.id, self.id)
