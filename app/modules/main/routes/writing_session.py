import hashlib
import os

from flask import render_template, redirect, url_for, abort, request, flash, send_from_directory
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

import app
from app import db
from app.models import WritingSession, HandwrittenLetter
from .write import allowed_file
from .. import bp, WritingSessionForm


@bp.route('/writing-session/create/', methods=['GET', 'POST'])
@login_required
def create_writing_session():
    form = WritingSessionForm()
    form.school_id.choices = [(school.id, school.name) for school in current_user.schools]
    if not form.validate_on_submit():
        return render_template('create_writing_session.html', form=form)

    writing_session = WritingSession(
        type=form.type.data,
        title=form.title.data,
        school_id=form.school_id.data,
        teacher_id=current_user.id,
    )
    db.session.add(writing_session)
    db.session.commit()
    return redirect(url_for('main.teacher_home'))


@bp.get('/writing-session/<int:session_id>/')
@login_required
def writing_session_detail(session_id):
    writing_session = db.session.get(WritingSession, session_id)
    if not writing_session:
        abort(404)
    if not (current_user == writing_session.teacher or current_user.can_edit_recipients):  # TODO Replace with the appropriate permission
        abort(403)
    return render_template('writing_session_detail.html', writing_session=writing_session, types=WritingSession.Type)


@bp.post('/writing-session/upload/')
def upload_handwritten_letters():
    session_id = request.form.get('session_id')
    files = request.files.getlist('files')
    upload_directory = app.HANDWRITTEN_LETTERS_UPLOAD_FOLDER
    if not os.path.exists(upload_directory):
        os.makedirs(upload_directory)
    for file in files:
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            name, file_ext = os.path.splitext(filename)
            file_hash = hashlib.md5(name.encode()).hexdigest()
            hash_exist = db.session.query(db.session.query(HandwrittenLetter).filter_by(hash=file_hash).exists()).scalar()
            if hash_exist:
                flash(f"File {file.filename} had already been uploaded. You can't upload the same letter twice.")
            else:
                file.save(os.path.join(app.HANDWRITTEN_LETTERS_UPLOAD_FOLDER, file_hash + file_ext))
                upload = HandwrittenLetter(
                    hash=file_hash,
                    name=name,
                    extension=file_ext,
                    writing_session_id=session_id
                )
                db.session.add(upload)
    db.session.commit()
    return redirect(url_for('main.writing_session_detail', session_id=session_id))


@bp.get('/writing-session/handwritten-letter/download/<upload_hash>/')
def handwritten_letter_download(upload_hash):
    image = db.session.get(HandwrittenLetter, upload_hash)
    if not image:
        abort(404)
    image_name = image.hash + image.extension
    return send_from_directory(app.HANDWRITTEN_LETTERS_UPLOAD_FOLDER, image_name)


@bp.get('/writing-session/handwritten-letter/delete/<upload_hash>')
def delete_handwritten_letter(upload_hash):
    letter = db.session.get(HandwrittenLetter, upload_hash)
    session_id = letter.writing_session_id
    file_path = os.path.join(app.HANDWRITTEN_LETTERS_UPLOAD_FOLDER, upload_hash + letter.extension)
    print(file_path)
    print(os.path.exists(file_path), flush=True)
    if os.path.exists(file_path):
        os.remove(file_path)
    db.session.delete(letter)
    db.session.commit()
    return redirect(url_for('main.writing_session_detail', session_id=session_id))