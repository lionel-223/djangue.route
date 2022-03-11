import bdb

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

from app import db
from app.models import WritingSession, Language


class WritingSessionForm(FlaskForm):
    type = SelectField('Type de session', validators=[DataRequired()])
    title = StringField('Titre de la session', validators=[DataRequired()])
    school_id = SelectField('Etablissement concerné', validators=[DataRequired()], coerce=int)
    language = SelectField('Langue', validators=[DataRequired()])
    submit = SubmitField('Créer')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type.choices = [
            (type.name, str(type)) for type in WritingSession.Type
        ]
        self.language.choices = [
            (language.code, str(language)) for language
            in db.session.query(Language)
        ]