from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, SelectMultipleField, PasswordField
from wtforms.validators import DataRequired, Email, Optional, NumberRange

from app import db
from app.models import Country, Language, Recipient


class RecipientForm(FlaskForm):
    type = SelectField("Type d'entité", validators=[DataRequired()])
    name = StringField("Nom de l'entité", validators=[DataRequired()])
    address = StringField("Adresse", validators=[DataRequired()])
    zipcode = StringField("Code postal", validators=[DataRequired()])
    city = StringField("Ville", validators=[DataRequired()])
    country_code = SelectField("Pays", validators=[DataRequired()])
    languages = SelectMultipleField("Langue(s) acceptée(s) pour les lettres", validators=[DataRequired()])
    frequency = IntegerField("Nombre de mois entre chaque réception de lettres", default=1)
    nb_letters = IntegerField("Nombre de lettres par envoi", default=20, validators=[Optional(), NumberRange(max=200)])
    submit = SubmitField("Enregistrer")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type.choices = [
            (recipient_type.name, str(recipient_type)) for recipient_type
            in Recipient.Types
        ]
        self.country_code.choices = [
            (country.code, str(country)) for country
            in db.session.query(Country)
            if str(country)[0] != '<' # Exclude untranslated countries
        ]
        self.languages.choices = [
            (language.code, str(language)) for language
            in db.session.query(Language).filter_by(accepts_letters=True)
        ]
