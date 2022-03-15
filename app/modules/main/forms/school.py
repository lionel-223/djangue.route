from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Optional

from app import db
from app.models import Country, Language, Recipient


class SchoolForm(FlaskForm):
    name = StringField("Nom de l'établissement", validators=[DataRequired()])
    address = StringField("Adresse", validators=[DataRequired()])
    zipcode = StringField("Code postal", validators=[DataRequired()])
    city = StringField("Ville", validators=[DataRequired()])
    country_code = SelectField("Pays", validators=[DataRequired()])
    languages = SelectMultipleField("Langue(s) parlée(s) au sein de l'établissement", validators=[DataRequired()])
    associated_recipient = SelectField("Jumelage avec un EHPAD", validators=[Optional()])
    submit = SubmitField("Enregistrer")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.country_code.choices = [
            (country.code, str(country)) for country
            in db.session.query(Country)
            if str(country)[0] != '<'  # Exclude untranslated countries
        ]
        self.languages.choices = [
            (language.code, str(language)) for language
            in db.session.query(Language)
        ]
        self.associated_recipient.choices = [
            (recipient.id, str(recipient)) for recipient
            in db.session.query(Recipient).filter(Recipient.type == Recipient.Types.retirement_home,
                                                  Recipient.associated_school is None)
        ]
