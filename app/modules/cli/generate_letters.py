from pathlib import Path
import click
import json

from . import bp
from app.modules.generation import (
    LetterSchema, pdf_from_letters
)


@bp.cli.command('generate')
@click.argument('file', type=Path)
def generate(file):
    def normalize(d):
        if 'joined_content' in d and not 'signature' in d:
            d['content'] = d.pop('joined_content')
            if 'greeting' in d:
                d.pop('greeting')
        d['image_url'] = d.pop('image')
        return d

    with file.open() as f:
        data = json.load(f)

    letters = (LetterSchema(raw_dict=normalize(x)) for x in data)
    result = pdf_from_letters(letters=letters)
    output = Path('./output.pdf')
    with output.open('wb') as f:
        f.write(result)
    print('Wrote file to', output)
