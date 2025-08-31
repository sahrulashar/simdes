from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from database import get_connection
from slugify import slugify
from utils.security import login_required, admin_required
import os

berita_bp = Blueprint('berita', __name__, url_prefix='/berita')
UPLOAD_FOLDER = 'static/uploads/berita'

# -----------------------
# LIST BERITA
# -----------------------
@berita_bp.route('/')
@login_required
@admin_required
def list_berita():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM berita ORDER BY id DESC")
        data = cursor.fetchall()
    return render_template('berita/index.html', berita=data)

# -----------------------
# TAMBAH BERITA
# -----------------------
@berita_bp.route('/tambah', methods=['GET', 'POST'])
@login_required
@admin_required
def tambah_berita():
    if request.method == 'POST':
        judul = request.form.get('judul', '').strip()
        konten = request.form.get('konten', '').strip()
        slug = slugify(judul)
        pembuat = session.get('nama', 'Admin')
        gambar_file = request.files.get('gambar')
        filename = None

        if not judul or not konten:
            flash('Judul dan konten tidak boleh kosong.', 'warning')
            return redirect(request.url)

        if gambar_file and gambar_file.filename:
            filename = secure_filename(gambar_file.filename)
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            gambar_file.save(os.path.join(UPLOAD_FOLDER, filename))

        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO berita (judul, slug, konten, gambar, pembuat)
                    VALUES (%s, %s, %s, %s, %s)
                """, (judul, slug, konten, filename, pembuat))
                conn.commit()
                flash('Berita berhasil ditambahkan.', 'success')
                return redirect(url_for('berita.list_berita'))
        except Exception as e:
            conn.rollback()
            flash(f'Gagal menambahkan berita: {e}', 'danger')

    return render_template('berita/tambah.html')

# -----------------------
# EDIT BERITA
# -----------------------
@berita_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_berita(id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM berita WHERE id = %s", (id,))
        berita = cursor.fetchone()

    if not berita:
        flash("Berita tidak ditemukan.", "danger")
        return redirect(url_for('berita.list_berita'))

    if request.method == 'POST':
        judul = request.form.get('judul', '').strip()
        konten = request.form.get('konten', '').strip()
        slug = slugify(judul)
        gambar_file = request.files.get('gambar')
        filename = berita['gambar']

        if not judul or not konten:
            flash('Judul dan konten tidak boleh kosong.', 'warning')
            return redirect(request.url)

        if gambar_file and gambar_file.filename:
            filename = secure_filename(gambar_file.filename)
            gambar_path = os.path.join(UPLOAD_FOLDER, filename)
            gambar_file.save(gambar_path)

            if berita['gambar'] and berita['gambar'] != filename:
                try:
                    os.remove(os.path.join(UPLOAD_FOLDER, berita['gambar']))
                except FileNotFoundError:
                    pass

        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE berita SET judul=%s, slug=%s, konten=%s, gambar=%s
                    WHERE id = %s
                """, (judul, slug, konten, filename, id))
                conn.commit()
                flash("Berita berhasil diperbarui.", "success")
                return redirect(url_for('berita.list_berita'))
        except Exception as e:
            conn.rollback()
            flash(f"Gagal memperbarui berita: {e}", "danger")

    return render_template('berita/tambah.html', data=berita, edit=True)

# -----------------------
# HAPUS BERITA
# -----------------------
@berita_bp.route('/hapus/<int:id>')
@login_required
@admin_required
def hapus_berita(id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT gambar FROM berita WHERE id = %s", (id,))
            data = cursor.fetchone()

            if data and data['gambar']:
                try:
                    os.remove(os.path.join(UPLOAD_FOLDER, data['gambar']))
                except FileNotFoundError:
                    pass

            cursor.execute("DELETE FROM berita WHERE id = %s", (id,))
            conn.commit()
            flash('Berita berhasil dihapus.', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Gagal menghapus berita: {e}', 'danger')

    return redirect(url_for('berita.list_berita'))

# -----------------------
# DETAIL BERITA
# -----------------------
@berita_bp.route('/detail/<int:id>')
@login_required
@admin_required
def detail_berita(id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM berita WHERE id = %s", (id,))
        berita = cursor.fetchone()

    if not berita:
        flash("Berita tidak ditemukan.", "danger")
        return redirect(url_for('berita.list_berita'))

    return render_template('berita/detail.html', berita=berita)
