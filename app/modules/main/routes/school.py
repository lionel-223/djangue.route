from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_user, login_required

from app import db
from app.models import User, School, Language
from .. import bp, SchoolForm


@bp.route('/schools/register/', methods=['GET', 'POST'])
@login_required
def register_school():
    form = SchoolForm()
    if not form.validate_on_submit():
        return render_template('register_school.html', form=form)

    school = School(
        name=form.name.data,
        address=form.address.data,
        zipcode=form.zipcode.data,
        city=form.city.data,
        country_code=form.country_code.data,
        languages=[db.session.get(Language, x) for x in form.languages.data or []],
    )
    school.teachers.append(current_user)
    db.session.add(school)
    db.session.commit()
    flash('Inscription réussie !')
    return redirect(url_for('main.teacher_home'))
