from flask import render_template, abort

from app.models import Article, User
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
