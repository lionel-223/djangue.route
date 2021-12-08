import importlib
import json
from pathlib import Path
from flask import Blueprint, Flask
from flask.json import JSONEncoder


APP_FOLDER = Path(__file__).parent
MODULES_FOLDER = APP_FOLDER / 'modules'


class StandardJSONEncoder(JSONEncoder):
    def default(self, obj):
        return json.dumps(obj, default=str)


class Blueprint(Blueprint):
    def __init__(self, module: str, /, prefix=None):
        module = module.removeprefix('app.modules.')
        path = module.split('.')
        if prefix == True:
            prefix = '/' + '/'.join(path)
        name = '_'.join(path)
        super().__init__(name, module, url_prefix=prefix)


def create_app():
    app = Flask(__name__)
    app.json_encoder = StandardJSONEncoder
    for module in MODULES_FOLDER.glob('./*/'):
        module = importlib.import_module(f'.{module.stem}', 'app.modules')
        app.register_blueprint(module.bp)
    return app
