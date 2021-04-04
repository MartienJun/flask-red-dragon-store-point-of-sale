from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from myapp.auth import login_required
from myapp.db import get_db

bp = Blueprint('user', __name__)


@bp.route('/list_user')
def list_user():
    db = get_db()
    users = db.execute(
        'SELECT * FROM user'
        ' ORDER BY id ASC'
    ).fetchall()
    return render_template('user/list_user.html', users=users)


