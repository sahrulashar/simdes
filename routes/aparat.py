from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from database import get_connection
from utils.security import login_required, role_required
import os

aparat_bp = Blueprint('aparat', __name__, url_prefix='/aparat')

UPLOAD_FOLDER = 'static/uploads/aparat'

# List data aparat
@aparat_bp.route('/')
@login_required
@role_required('admin')
def list_aparat():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM aparat_desa ORDER BY id DESC")
        data = cursor.fetchall()
    return render_template('aparat/index.html', data=data)

# Tambah aparat
@aparat_bp.route('/tambah', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def tambah_aparat():
    if request.method == 'POST':
        nama = request.form['nama']
        jabatan = request.form['jabatan']
        kontak = request.form['kontak']
        foto_file = request.files.get('foto')
        filename = None

        if foto_file and foto_file.filename != '':
            filename = secure_filename(foto_file.filename)
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            foto_path = os.path.join(UPLOAD_FOLDER, filename)
            foto_file.save(foto_path)

        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO aparat_desa (nama, jabatan, kontak, foto)
                    VALUES (%s, %s, %s, %s)
                """, (nama, jabatan, kontak, filename))
                conn.commit()
                flash('Data aparat berhasil ditambahkan', 'success')
                return redirect(url_for('aparat.list_aparat'))
        except Exception as e:
            conn.rollback()
            flash(f'Gagal menambahkan data: {e}', 'danger')

    return render_template('aparat/tambah.html')

# Edit aparat
@aparat_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit_aparat(id):
    conn = get_connection()
    if request.method == 'POST':
        nama = request.form['nama']
        jabatan = request.form['jabatan']
        kontak = request.form.get('kontak')
        foto_file = request.files.get('foto')
        foto_filename = None

        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT foto FROM aparat_desa WHERE id = %s", (id,))
                old_data = cursor.fetchone()
                old_foto = old_data['foto'] if old_data else None

                if foto_file and foto_file.filename != '':
                    foto_filename = secure_filename(foto_file.filename)
                    foto_path = os.path.join(UPLOAD_FOLDER, foto_filename)
                    foto_file.save(foto_path)

                    if old_foto and old_foto != foto_filename:
                        old_foto_path = os.path.join(UPLOAD_FOLDER, old_foto)
                        if os.path.exists(old_foto_path):
                            os.remove(old_foto_path)
                else:
                    foto_filename = old_foto

                cursor.execute("""
                    UPDATE aparat_desa SET
                        nama = %s,
                        jabatan = %s,
                        kontak = %s,
                        foto = %s
                    WHERE id = %s
                """, (nama, jabatan, kontak, foto_filename, id))
                conn.commit()
                flash("Data aparat desa berhasil diperbarui", "success")
                return redirect(url_for('aparat.list_aparat'))
        except Exception as e:
            conn.rollback()
            flash(f"Gagal memperbarui data: {e}", "danger")

    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM aparat_desa WHERE id = %s", (id,))
        data = cursor.fetchone()

    return render_template('aparat/tambah.html', data=data, edit=True)

# Hapus aparat
@aparat_bp.route('/hapus/<int:id>')
@login_required
@role_required('admin')
def hapus_aparat(id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT foto FROM aparat_desa WHERE id = %s", (id,))
            aparat = cursor.fetchone()

            if aparat and aparat['foto']:
                try:
                    os.remove(os.path.join(UPLOAD_FOLDER, aparat['foto']))
                except FileNotFoundError:
                    pass

            cursor.execute("DELETE FROM aparat_desa WHERE id = %s", (id,))
            conn.commit()
            flash('Data aparat berhasil dihapus', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Gagal menghapus data: {e}', 'danger')

    return redirect(url_for('aparat.list_aparat'))
