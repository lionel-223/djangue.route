from flask import render_template, redirect, url_for, abort, request, flash
from flask_login import current_user, login_required

from app import db
from app.models import User, Recipient, WritingSession
from app.utils.pagination import paginate
from .. import bp


@bp.get('/user/home/')
@login_required
def user_home():
    if current_user.recipients.count() + current_user.pending_recipients.count() > 0:
        return redirect(url_for('main.recipient_home'))
    if len(current_user.schools) > 0:
        return redirect(url_for('main.teacher_home'))
    if current_user.can_moderate:
        return redirect(url_for('admin.index'))
    flash('Votre espace personnel est vide. '
          'Inscrivez votre EHPAD, association ou établissement scolaire, ou rejoignez-en un existant.')
    return redirect(url_for('main.index'))


@bp.get('/user/recipients/')
@login_required
def recipient_home():
    recipients = current_user.recipients
    pending_recipients = current_user.pending_recipients
    if recipients.count() + pending_recipients.count() == 0:
        abort(404)
    return render_template('recipient_home.html', recipients=recipients, pending_recipients=pending_recipients)


@bp.get('/user/schools/')
@login_required
def teacher_home():
    schools = current_user.schools
    if len(schools) == 0:
        abort(404)
    page = int(request.args.get('page', 1))
    writing_sessions = paginate(db.session.query(WritingSession).filter_by(teacher=current_user), page, 10)
    return render_template('teacher_home.html', schools=schools, writing_sessions=writing_sessions)
