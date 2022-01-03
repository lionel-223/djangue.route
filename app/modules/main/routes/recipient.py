from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user

from app import db
from app.models import User, Recipient, Language
from .. import bp, RecipientForm


@bp.route('/recipients/register/', methods=['GET', 'POST'])
def register_recipient():
    form = RecipientForm()
    if current_user.is_authenticated:
        del form.email
        del form.password
    if not form.validate_on_submit():
        return render_template('recipient.html', form=form)

    if not current_user.is_authenticated:
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
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
    flash('Inscription réussie!')
    return redirect(url_for('main.index'))
