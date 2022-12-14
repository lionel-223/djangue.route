from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from app import db
from app.models import User
from .. import bp, LoginForm, RegistrationForm


@bp.route('/login/', methods=['GET', 'POST'])
def login():
    target = request.args.get('next')
    if not target or url_parse(target).netloc != '':
        target = url_for('main.user_home')
    if current_user.is_authenticated:
        return redirect(target)

    form = LoginForm()
    if not form.validate_on_submit():
        return render_template('login.html', form=form)

    user = db.session.query(User).filter_by(email=form.email.data).first()
    if user is None or not user.check_password(form.password.data):
        flash('Email ou mot de passe invalide')
        return redirect(url_for('main.login'))

    login_user(user, remember=form.remember_me.data)
    flash('Connexion réussie')
    return redirect(target)


@bp.route('/logout/')
def logout():
    logout_user()
    flash('Déconnexion réussie')
    return redirect(url_for('main.index'))


@bp.route('/register/', methods=['GET', 'POST'])
def register():
    target = request.args.get('next')
    if not target or url_parse(target).netloc != '':
        target = url_for('main.index')
    if current_user.is_authenticated:
        return redirect(target)

    form = RegistrationForm()
    if not form.validate_on_submit():
        return render_template('register.html', form=form)

    user = User(email=form.email.data)
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    flash('Inscription réussie')
    login_user(user, remember=form.remember_me.data)
    return redirect(target)
