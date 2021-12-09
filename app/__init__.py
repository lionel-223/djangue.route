import importlib
import json
from pathlib import Path
from flask import Blueprint, Flask, request
from flask.json import JSONEncoder
from flask_babel import Babel


babel = Babel()
APP_FOLDER = Path(__file__).parent
MODULES_FOLDER = APP_FOLDER / 'modules'


@babel.localeselector
def get_locale():
    from app import db
    from app.models import Language

    cookie = request.cookies.get("lang")
    if cookie:
        return cookie
    langs = db.session.query(Language).filter_by(has_translations=True)
    return request.accept_languages.best_match([x.code for x in langs])


class StandardJSONEncoder(JSONEncoder):
    def default(self, obj):
        return json.dumps(obj, default=str)


class Blueprint(Blueprint):
    def __init__(self, module: str, /, prefix=None):
        module = module.removeprefix('app.modules.')
        path = module.split('.')
        if prefix is True:
            prefix = '/' + '/'.join(path)
        name = '_'.join(path)
        super().__init__(name, module, url_prefix=prefix)


def create_app():
    app = Flask(__name__)
    app.json_encoder = StandardJSONEncoder
    babel.init_app(app)
    for module in MODULES_FOLDER.glob('./*/'):
        module = importlib.import_module(f'.{module.stem}', 'app.modules')
        app.register_blueprint(module.bp)
    return app
