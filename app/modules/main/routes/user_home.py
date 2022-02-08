from flask import render_template, redirect, url_for, abort
from flask_login import current_user, login_required

from app import db
from app.models import User, Recipient
from .. import bp


@bp.get('/user/home/')
@login_required
def user_home():
    if current_user.recipients.count() > 0:
        return redirect(url_for('main.recipient_home'))
    if len(current_user.schools) > 0:
        return redirect(url_for('main.teacher_home'))
    if current_user.can_moderate:
        return redirect(url_for('admin.index'))
    return 404


@bp.get('/user/recipients/')
@login_required
def recipient_home():
    ehpads = current_user.recipients.filter_by(type=Recipient.Types.retirement_home)
    associations = current_user.recipients.filter_by(type=Recipient.Types.association)
    if ehpads.count() + associations.count() == 0:
        abort(404)
    return render_template('recipient_home.html', ehpads=ehpads, associations=associations)


@bp.get('/user/schools/')
@login_required
def teacher_home():
    schools = current_user.schools
    if len(schools) == 0:
        abort(404)
    return render_template('teacher_home.html', schools=schools)
