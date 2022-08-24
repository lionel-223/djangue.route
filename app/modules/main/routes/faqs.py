from flask import render_template

from .. import bp


@bp.route('/faqs')
def faqs():
    return render_template('faqs.html')