from datetime import datetime, timedelta
from flask import render_template, request, flash


from app import db
from app.models import Letter, Recipient
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
            .filter(Letter.status == Letter.Status.not_moderated)
        ).count(),
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
    db.session.commit()
    return True, 200


@bp.route('/moderation-recipient/', methods=['GET', 'POST'])
def moderation_recipient():
    new_status = request.form.get('status', None)
    recipient_id = request.form.get('recipient_id', None)
    if new_status and recipient_id:
        new_status = Recipient.Status[new_status]
        recipient = db.session.query(Recipient).get(recipient_id)
        if recipient.status != Recipient.Status.not_moderated:
            flash('Oups ! Cet établissement avait déjà été modéré...')
        else:
            recipient.status = new_status
            db.session.commit()
    new_recipient = db.session.query(Recipient).filter(Recipient.status == Recipient.Status.not_moderated)\
        .order_by(Recipient.created_at).first()
    return render_template('admin/moderation_recipient.html', recipient=new_recipient)
