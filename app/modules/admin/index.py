from . import bp


@bp.route('/')
def index():
    return 'Hello admin'

@bp.route('/moderation')
def moderation():
    return 'Modération'
