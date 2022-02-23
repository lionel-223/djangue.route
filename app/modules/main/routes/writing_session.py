from flask import request, render_template, redirect, url_for, flash
from flask_login import current_user

import app
from app import db
from app.models import Letter, Upload, WritingSession
from app.utils.str_to_bool import strtobool
from .. import bp, WritingSessionForm


@bp.route('/writing-session/create/', methods=['GET', 'POST'])
def create_writing_session():
    form = WritingSessionForm()
    form.school_id.choices = [(school.id, school.name) for school in current_user.schools]
    if not form.validate_on_submit():
        return render_template('create_writing_session.html', form=form)

    writing_session = WritingSession(
        type=form.type.data,
        title=form.title.data,
        school_id=form.school_id.data,
        teacher_id=current_user.id,
    )
    db.session.add(writing_session)
    db.session.commit()
    return redirect(url_for('main.teacher_home'))
