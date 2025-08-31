from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from database import get_connection
from utils.security import login_required, admin_required
import os
import datetime

galeri_bp = Blueprint('galeri', __name__, url_prefix='/galeri')

UPLOAD_FOLDER = 'static/uploads/galeri'

# ---------------------
# LIST GALERI
# ---------------------
@galeri_bp.route('/')
@login_required
@admin_required
def index():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM galeri ORDER BY created_at DESC")
        data = cursor.fetchall()
    conn.close()
    return render_template('galeri/index.html', data=data)

# ---------------------
# TAMBAH GALERI
# ---------------------
@galeri_bp.route('/tambah', methods=['GET', 'POST'])
@login_required
@admin_required
def tambah():
    if request.method == 'POST':
        judul = request.form.get('judul', '').strip()
        deskripsi = request.form.get('deskripsi', '').strip()
        files = request.files.getlist('gambar')

        if not files or files[0].filename == '':
            flash('Silakan pilih minimal satu gambar!', 'warning')
            return redirect(request.url)

        saved = 0
        conn = get_connection()

        try:
            with conn.cursor() as cursor:
                for file in files:
                    if file and file.filename:
                        filename = secure_filename(file.filename)
                        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                        file_path = os.path.join(UPLOAD_FOLDER, filename)
                        file.save(file_path)

                        cursor.execute("""
                            INSERT INTO galeri (judul, deskripsi, gambar, created_at)
                            VALUES (%s, %s, %s, %s)
                        """, (judul, deskripsi, filename, datetime.datetime.now()))
                        saved += 1

                conn.commit()
                flash(f"{saved} gambar berhasil disimpan.", "success")
                return redirect(url_for('galeri.index'))

        except Exception as e:
            conn.rollback()
            flash(f"Terjadi kesalahan saat menyimpan gambar: {e}", "danger")

        finally:
            conn.close()

    return render_template('galeri/tambah.html')
# ---------------------
# HAPUS GALERI
# ---------------------
@galeri_bp.route('/hapus/<int:id>', methods=['POST'])
@login_required
@admin_required
def hapus(id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # Ambil nama file gambar terlebih dahulu
            cursor.execute("SELECT gambar FROM galeri WHERE id = %s", (id,))
            row = cursor.fetchone()
            if row:
                gambar_path = os.path.join(UPLOAD_FOLDER, row['gambar'])
                if os.path.exists(gambar_path):
                    os.remove(gambar_path)

                # Hapus dari database
                cursor.execute("DELETE FROM galeri WHERE id = %s", (id,))
                conn.commit()
                flash("Data galeri berhasil dihapus.", "success")
            else:
                flash("Data tidak ditemukan.", "warning")
    except Exception as e:
        conn.rollback()
        flash(f"Gagal menghapus data: {e}", "danger")
    finally:
        conn.close()
    return redirect(url_for('galeri.index'))
