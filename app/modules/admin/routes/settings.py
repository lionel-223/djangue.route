from flask import request, render_template, redirect, url_for, flash

from app import db
from app.models import Setting

from .. import bp


@bp.route('/settings/', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        new_partnership = request.form.get('partnership', None)
        new_gender = request.form.get('gender')
        settings = db.session.query(Setting).first()
        if settings:
            settings.partnership = new_partnership
            settings.gender = new_gender
        else:
            new_settings = Setting(
                partnership=new_partnership,
                gender=new_gender
            )
            db.session.add(new_settings)
        db.session.commit()
        return redirect(url_for('admin.index'))
    return render_template('admin/settings.html')