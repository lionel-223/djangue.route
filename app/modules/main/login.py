from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required

from . import bp
from app import db
from app.forms import LoginForm
from app.models import User


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me.data)
        flash('Connexion réussie')
        return redirect(url_for('main.index'))
    return render_template('login.html', title='Connexion', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    flash('Déconnexion réussie')
    return redirect(url_for('main.index'))
