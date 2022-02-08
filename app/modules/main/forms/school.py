from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, SelectMultipleField, PasswordField
from wtforms.validators import DataRequired, Email, Optional, NumberRange

from app import db
from app.models import Country, Language


class SchoolForm(FlaskForm):
    name = StringField("Nom de l'établissement", validators=[DataRequired()])
    address = StringField("Adresse", validators=[DataRequired()])
    zipcode = StringField("Code postal", validators=[DataRequired()])
    city = StringField("Ville", validators=[DataRequired()])
    country_code = SelectField("Pays", validators=[DataRequired()])
    languages = SelectMultipleField("Langue(s) parlée(s) au sein de l'établissement", validators=[DataRequired()])
    submit = SubmitField("Enregistrer")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.country_code.choices = [
            (country.code, str(country)) for country
            in db.session.query(Country)
            if str(country)[0] != '<' # Exclude untranslated countries
        ]
        self.languages.choices = [
            (language.code, str(language)) for language
            in db.session.query(Language).filter_by(accepts_letters=True)
        ]
