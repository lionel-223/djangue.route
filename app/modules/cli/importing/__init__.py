import csv
import json
from pathlib import Path
import click

from app import IMPORT_FOLDER
from .. import bp


@bp.cli.group('import', invoke_without_command=True)
@click.pass_context
def group(ctx: click.Context):
    if ctx.invoked_subcommand:
        return
    import_all()


def import_all():
    from .download import download_all
    from .countries import import_countries
    from .languages import import_languages
    from .ehpads import import_ehpads

    download_all()
    print('Searching for files in', IMPORT_FOLDER)
    for file, func in {
        'countries.csv': import_countries,
        'languages.csv': import_languages,
        'ehpads.json': import_ehpads,
    }.items():
        file = IMPORT_FOLDER / file
        if not file.exists():
            print('No', file.name)
            continue
        print('Running script', func.__name__)
        func(file)


def read_file(path: Path, type=None) -> list[dict]:
    type = type or path.suffix[1:]
    func = {
        'json': json.load,
        'csv': lambda x: csv.DictReader(x.readlines(), skipinitialspace=True)
    }.get(type)
    if not func:
        raise Exception(f"Invalid type {type}")
    with path.expanduser().open() as f:
        data = func(f)
    return data


from . import download, ehpads, letters
