import os
import json

from flask import render_template, redirect, url_for, flash, abort, send_from_directory, request
from flask_login import current_user, login_user, login_required

import app
from app import db
from app.models import User, Recipient, Language, Package
from app.utils.pagination import paginate
from .. import bp, RecipientForm


@bp.route('/recipients/register/', methods=['GET', 'POST'])
@login_required
def register_recipient():
    form = RecipientForm()
    if not form.validate_on_submit():
        return render_template('register_recipient.html', form=form)

    recipient = Recipient(
        type=form.type.data,
        name=form.name.data,
        address=form.address.data,
        zipcode=form.zipcode.data,
        city=form.city.data,
        country_code=form.country_code.data,
        languages=[db.session.get(Language, x) for x in form.languages.data or []],
        frequency=form.frequency.data or None,
        nb_letters=form.nb_letters.data or None,
    )
    recipient.users.append(current_user)
    db.session.add(recipient)
    db.session.commit()
    flash('Inscription réussie !')
    return redirect(url_for('main.recipient_home'))


@bp.route('/recipients/join/', methods=['GET', 'POST'])
@login_required
def join_existing_recipient():
    if request.method == 'GET':
        return render_template('join_recipient.html')
    recipient_id = request.values.get('recipient_id')
    recipient = db.session.get(Recipient, recipient_id)
    if not recipient:
        flash('This recipient does not exist !')
        return render_template('join_recipient.html')
    if recipient in current_user.recipients:
        flash('You already belong to this recipient !')
        return render_template('join_recipient.html')
    current_user.recipients.append(recipient)
    db.session.commit()
    flash('Inscription réussie !')
    return redirect(url_for('main.recipient_home'))


@bp.route('/recipients/edit/<int:recipient_id>/', methods=['GET', 'POST'])
@login_required
def edit_recipient(recipient_id):
    recipient = db.session.get(Recipient, recipient_id)
    if not recipient:
        abort(404)
    if not (current_user in recipient.users or current_user.can_edit_recipients):
        abort(403)
    form = RecipientForm(obj=recipient)
    form.languages.data = [language.code for language in recipient.languages]
    del form.type
    if not form.validate_on_submit():
        return render_template('register_recipient.html', form=form, recipient=recipient)
    recipient.name = form.name.data
    recipient.address = form.address.data
    recipient.zipcode = form.zipcode.data
    recipient.city = form.city.data
    recipient.country_code = form.country_code.data
    recipient.languages = [db.session.get(Language, x) for x in form.languages.data or []]
    recipient.frequency = form.frequency.data or None
    recipient.nb_letters = form.nb_letters.data or None
    db.session.commit()
    flash('Modifications enregistrées !')
    return redirect(url_for('main.recipient_detail', recipient_id=recipient_id))


@bp.get('/recipient/<int:recipient_id>/')
@login_required
def recipient_detail(recipient_id):
    recipient = db.session.get(Recipient, recipient_id)
    if not recipient:
        abort(404)
    if not (current_user in recipient.users or current_user.can_edit_recipients):
        abort(403)
    page = int(request.args.get('page', 1))
    packages = paginate(db.session.query(Package).filter_by(recipient_id=recipient_id), page, 10)
    return render_template('recipient_detail.html', recipient=recipient, packages=packages)


@bp.get('/download-package/<int:package_id>/')
@login_required
def download_package(package_id):
    package = db.session.get(Package, package_id)
    if not package:
        abort(404)
    recipient = db.session.get(Recipient, package.recipient_id)
    if not (current_user in recipient.users or current_user.can_edit_recipients):
        abort(403)
    pdf_folder = app.PDF_UPLOAD_FOLDER
    date_package = package.created_at
    package_directory = os.path.join(pdf_folder, str(date_package.year), str(date_package.month))
    return send_from_directory(package_directory, package.file)


@bp.get('/recipients/search/')
def recipients_search():
    search = request.args.get('term')
    if not search:
        return {'results': []}
    results = db.session.query(Recipient).filter(Recipient.name.ilike(f'%{search}%'))
    response = {'results': [{'id': recipient.id, 'text': recipient.name} for recipient in results]}
    return response


@bp.route('/recipients/remove_current_user/<int:recipient_id>')
def remove_current_user_recipient(recipient_id):
    recipient = db.session.get(Recipient, recipient_id)
    recipient.users.remove(current_user)
    db.session.commit()
    return redirect(url_for('main.user_home'))