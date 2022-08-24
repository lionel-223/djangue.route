import os

from flask import render_template
from .. import bp

import app
from app.models import Article, User, Upload
from app import db
@bp.route('/Nos-Partenaires/')
def nos_partenaires():
        return render_template('nos_partenaires.html')