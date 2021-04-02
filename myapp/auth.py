import functools

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from myapp.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route('/register', methods=('GET', 'POST')) #note -@bp.route-
def register():
    if request.method == 'POST':
        email = request.form['email'] #note -request.form-
        password = request.form['password']
        nama = request.form['name']
        db = get_db()
        error = None

        if not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'
        elif not nama:
            error = 'Name is required.'
        elif db.execute( #note -db.execute-
            'SELECT id FROM user WHERE email = ?', (email,)
        ).fetchone() is not None: #note -fetchone()-
            error = 'Email {} is already registered.'.format(email)

        if error is None:
            db.execute(
                'INSERT INTO user (email, password, nama) VALUES (?, ?, ?)',
                (email, generate_password_hash(password)) #note -generate_password_hash()-
            )
            db.commit() #note -db.commit()-
            return redirect(url_for('auth.login')) #note -redirect()-, -url_for()-

        flash(error) #note -flash()-

    return render_template('auth/register.html') #note -render_template()-


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute('SELECT * FROM user WHERE email = ?', (email,)).fetchone()

        if user is None:
            error = 'Incorrect Email.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect Password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


