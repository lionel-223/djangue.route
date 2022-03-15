from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import current_user, login_user, login_required

from app import db
from app.models import User, School, Language, Letter, Recipient
from app.utils.str_to_bool import strtobool
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
        recipient_id=form.associated_recipient.data or None,
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


@bp.get('/schools/<int:school_id>')
@login_required
def school_detail(school_id):
    school = db.session.get(School, school_id)
    if not school:
        abort(404)
    if school not in current_user.schools:
        abort(403)
    return render_template('school_detail.html', school=school)


@bp.get('/schools/search/')
def schools_search():
    search = request.args.get('term')
    if not search:
        return {'results': []}
    results = db.session.query(School).filter(School.name.ilike(f'%{search}%'))
    response = {'results': [{'id': school.id, 'text': school.name} for school in results]}
    return response


@bp.route('/schools/remove-current-user/<int:school_id>')
def remove_current_user_school(school_id):
    school = db.session.get(School, school_id)
    school.teachers.remove(current_user)
    db.session.commit()
    return redirect(url_for('main.user_home'))


@bp.route('/schools/correct-letter/<int:letter_id>/', methods=['GET', 'POST'])
def correct_letter(letter_id):
    letter = db.session.get(Letter, letter_id)
    if not letter:
        abort(404)
    if letter.writing_session not in current_user.writing_sessions:
        abort(403)
    if request.method == 'POST':
        session_id = letter.writing_session_id
        validate = strtobool(request.form.get('validate'))
        new_content = request.form.get('content')
        new_signature = request.form.get('signature')
        delete_image = request.form.get('delete_image', None)
        if validate:
            letter.content = new_content
            letter.signature = new_signature
            letter.status = Letter.Status.not_moderated
            if delete_image:
                letter.upload_hash = None
        else:
            letter.status = Letter.Status.rejected
            letter.writing_session_id = None
        db.session.commit()
        return redirect(url_for('main.writing_session_detail', session_id=session_id))
    return render_template('correct_letter.html', letter=letter)


@bp.route('/school/<int:school_id>/associate_recipient', methods=['GET', 'POST'])
def associate_recipient(school_id):
    school = db.session.get(School, school_id)
    if not school:
        abort(404)
    if school.associated_recipient or school not in current_user.schools:
        abort(403)
    target = redirect(url_for('main.school_detail', school_id=school_id))
    if request.method == 'POST':
        school.recipient_id = request.form.get('ehpad_id')
        db.session.commit()
        flash('Twinning created')
        return target
    ehpads = db.session.query(Recipient).filter(Recipient.type == Recipient.Types.retirement_home,
                                                Recipient.associated_school == None)
    if not ehpads.count():
        flash('Aucun EHPAD disponible pour un jumelage')
        return target
    return render_template('associate_recipient.html', school=school, ehpads=ehpads)
