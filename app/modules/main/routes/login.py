from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user

from app import db
from app.models import User
from .. import bp, LoginForm, RegistrationForm


@bp.route('/login/', methods=['GET', 'POST'])
def login():
    target = redirect(url_for('main.index'))
    if current_user.is_authenticated:
        return target

    form = LoginForm()
    if not form.validate_on_submit():
        return render_template('login.html', form=form)

    user = db.session.query(User).filter_by(email=form.email.data).first()
    if user is None or not user.check_password(form.password.data):
        flash('Invalid username or password')
        return redirect(url_for('main.login'))

    login_user(user, remember=form.remember_me.data)
    flash('Connexion réussie')
    return target


@bp.route('/logout/')
def logout():
    logout_user()
    flash('Déconnexion réussie')
    return redirect(url_for('main.index'))


@bp.route('/register/', methods=['GET', 'POST'])
def register():
    target = redirect(url_for('main.index'))
    if current_user.is_authenticated:
        return target

    form = RegistrationForm()
    if not form.validate_on_submit():
        return render_template('register.html', form=form)

    user = User(email=form.email.data)
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    flash('Inscription réussie')
    login_user(user, remember=form.remember_me.data)
    return target
