import importlib
import json
from pathlib import Path
from flask import Blueprint, Flask as BaseFlask, request
from flask.json import JSONEncoder
from flask.wrappers import Request
from flask_babel import Babel
from flask_login import LoginManager

from app import config

babel = Babel()
APP_FOLDER = Path(__file__).parent
MODULES_FOLDER = APP_FOLDER / 'modules'


@babel.localeselector
def get_locale():
    from app import db
    from app.models import Language

    return 'fr'
    cookie = request.cookies.get('lang')
    if cookie:
        return cookie
    langs = db.session.query(Language).filter_by(has_translations=True)
    return request.accept_languages.best_match([x.code for x in langs])


class MutableArgsRequest(Request):
    parameter_storage_class = dict


class StandardJSONEncoder(JSONEncoder):
    def default(self, obj):
        return json.dumps(obj, default=str)


class Flask(BaseFlask):
    # request_class = MutableArgsRequest
    json_encoder = StandardJSONEncoder

    def __init__(self, name=__name__, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.url_map.strict_slashes = False


class Blueprint(Blueprint):
    def __init__(self, module: str, /, prefix=None):
        module = module.removeprefix('app.modules.')
        path = module.split('.')
        if prefix is True:
            prefix = '/' + '/'.join(path)
        name = '_'.join(path)
        super().__init__(name, module, url_prefix=prefix)


def create_app():
    from app import db
    from app.models import User

    app = Flask()
    app.config['SECRET_KEY'] = config.SECRET_KEY
    babel.init_app(app)
    for module in MODULES_FOLDER.glob('./*/'):
        module = importlib.import_module(f'.{module.stem}', 'app.modules')
        app.register_blueprint(module.bp)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(int(user_id))

    return app
