from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, SelectField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Optional

from app import db
from app.models import Greeting, Language, Recipient, Country


class LetterForm(FlaskForm):
    language_code = SelectField("Language", validators=[DataRequired()])
    greeting_id = SelectField("Greeting", coerce=int, validators=[DataRequired()])
    content = TextAreaField("Letter body", validators=[DataRequired(), Length(min=120)])
    signature = StringField("Signature", validators=[DataRequired()])
    upload = FileField("Attachment", validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    email = StringField("Email", validators=[DataRequired(), Email()])
    country_code = SelectField("Country", validators=[DataRequired()])
    zipcode = StringField("Zipcode")
    specific_recipient_id = SelectField("I want my letter to be sent to :", validators=[Optional()])
    terms_agreement = BooleanField("I agree to the terms and conditions", validators=[DataRequired()])
    allow_reuse = BooleanField("I allow my letter to be published on social media")
    submit = SubmitField("Send letter")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.greeting_id.choices = [
            (greeting.id, str(greeting)) for greeting in db.session.query(Greeting)
        ]
        self.language_code.choices = [
            (language.code, str(language)) for language in db.session.query(Language).filter_by(accepts_letters=True)
        ]
        self.specific_recipient_id.choices = [
            (recipient.id, recipient.name) for recipient in db.session.query(Recipient).filter_by(receives_letters=True)
        ]
        self.country_code.choices = [
            (country.code, str(country)) for country in db.session.query(Country)
        ]
