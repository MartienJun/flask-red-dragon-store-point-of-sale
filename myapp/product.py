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

bp = Blueprint('product', __name__)


@bp.route('/list_product')
def list_product():
    db = get_db()
    products = db.execute(
        'SELECT * FROM barang'
        ' ORDER BY id_barang ASC'
    ).fetchall()
    return render_template('product/list_product.html', products=products)


