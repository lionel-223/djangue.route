from flask import request, render_template, redirect, url_for, flash

from app import db
from app.models import Letter
from .. import bp, LetterForm


@bp.route('/write/', methods=['GET', 'POST'])
def write():
    is_young = request.args.get('is_young', None) == 'True'
    event = request.args.get('event', None)
    form = LetterForm()
    if not form.validate_on_submit():
        if is_young:
            del form.specific_recipient_id
            return render_template('write_young.html', form=form)
        return render_template('write.html', form=form)

    greeting = form.greeting.data
    if not greeting.endswith(","):
        greeting = greeting + ','
    letter = Letter(
        event=event,
        language_code=form.language_code.data,
        is_male=form.is_male.data,
        is_young=is_young,
        content=greeting + '\n' + form.content.data,
        signature=form.signature.data,
        email=form.email.data,
        country_code=form.country_code.data,
        zipcode=form.zipcode.data,
        specific_recipient_id=form.specific_recipient_id.data or None,
        allow_reuse=form.allow_reuse.data
    )
    db.session.add(letter)
    db.session.commit()
    flash('Ta lettre a été enregistrée, elle sera envoyée prochainement.')
    return redirect(url_for('main.index'))
