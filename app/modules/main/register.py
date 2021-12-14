from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required

from . import bp
from app import db
from app.forms import RegistrationForm
from app.models import User


@bp.route('/inscription', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Inscription réussie')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Inscription', form=form)
