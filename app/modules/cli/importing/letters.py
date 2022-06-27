"""
Exported data refers to data exported in a readable and digest format, using
column names that are the same as the ones of the new db, or close to them
"""

import functools
import traceback
from typing import Type
import csv
from datetime import datetime

from app import db
from app.models import Country, Letter
from . import group


@functools.cache
def get_country(x):
    if not x:
        return None
    return db.session.query(Country).filter_by(name=x).first()

def parse(row: dict):
    def get(key: str, type: Type = str, func=None):
        result = row.get(key, '').strip()
        if func:
            result = func(result)
        if type == bool:
            return result == 'True'
        if result == '':
            return None
        return result
    date = row.get('date')
    if date:
        date = datetime.fromisoformat(date)
    return {
        'id': get('id'),
        'created_at': date,
        'email': get('email', func=str.lower),
        'is_male': get('is_male', bool),
        'content': f"{get('greeting')}\n{get('content')}",
        'signature': get('signature'),
        'allow_reuse': get('allow_reuse', bool),
        'city': get('city'),
        'zipcode': get('zipcode'),
        'country': get_country((get('country'))),
        'language_code': get('language_code'),
    }

@group.command('letters')
def import_letters(path: str):
    ids = [x.id for x in db.session.query(Letter).with_entities(Letter.id)]
    ids = set(ids)
    f = open(path)
    reader = csv.DictReader(f)
    data = reader
    for i, row in enumerate(data):
        if i % 1000 == 0:
            print(f'Importing {i}th letter')
        if row['id'] in ids:
            continue
        letter_data = parse(row)
        try:
            db.get_or_create(Letter, letter_data, ['id'], commit=False)
            db.session.flush()
        except Exception:
            db.session.rollback()
            traceback.print_exc()
            print('Raw Data', row)
            print('Letter Data', letter_data)
    db.session.commit()
    f.close()

