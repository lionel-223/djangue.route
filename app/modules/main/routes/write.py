import os.path
import hashlib

from flask import request, render_template, redirect, url_for, flash, abort
from flask_login import login_required
from werkzeug.utils import secure_filename
from PIL import Image

import app
from app import db
from app.models import Letter, Upload, WritingSession, Recipient
from app.utils.str_to_bool import strtobool
from .. import bp, LetterForm


def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in app.ALLOWED_EXTENSIONS


@bp.route('/write/', methods=['GET', 'POST'])
def write():
    is_young = strtobool(request.args.get('is_young', ''))
    event = request.args.get('event', None)
    writing_session_id = request.args.get('writing_session', None)
    writing_session = db.session.get(WritingSession, writing_session_id)
    if writing_session_id and not writing_session:
        flash('WritingSession not found')
        writing_session_id = None

    form = LetterForm()
    if not form.validate_on_submit():
        if is_young:
            del form.specific_recipient_id
            return render_template('write_young.html', form=form)
        if writing_session:
            del form.specific_recipient_id
            form.language_code.data = writing_session.language_code
            form.country_code.data = writing_session.school.country_code
            form.zipcode.data = writing_session.school.zipcode
        ehpads = db.session.query(Recipient).filter(Recipient.type == Recipient.Types.RETIREMENT_HOME)
        return render_template('write.html', form=form, ehpads=ehpads)

    greeting = form.greeting.data
    if not greeting.endswith((",", ".", "!")):
        greeting = greeting + ','
    letter = Letter(
        event=event,
        writing_session_id=writing_session_id,
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
    if writing_session:
        letter.specific_recipient = writing_session.school.associated_recipient
        letter.status = Letter.Status.NOT_CORRECTED

    file = form.upload.data
    upload_directory = app.FILE_UPLOAD_FOLDER
    if not os.path.exists(upload_directory):
        os.makedirs(upload_directory)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        name, file_ext = os.path.splitext(filename)
        file_hash = hashlib.md5(name.encode()).hexdigest()
        hash_exist = db.session.query(db.session.query(Upload).filter_by(hash=file_hash).exists()).scalar()
        if hash_exist:
            letter.upload_hash = file_hash
        else:
            upload = Upload(
                hash=file_hash,
                name=name,
                extension=file_ext
            )
            letter.upload_hash = upload.hash
            image = Image.open(file)
            image.thumbnail(app.IMAGE_SIZE)
            image.save(os.path.join(upload_directory, file_hash + file_ext))
            db.session.add(upload)
            db.session.commit()

    db.session.add(letter)
    db.session.commit()
    flash('Ta lettre a été enregistrée, elle sera envoyée prochainement.')
    return redirect(url_for('main.index'))


@bp.get('/letter/<int:letter_id>')
@login_required
def letter_detail(letter_id):
    letter = db.session.get(Letter, letter_id)
    if not letter:
        abort(404)
    return render_template('letter_detail.html', letter=letter)

