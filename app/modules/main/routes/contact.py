from flask import render_template, flash

from .. import bp, ContactForm
from app.utils import email


@bp.route('/FAQ-contact/', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if not form.validate_on_submit():
        return render_template('contact.html', form=form)
    data = {
        "name": form.name.data,
        "email": form.email.data,
        "message": form.message.data
    }
    subject = 'Message reçu de la part de :'
    sender = data["name"] + ', ' + data["email"]
    # For the moment, this function doesn't really send an email
    email.send_email(subject, sender, 'contact@1lettre1sourire.org', data["message"])
    flash('Votre message a été envoyé ! Nous faisons notre possible pour vous répondre dans les plus brefs délais')
    return render_template('contact.html', data=data)
