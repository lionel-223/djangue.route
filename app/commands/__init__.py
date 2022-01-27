from app import Blueprint

bp = Blueprint('cli', __name__)

from .generate_packages import generate_packages
