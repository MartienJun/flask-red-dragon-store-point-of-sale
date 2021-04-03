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

"""Declare auth blueprint"""
bp = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/register', methods=('GET', 'POST')) #note -@bp.route-
def register():
    if request.method == 'POST':
        nama = request.form['name']
        email = request.form['email'] #note -request.form-
        password = request.form['password']
        db = get_db()
        error = None

        if not nama:
            error = 'Name is required.'
        elif not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute( #note -db.execute-
            'SELECT id FROM user WHERE email = ?', (email,)
        ).fetchone() is not None: #note -fetchone()-
            error = 'Email {} is already registered.'.format(email)

        if error is None:
            db.execute(
                'INSERT INTO user (email, password, nama) VALUES (?, ?, ?)',
                (nama, email, generate_password_hash(password)) #note -generate_password_hash()-
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


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


"""
Note:

-@bp.routep-
@bp.route associates the URL /register with the register view function. When Flask receives a 
request to /auth/register, it will call the register view and use the return value as the response.


-request.form-
request.form is a special type of dict mapping submitted form keys and values. The user will input 
their email and password.


-db.execute-
Execute query


-fetchone()-
fetchone() returns one row from the query. If the query returned no results, it returns None.


-fetchall()-
fetchall() is used, which returns a list of all results.


-generate_password_hash()-
generate_password_hash() is used to securely hash the password


-db.commit()-
db.commit() needs to be called afterwards to save the changes.


-url_for()-
url_for() generates the URL for the login view based on its name. This is preferable 
to writing the URL directly as it allows you to change the URL later without changing all 
code that links to it.


-redirect()-
redirect() generates a redirect response to the generated URL.


-flash()-
flash() stores messages that can be retrieved when rendering the template.


-render_template()-
render_template() will render a template containing the HTML
"""