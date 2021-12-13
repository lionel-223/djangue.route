from flask import render_template, redirect, url_for, flash

from . import bp
from app import db
from app.forms import LetterForm
from app.models import Letter


@bp.route('/ecrivez-une-lettre', methods=['GET', 'POST'])
def write_letter():
    form = LetterForm()
    if form.validate_on_submit():
        letter = Letter(
            language_code=form.language_code.data,
            greeting_id=form.greeting_id.data,
            content=form.content.data,
            signature=form.signature.data,
            email=form.email.data,
            country_code=form.country_code.data,
            zipcode=form.zipcode.data,
            specific_recipient_id=form.specific_recipient_id.data,
            allow_reuse=form.allow_reuse.data
        )
        db.session.add(letter)
        db.session.commit()
        flash('Letter saved')
        return redirect(url_for('main.index'))
    return render_template('letter_form.html', title='Ecrivez une lettre', form=form)
