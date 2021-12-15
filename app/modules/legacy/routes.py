from flask import redirect, request, url_for

from . import bp


@bp.get('/ecrire-une-lettre/')
@bp.get('/ecrivez-une-lettre/')
def from_write():
    event = request.args.get('partnership')
    return redirect(url_for('main.write', event=event))


@bp.get('/wp-login.php')
def from_login():
    return redirect(url_for('main.login'))


@bp.get('/wp-admin/admin.php')
def from_admin():
    pages = {
        'gravity-moderation': 'admin.moderation',
        'gravity-moderation-plus': 'admin.moderation',
        'gravity-moderation-actimel': 'admin.moderation',
    }
    requested_page = request.args.get('page')
    route = pages.get(requested_page, 'main.index')
    return redirect(url_for(route))
