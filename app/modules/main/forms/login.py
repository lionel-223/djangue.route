from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import ValidationError, DataRequired, Email

from app import db
from app.models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember_me = BooleanField('Se souvenir de moi')
    submit = SubmitField('Se connecter')


class RegistrationForm(LoginForm):
    submit = SubmitField("S'inscrire")

    def validate_email(self, email):
        user = db.session.query(User).filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Cet email est déjà utilisé')
