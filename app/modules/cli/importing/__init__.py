import json
from pathlib import Path
import click

from app import APP_FOLDER
from .. import bp


@bp.cli.group('import', invoke_without_command=True)
@click.pass_context
def group(ctx: click.Context):
    if ctx.invoked_subcommand:
        return
    import_all()


def import_all():
    from .ehpads import import_ehpads

    folder = APP_FOLDER.parent / 'import'
    print('Searching for files in', folder)
    for file in folder.rglob('*'):
        name = file.name
        func = {
            'ehpads.json': import_ehpads,
        }.get(name)
        print('Found', name)
        if func:
            func(file)
        else:
            print('No matching import script for', name)


def read_file(path: Path) -> dict:
    with path.expanduser().open() as f:
        data = json.load(f)
    return data


from . import ehpads, letters
