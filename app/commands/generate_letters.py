import click
import json

from . import bp
from app.modules.generation import (
    LetterSchema, pdf_from_letters
)


@bp.cli.command('generate')
@click.option('-d', '--data')
def generate(data):
    letters = None

    if data:
        def normalize(d):
            if 'joined_content' in d and not 'signature' in d:
                d['content'] = d.pop('joined_content')
                if 'greeting' in d:
                    d.pop('greeting')
            d['image_url'] = d.pop('image')
            return d
        with open(data) as f:
            data = json.load(f)
        letters = (LetterSchema(raw_dict=normalize(x)) for x in data)
    if not letters:
        raise Exception('No letters')
    result = pdf_from_letters(letters=letters)
    with open('output.pdf', 'wb') as f:
        f.write(result)
