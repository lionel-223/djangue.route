from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, SelectField, TextAreaField, BooleanField, HiddenField, RadioField
from wtforms.validators import DataRequired, Email, Length, InputRequired

from app import db, get_locale
from app.models import Language, Recipient, Country


class LetterForm(FlaskForm):
    language_code = SelectField(validators=[DataRequired()], default=get_locale)
    is_male = SelectField(validators=[InputRequired()], coerce=lambda x: bool(int(x)))
    greeting = StringField(validators=[DataRequired()])
    content = TextAreaField(validators=[DataRequired(), Length(min=120)])
    signature = StringField(validators=[DataRequired()])
    upload = FileField(validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    email = StringField(validators=[DataRequired(), Email()])
    country_code = SelectField(validators=[DataRequired()])
    zipcode = StringField()
    specific_recipient_bool = RadioField(
        choices=[("false", "Non"), ("true", "Oui")],
        default="false",
    )
    specific_recipient_name = StringField(render_kw={'readonly': True})
    specific_recipient_id = HiddenField()
    terms_agreement = BooleanField(validators=[DataRequired()])
    allow_reuse = BooleanField()
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_male.choices = [
            ("1", "Un homme"),
            ("0", "Une femme"),
        ]
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
            if str(country)[0] != '<'  # Exclude untranslated countries
        ]
