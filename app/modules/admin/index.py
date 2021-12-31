from datetime import datetime, timedelta
from flask import render_template

from app import db
from app.models import Letter
from . import bp


@bp.route('/')
def index():
    today = datetime.utcnow()
    week_start = today - timedelta(days=today.weekday())
    stats = {
        'letters_count': db.session.query(Letter).count(),
        'letters_week_count': (
            db.session.query(Letter)
            .filter(Letter.created_at >= week_start)
        ).count(),
        'letters_unmoderated_count': '/',
    }
    return render_template('admin/dashboard.html', stats=stats)

@bp.route('/moderation')
def moderation():
    return 'Modération'
