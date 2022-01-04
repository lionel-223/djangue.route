from datetime import datetime, timedelta
from flask import render_template, request

from app import db
from app.models import Letter
from . import bp


@bp.route('/')
def index():
    today = datetime.utcnow()
    week_start = today - timedelta(days=today.weekday(), hours=today.hour, minutes=today.minute, seconds=today.second)
    stats = {
        'letters_count': db.session.query(Letter).count(),
        'letters_week_count': (
            db.session.query(Letter)
            .filter(Letter.created_at >= week_start)
        ).count(),
        'letters_unmoderated_count': (
            db.session.query(Letter)
            .filter(Letter.status == "not_moderated")
        ).count(),
    }
    return render_template('admin/dashboard.html', stats=stats)


@bp.route('/moderation', methods=['GET', 'POST'])
def moderation():
    new_status = request.form.get('status', None)
    letter_id = request.form.get('letter_id', None)
    if letter_id:
        letter = db.session.query(Letter).get(letter_id)
        letter.status = new_status
        db.session.commit()
    new_letter = db.session.query(Letter).filter(Letter.status == "not_moderated").order_by(Letter.created_at).first()
    return render_template('admin/moderation.html', letter=new_letter, post=request.form)
