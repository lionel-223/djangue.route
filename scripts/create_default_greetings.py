#!/bin/env python

from app import db
from app.models.greeting import Greeting, GREETINGS_TEXTS


def main():
    if db.session.query(Greeting).count() != 0:
        return
    for key in GREETINGS_TEXTS:
        db.get_or_create(Greeting, key=key)
