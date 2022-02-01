import importlib
import json
import os
from pathlib import Path
from flask import Blueprint, Flask as BaseFlask, request
from flask.json import JSONEncoder
from flask_assets import Environment, Bundle
from flask_babel import Babel
from flask_login import LoginManager

from app import config

assets = Environment()
babel = Babel()
APP_FOLDER = Path(__file__).parent
MODULES_FOLDER = APP_FOLDER / 'modules'
PDF_UPLOAD_FOLDER = os.path.join(APP_FOLDER, 'uploads', 'letter_packages')


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


class StandardJSONEncoder(JSONEncoder):
    def default(self, obj):
        return json.dumps(obj, default=str)


class Flask(BaseFlask):
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


def register_assets(assets):
    bundles_dir = APP_FOLDER / 'static' / 'bundles'
    for bundle_dir in bundles_dir.glob('*/'):
        file_type = bundle_dir.stem
        bundle_name = f'bundle.{file_type}'
        bundle = Bundle(
            *[str(x) for x in bundle_dir.glob(f'**/*.{file_type}')],
            output=bundle_name,
            filters={'css': 'cssmin'}.get(file_type),
        )
        assets.register(file_type, bundle)


def create_app():
    from app import db, commands
    from app.models import User

    app = Flask()
    app.config['SECRET_KEY'] = config.SECRET_KEY
    register_assets(assets)
    assets.init_app(app)
    babel.init_app(app)
    for module in MODULES_FOLDER.glob('./*/'):
        module = importlib.import_module(f'.{module.stem}', 'app.modules')
        app.register_blueprint(module.bp)
    app.register_blueprint(commands.bp)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    init_static_data()

    return app


def init_static_data():
    for script in ['import_countries_and_langs']:
        module = importlib.import_module(f'scripts.{script}')
        module.main()
