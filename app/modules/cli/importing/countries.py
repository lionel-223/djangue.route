from pathlib import Path

import click
from app import IMPORT_FOLDER, db
from app.models import Country

from app.utils.model import Model
from . import group, read_file


class CountryModel(Model):
    code = Model.getter('Alpha-2 code')
    name = Model.getter('Country')


def import_countries(path: Path):
    data = read_file(path)
    for entry in data:
        obj_dict = CountryModel.dict(entry)
        obj_db = db.get_or_create(Country, obj_dict, ['code'])
        if db.Action.is_created():
            print('Added', obj_db)


@group.command()
@click.argument('path', type=Path, default=IMPORT_FOLDER / 'countries.csv')
def countries(path: Path):
    import_countries(path)
