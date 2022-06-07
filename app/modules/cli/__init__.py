from app import Blueprint

bp = Blueprint(__name__)

from . import (
    generate_letters,
    generate_packages,
    import_legacy_data,
    importing,
)
