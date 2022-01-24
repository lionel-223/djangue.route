from flask import render_template, redirect, url_for, flash

from app import db
from app.models import Letter
from .. import bp, LetterForm


@bp.route('/write-young/', methods=['GET', 'POST'])
@bp.route('/write-young/<event>', methods=['GET', 'POST'])
def write_young(event=None):
    form = LetterForm()
    del form.specific_recipient_id
    if not form.validate_on_submit():
        return render_template('write_young.html', form=form)

    letter = Letter(
        event=event,
        language_code=form.language_code.data,
        is_male=form.is_male.data,
        is_young=True,
        content=form.greeting.data + ',\n' + form.content.data,
        signature=form.signature.data,
        email=form.email.data,
        country_code=form.country_code.data,
        zipcode=form.zipcode.data,
        specific_recipient_id=None,
        allow_reuse=form.allow_reuse.data
    )
    db.session.add(letter)
    db.session.commit()
    flash('Ta lettre a été enregistrée ! Elle sera distribuée prochainement au sein des établissements scolaires.')
    return redirect(url_for('main.index'))
