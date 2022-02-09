import os
import hashlib

from flask import render_template, redirect, url_for
from werkzeug.utils import secure_filename
from flask_login import current_user
from PIL import Image

import app
from app.models import Article, Upload
from app import db
from .. import bp, ArticleForm


@bp.route('/article-form/', methods=['GET', 'POST'])
def article_form():
    form = ArticleForm()
    if not form.validate_on_submit():
        return render_template('admin/article_form.html', form=form)

    article = Article(
        title=form.title.data,
        content=form.content.data,
        author_id=current_user.id
    )
    file = form.upload.data
    upload_directory = os.path.join(app.FILE_UPLOAD_FOLDER, 'blog')
    if not os.path.exists(upload_directory):
        os.makedirs(upload_directory)

    if file:
        filename = secure_filename(file.filename)
        name, file_ext = os.path.splitext(filename)
        file_hash = hashlib.md5(name.encode()).hexdigest()
        hash_exist = db.session.query(db.session.query(Upload).filter_by(hash=file_hash).exists()).scalar()
        if hash_exist:
            article.upload_hash = file_hash
        else:
            upload = Upload(
                hash=file_hash,
                name=name,
                extension=file_ext
            )
            article.upload_hash = upload.hash
            image = Image.open(file)
            image.thumbnail(app.IMAGE_SIZE)
            image.save(os.path.join(upload_directory, file_hash + file_ext))
            db.session.add(upload)
            db.session.commit()

    db.session.add(article)
    db.session.commit()
    return redirect(url_for('admin.index'))
