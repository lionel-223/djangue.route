#!/usr/bin/env python

from pathlib import Path
import click
import requests

from app import IMPORT_FOLDER
from . import group


COUNTRY_CODES_DATA_URL = 'https://gist.github.com/tadast/8827699/raw/f5cac3d42d16b78348610fc4ec301e9234f82821/countries_codes_and_coordinates.csv'
LANGUAGE_CODES_DATA_URL = 'https://github.com/datasets/language-codes/raw/master/data/language-codes.csv'


VALID_FILES = {
    'countries.csv': COUNTRY_CODES_DATA_URL,
    'languages.csv': LANGUAGE_CODES_DATA_URL,
}


def download_to(url: str, file: str, prefix = IMPORT_FOLDER, force=False):
    path = prefix / file
    if not force and path.exists():
        print(path, 'already exists, skipping...')
        return
    resp = requests.get(url)
    with (prefix / file).open('wb') as f:
        f.write(resp.content)


def download_all(force=False):
    for name, url in VALID_FILES.items():
        download_to(url, name, force=force)


@group.command('download')
@click.argument('name')
@click.option('-f', '--force', is_flag=True)
def download(name: str, force: bool):
    if name in VALID_FILES:
        download_to(VALID_FILES[name], name, force=force)
    else:
        download_all(force=force)
