import flask

import app
from .schema import LetterSchema


LOGO_PATH = app.APP_FOLDER / 'static' / 'logo' / 'logo-150x.png'
CSS_PATH = app.APP_FOLDER / 'static' / 'generation' / 'letter.css'


def render_letter(letter: LetterSchema):
    return flask.render_template(
        'generation/letter.html',
        letter=letter,
        logo_path=LOGO_PATH,
        css_path=CSS_PATH,
    )
