from datetime import datetime, timedelta, date
from flask import current_app, render_template
from flask_login import current_user


from app import db
from app.models import Letter, Recipient
from .. import bp


def get_count_per_year():
    results = {}
    today = date.today()
    this_year = today.year
    year = this_year
    while True:
        min = datetime(year, 1, 1)
        max = datetime(year + 1, 1, 1)
        count = (
            db.session.query(Letter)
            .with_entities(Letter.id)
            .filter(Letter.created_at >= min, Letter.created_at <= max)
        ).count()
        if count == 0:
            break
        results[year] = count
        year -= 1
    return results


@bp.route('/')
def index():
    today = datetime.utcnow()
    week_start = today - timedelta(days=today.weekday(), hours=today.hour, minutes=today.minute, seconds=today.second)
    stats = {
        'letters_count': db.session.query(Letter).count(),
        'per_year_count': get_count_per_year(),
        'letters_week_count': (
            db.session.query(Letter)
            .filter(Letter.created_at >= week_start)
        ).count(),
        'letters_moderated_week_count': (
            db.session.query(Letter)
            .filter((Letter.moderation_time >= week_start) &
                    (Letter.status.in_([Letter.Status.approved, Letter.Status.rejected])))
        ).count(),
        'letters_unmoderated_count': (
            db.session.query(Letter)
            .filter(Letter.status == Letter.Status.not_moderated)
        ).count(),
        'ehpad_count': db.session.query(Recipient).filter_by(type=Recipient.Types.RETIREMENT_HOME).count(),
        'associations_count': db.session.query(Recipient).filter_by(type=Recipient.Types.ASSOCIATION).count(),
        'unique_emails_count': db.session.query(Letter).distinct(Letter.email).count(),
    }
    user_moderated_letters = db.session.query(Letter).filter(
        (Letter.moderator == current_user),
        (Letter.status.in_([Letter.Status.approved, Letter.Status.rejected]))
    )
    user_moderation_week_count = user_moderated_letters.filter(Letter.moderation_time >= week_start).count()
    user_accepted_count = user_moderated_letters.filter_by(status=Letter.Status.approved).count()
    if user_moderated_letters.count() > 0:
        stats['user_moderation_count'] = user_moderated_letters.count()
        stats['user_moderation_week_count'] = user_moderation_week_count
        stats['user_pct_accepted'] = round(100 * user_accepted_count / user_moderated_letters.count())

    available_routes = current_app.url_map
    return render_template('admin/dashboard.html', stats=stats, available_routes=available_routes)
