from app import Blueprint


bp = Blueprint(__name__, prefix=True)

from . import index
