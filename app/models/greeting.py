from app import db


class Greeting(db.TimedMixin, db.IdMixin, db.Base):
    pass
