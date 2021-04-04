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


def get_user(id, check_author=True):
    users = get_db().execute(
        'SELECT * FROM user'
        ' WHERE id = ?',(id,)
    ).fetchone()

    return users


@bp.route('/add_user', methods=('GET', 'POST'))
@login_required
def add_user():
    if request.method == 'POST':
        nama = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        db = get_db()
        error = None

        if not nama:
            error = 'Name is required.'
        elif not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'
        elif not role:
            error = 'Role is required.'
        elif db.execute( #note -db.execute-
            'SELECT id FROM user WHERE email = ?', (email,)
        ).fetchone() is not None: #note -fetchone()-
            error = 'Email {} is already registered.'.format(email)

        if error is None:
            db.execute(
                'INSERT INTO user (email, password, login_status, nama, role) VALUES (?, ?, ?, ?, ?)',
                (email, generate_password_hash(password), False, nama, role)
            )
            db.commit()
            return redirect(url_for('user.list_user'))

        flash(error)

    return render_template('user/add_user.html')


