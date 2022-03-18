from app import Blueprint

bp = Blueprint('cli', __name__)

from . import generate_packages, import_legacy_data
