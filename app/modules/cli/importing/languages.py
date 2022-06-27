from pathlib import Path

import click
from app import IMPORT_FOLDER, db
from app.models import Language
from app.utils.model import Model
from . import group, read_file


DEFAULT_LETTER_LANGUAGES = ['en', 'fr', 'nl', 'es', 'de']


class LanguageModel(Model):
    code = Model.getter('alpha2')

    @staticmethod
    def accepts_letters(d: dict):
        return d.get('code') in DEFAULT_LETTER_LANGUAGES


def import_languages(path: Path):
    data = read_file(path)
    for entry in data:
        obj_dict = LanguageModel.dict(entry)
        obj_db = db.get_or_create(Language, obj_dict, ['code'])
        if db.Action.is_created():
            print('Added', obj_db)


@group.command()
@click.argument('path', type=Path, default=IMPORT_FOLDER / 'languages.csv')
def languages(path: Path):
    import_languages(path)
