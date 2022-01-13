from datetime import datetime, timedelta
from flask import render_template, request, flash
from flask_login import current_user


from app import db
from app.models import Letter, Recipient
from . import bp


@bp.route('/')
def index():
    today = datetime.utcnow()
    week_start = today - timedelta(days=today.weekday(), hours=today.hour, minutes=today.minute, seconds=today.second)
    user_moderation_count = len(current_user.moderated_letters)
    user_accepted_count = db.session.query(Letter).filter_by(moderator=current_user,
                                                             status=Letter.Status.approved).count()
    stats = {
        'letters_count': db.session.query(Letter).count(),
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
        'ehpad_count': db.session.query(Recipient).filter_by(type=Recipient.Types.retirement_home).count(),
        'associations_count': db.session.query(Recipient).filter_by(type=Recipient.Types.association).count(),
        'user_moderation_count': user_moderation_count,
        'user_moderation_week_count':
            db.session.query(Letter).filter((Letter.moderator == current_user)
                                            & (Letter.moderation_time >= week_start)).count(),
        'user_pct_accepted':
            round(100 * user_accepted_count / user_moderation_count),
    }
    return render_template('admin/dashboard.html', stats=stats)


@bp.route('/moderation/', methods=['GET', 'POST'])
def moderation():
    new_status = request.form.get('status', None)
    letter_id = request.form.get('letter_id', None)
    if letter_id and new_status:
        new_status = Letter.Status[new_status]
        letter = db.session.query(Letter).get(letter_id)
        if letter.status != Letter.Status.not_moderated:
            flash('Oups ! Cette lettre avait déjà été modérée...')
        else:
            letter.status = new_status
            letter.moderation_time = datetime.utcnow()
            db.session.commit()
    new_letter = (
        db.session.query(Letter)
        .filter((Letter.status == Letter.Status.not_moderated) &
                ((Letter.moderation_time == None) | (Letter.moderation_time <= datetime.utcnow() - timedelta(hours=1))))
        .order_by(Letter.created_at).first()
    )
    if new_letter:
        new_letter.moderation_time = datetime.utcnow()
        new_letter.moderator = current_user
        db.session.commit()
    return render_template('admin/moderation.html', letter=new_letter)


@bp.post('/moderation/unlock_letter/<int:letter_id>')
def unlock_letter(letter_id):
    """
    When a moderator leaves the moderation interface, the letter he was reviewing must have its
    'moderation_time' set to None to avoid it being considered as currently under review.
    """
    letter = db.session.get(Letter, letter_id)
    letter.moderation_time = None
    letter.moderator = None
    db.session.commit()
    return True, 200
