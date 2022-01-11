from flask import render_template

from app import db
from app.models import Recipient
from .. import bp


@bp.route('/recipient-list/')
def recipient_list():
    recipients = db.session.query(Recipient).filter_by(type=Recipient.Types.retirement_home)
    return render_template('recipient_list.html', recipients=recipients)
