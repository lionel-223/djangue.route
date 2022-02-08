from flask import render_template, redirect, url_for
from flask_login import current_user

from app.models import Article
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
    db.session.add(article)
    db.session.commit()
    return redirect(url_for('admin.index'))
