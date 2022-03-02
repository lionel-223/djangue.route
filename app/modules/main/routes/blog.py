import os

from flask import render_template, abort, send_from_directory

import app
from app.models import Article, User, Upload
from app import db
from .. import bp


@bp.route('/our-blog/')
def our_blog():
    articles = db.session.query(Article)
    return render_template('blog.html', articles=articles)


@bp.get('/our-blog/article/<int:article_id>/')
def article(article_id):
    article = db.session.get(Article, article_id)
    author = db.session.get(User, article.author_id)
    if not article:
        abort(404)
    return render_template('article.html', article=article, author=author)


@bp.get('/image-blog-upload/<upload_hash>')
def image_blog_upload(upload_hash):
    image = db.session.get(Upload, upload_hash)
    if not image:
        abort(404)
    image_name = image.hash + image.extension
    image_blog_folder = os.path.join(app.FILE_UPLOAD_FOLDER, 'blog')
    return send_from_directory(image_blog_folder, image_name)
