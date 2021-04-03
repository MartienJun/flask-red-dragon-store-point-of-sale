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

bp = Blueprint('purchase', __name__)


@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT id_pembelian, tgl_pembelian, barang.nama_barang, barang.harga, bayar, user.nama'
        ' FROM pembelian, barang, user WHERE barang.id_barang = pembelian.id_produk AND user.id = pembelian.id_karyawan'
        ' ORDER BY id_pembelian DESC'
    ).fetchall()
    return render_template('purchase/index.html', posts=posts)