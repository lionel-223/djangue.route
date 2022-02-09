from flask_login import current_user, login_required

from app import Blueprint


bp = Blueprint(__name__, prefix=True)


@bp.before_request
@login_required
def before_request():
    if not any(current_user.admin_accesses.values()):
        return "no admin access"


from .forms.article import ArticleForm
from .routes import index, moderation, article
