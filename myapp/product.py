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


def get_products(id, check_author=True):
    products = get_db().execute(
        'SELECT * FROM barang'
        ' WHERE id_barang = ?',(id,)
    ).fetchone()

    return products


def getAllProduct():
    products = get_db().execute(
        'SELECT * FROM barang'
    ).fetchall()

    return products


@bp.route('/add_product', methods=('GET', 'POST'))
@login_required
def add_product():
    if request.method == 'POST':
        nama_barang = request.form['product_name']
        tipe_barang = request.form['product_type']
        harga = request.form['price']
        stock = request.form['stock']
        db = get_db()
        error = None

        if not nama_barang:
            error = 'Product name is required.'
        elif not tipe_barang:
            error = 'Product type is required.'
        elif not harga:
            error = 'Product price is required.'
        elif not stock:
            error = 'Product stock is required.'
        elif db.execute( #note -db.execute-
                    'SELECT id_barang FROM barang WHERE nama_barang = ?', (nama_barang,)
                ).fetchone() is not None: #note -fetchone()-
                    error = 'Product name {} is already registered.'.format(nama_barang)
        
        if error is not None:
            flash(error)
        else:
            db.execute(
                'INSERT INTO barang (nama_barang, tipe_barang, harga, stock) VALUES (?, ?, ?, ?)',
                (nama_barang, tipe_barang, harga, stock)
            )
            db.commit()
            return redirect(url_for('product.list_product'))
    
    return render_template('product/add_product.html')


@bp.route('/<int:id>/edit_product', methods=('GET', 'POST'))
@login_required
def edit_product(id):
    products = get_products(id)

    if request.method == 'POST':
        nama_barang = request.form['product_name']
        tipe_barang = request.form['product_type']
        harga = request.form['price']
        stock = request.form['stock']
        error = None

        if not nama_barang:
            error = 'Product name is required.'
        elif not tipe_barang:
            error = 'Product type is required.'
        elif not harga:
            error = 'Product price is required.'
        elif not stock:
            error = 'Product stock is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE barang SET nama_barang = ?, tipe_barang = ?, harga = ?, stock = ?'
                ' WHERE id_barang = ?',
                (nama_barang, tipe_barang, harga, stock, id)
            )
            db.commit()
            return redirect(url_for('product.list_product'))

    return render_template('product/edit_product.html', products=products)


@bp.route('/<int:id>/delete_product', methods=('POST', 'GET'))
@login_required
def delete_product(id):
    get_products(id)
    db = get_db()
    db.execute('DELETE FROM barang WHERE id_barang = ?', (id,))
    db.commit()
    return redirect(url_for('product.list_product'))