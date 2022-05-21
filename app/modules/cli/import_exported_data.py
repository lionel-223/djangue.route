"""
Exported data refers to data exported in a readable and digest format, using
column names that are the same as the ones of the new db, or close to them
"""

import functools
import traceback
from typing import Type
import click
import csv
from datetime import datetime

from app import db
from app.models import Country, Letter
from . import bp
from scripts.import_countries_and_langs import get_countries_data


@functools.cache
def generate_country_matcher(countries_data):
    code_by_name = {x['Country']: x['Alpha-2 code'] for x in countries_data}
    def matcher(name: str):
        return (
            db.session.query(Country)
            .filter_by(code=code_by_name.get(name))
        ).first()
    return matcher


def parse(row: dict, country_matcher):
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
        'country': country_matcher(get('country')),
        'language_code': get('language_code'),
    }

@bp.cli.command('import-exported')
@click.argument('path')
def import_exported_file(path: str):
    ids = [x.id for x in db.session.query(Letter).with_entities(Letter.id)]
    ids = set(ids)
    countries_data = get_countries_data()
    country_matcher = generate_country_matcher(countries_data)
    f = open(path)
    reader = csv.DictReader(f)
    data = reader
    for i, row in enumerate(data):
        if i % 1000 == 0:
            print(f'Importing {i}th letter')
        if row['id'] in ids:
            continue
        letter_data = parse(row, country_matcher)
        try:
            db.get_or_create(Letter, {'id': letter_data['id']}, letter_data, commit=False)
            db.session.flush()
        except Exception:
            db.session.rollback()
            traceback.print_exc()
            print('Raw Data', row)
            print('Letter Data', letter_data)
    db.session.commit()
    f.close()

