#!/bin/env python
import csv
import requests

from app import db
from app.models import Country, Language


COUNTRY_CODES_DATA_URL = 'https://gist.github.com/tadast/8827699/raw/f5cac3d42d16b78348610fc4ec301e9234f82821/countries_codes_and_coordinates.csv'
LANGUAGE_CODES_DATA_URL = 'https://github.com/datasets/language-codes/raw/master/data/language-codes.csv'

country_codes = requests.get(COUNTRY_CODES_DATA_URL).text
reader = csv.DictReader(country_codes.splitlines(), skipinitialspace=True)
codes = (x['Alpha-2 code'] for x in reader)
for code in codes:
    print('Adding', code, 'to countries')
    db.get_or_create(Country, code=code)
db.session.commit()

language_codes = requests.get(LANGUAGE_CODES_DATA_URL).text
reader = csv.DictReader(language_codes.splitlines())
codes = (x['alpha2'] for x in reader)
for code in codes:
    print('Adding', code, 'to languages')
    db.get_or_create(Language, code=code)
db.session.commit()
