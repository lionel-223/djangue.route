from flask import render_template, redirect, url_for, flash, request
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


@bp.route('/schools/join/', methods=['GET', 'POST'])
@login_required
def join_existing_school():
    if request.method == 'GET':
        return render_template('join_school.html')
    school_id = request.values.get('school_id')
    school = db.session.get(School, school_id)
    if not school:
        flash('This school does not exist !')
        return render_template('join_school.html')
    if school in current_user.schools:
        flash('You already belong to this school !')
        return render_template('join_school.html')
    current_user.schools.append(school)
    db.session.commit()
    flash('Inscription réussie !')
    return redirect(url_for('main.teacher_home'))


@bp.get('/schools/search/')
def schools_search():
    search = request.args.get('term')
    if not search:
        return {'results': []}
    results = db.session.query(School).filter(School.name.ilike(f'%{search}%'))
    response = {'results': [{'id': school.id, 'text': school.name} for school in results]}
    return response


@bp.route('/schools/remove_current_user/<int:school_id>')
def remove_current_user_school(school_id):
    school = db.session.get(School, school_id)
    school.teachers.remove(current_user)
    db.session.commit()
    return redirect(url_for('main.user_home'))
