from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from myapp.auth import login_required
from myapp.product import *
from myapp.db import get_db

bp = Blueprint('purchase', __name__)


@bp.route('/')
@login_required
def index():
    db = get_db()
    purchases = db.execute(
        'SELECT id_pembelian, tgl_pembelian, barang.nama_barang, barang.harga, bayar, user.nama'
        ' FROM pembelian, barang, user WHERE barang.id_barang = pembelian.id_produk AND user.id = pembelian.id_karyawan'
        ' ORDER BY id_pembelian DESC'
    ).fetchall()
    return render_template('purchase/index.html', purchases=purchases)


def get_purchase(id, check_author=True):
    purchases = get_db().execute(
        'SELECT * FROM pembelian'
        ' WHERE id_pembelian = ?',(id,)
    ).fetchone()

    return purchases


@bp.route('/add_purchase', methods=('GET', 'POST'))
@login_required
def add_purchase():
    if request.method == 'POST':
        id_produk = request.form['id_produk']
        bayar = request.form['bayar']
        id_karyawan = request.form['id_karyawan']
        db = get_db()
        error = None

        if not id_produk:
            error = 'Product is required.'
        elif not bayar:
            error = 'Pay is required.'
        
        if error is not None:
            flash(error)
        else:
            db.execute(
                'INSERT INTO pembelian (id_produk, bayar, id_karyawan) VALUES (?, ?, ?)',
                (id_produk, bayar, id_karyawan)
            )
            db.commit()
            return redirect(url_for('purchase.index'))
    
    return render_template('purchase/add_purchase.html', products=getAllProduct())


