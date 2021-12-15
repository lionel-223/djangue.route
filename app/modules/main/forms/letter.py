from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, SelectField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Optional

from app import db, get_locale
from app.models import Greeting, Language, Recipient, Country


class LetterForm(FlaskForm):
    language_code = SelectField("Langue", validators=[DataRequired()], default=get_locale)
    greeting_id = SelectField("Salutation", coerce=int, validators=[DataRequired()])
    content = TextAreaField("Contenu", validators=[DataRequired(), Length(min=120)])
    signature = StringField("Signature", validators=[DataRequired()])
    upload = FileField("Photo", validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    email = StringField("Email", validators=[DataRequired(), Email()])
    country_code = SelectField("Pays", validators=[DataRequired()])
    zipcode = StringField("Code postal")
    specific_recipient_id = SelectField("Destinatation", validators=[Optional()], default='')
    terms_agreement = BooleanField("J'accepte les conditions", validators=[DataRequired()])
    allow_reuse = BooleanField("J'autorise l'utilisation de ma lettre anonymisée sur les réseaux sociaux")
    submit = SubmitField("Envoyer")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.greeting_id.choices = [
            (greeting.id, str(greeting)) for greeting in db.session.query(Greeting)
        ]
        self.language_code.default = get_locale
        self.language_code.choices = [
            (language.code, str(language)) for language in
            db.session.query(Language).filter_by(accepts_letters=True)
        ]
        self.specific_recipient_id.choices = [
            (recipient.id, recipient.name) for recipient
            in db.session.query(Recipient).filter_by(receives_letters=True)
        ] + [('', "Au hasard")]
        self.country_code.choices = [
            (country.code, str(country)) for country
            in db.session.query(Country)
        ]
