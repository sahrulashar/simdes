from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from database import get_connection
from datetime import datetime
from utils.security import login_required, admin_required

kepindahan_bp = Blueprint('kepindahan', __name__, url_prefix='/kepindahan')

# -----------------------------------
# Generate nomor pindah otomatis
# -----------------------------------
def generate_no_pindah():
    today_str = datetime.today().strftime('%Y%m%d')
    prefix = f"KP-{today_str}-"
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) AS jumlah FROM kepindahan WHERE DATE(created_at) = CURDATE()")
        result = cursor.fetchone()
        count = result['jumlah'] + 1 if result and result['jumlah'] else 1
    return f"{prefix}{str(count).zfill(3)}"

# -----------------------------------
# Halaman Utama (List)
# -----------------------------------
@kepindahan_bp.route('/')
@login_required
@admin_required
def index():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM kepindahan ORDER BY id DESC")
        data = cursor.fetchall()
    return render_template('kepindahan/index.html', data=data)

# -----------------------------------
# Tambah Data
# -----------------------------------
@kepindahan_bp.route('/tambah', methods=['GET', 'POST'])
@login_required
@admin_required
def tambah():
    conn = get_connection()
    if request.method == 'POST':
        no_pindah = generate_no_pindah()
        nik = request.form.get('nik', '').strip()
        nama = request.form.get('nama', '').strip()
        tanggal_pindah = request.form.get('tanggal_pindah', '')
        keterangan = request.form.get('keterangan', '')

        if not nik or not nama or not tanggal_pindah:
            flash("NIK, Nama, dan Tanggal Pindah wajib diisi.", "warning")
            return redirect(request.url)

        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO kepindahan (no_pindah, nik, nama, tanggal_pindah, keterangan)
                VALUES (%s, %s, %s, %s, %s)
            """, (no_pindah, nik, nama, tanggal_pindah, keterangan))
            conn.commit()
            flash("Data kepindahan berhasil ditambahkan", "success")
            return redirect(url_for('kepindahan.index'))

    return render_template('kepindahan/tambah.html')

# -----------------------------------
# Ambil Data Penduduk berdasarkan NIK
# -----------------------------------
@kepindahan_bp.route('/penduduk/<nik>')
@login_required
def get_penduduk(nik):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT nama FROM penduduk WHERE nik = %s", (nik,))
        row = cursor.fetchone()
        if row:
            return jsonify({'nama': row['nama']})
    return jsonify({})

# -----------------------------------
# Edit Data
# -----------------------------------
@kepindahan_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit(id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM kepindahan WHERE id = %s", (id,))
        data = cursor.fetchone()
        if not data:
            flash("Data tidak ditemukan", "danger")
            return redirect(url_for('kepindahan.index'))

    if request.method == 'POST':
        nik = request.form.get('nik', '').strip()
        nama = request.form.get('nama', '').strip()
        tanggal_pindah = request.form.get('tanggal_pindah', '')
        keterangan = request.form.get('keterangan', '')

        if not nik or not nama or not tanggal_pindah:
            flash("NIK, Nama, dan Tanggal Pindah wajib diisi.", "warning")
            return redirect(request.url)

        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE kepindahan
                    SET nik=%s, nama=%s, tanggal_pindah=%s, keterangan=%s
                    WHERE id=%s
                """, (nik, nama, tanggal_pindah, keterangan, id))
                conn.commit()
                flash("Data kepindahan berhasil diperbarui", "success")
                return redirect(url_for('kepindahan.index'))
        except Exception as e:
            conn.rollback()
            flash(f"Gagal memperbarui data: {e}", "danger")

    return render_template('kepindahan/tambah.html', data=data, edit=True)

# -----------------------------------
# Hapus Data
# -----------------------------------
@kepindahan_bp.route('/hapus/<int:id>')
@login_required
@admin_required
def hapus(id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM kepindahan WHERE id = %s", (id,))
            conn.commit()
            flash("Data kepindahan berhasil dihapus", "danger")
    except Exception as e:
        conn.rollback()
        flash(f"Gagal menghapus data: {e}", "danger")
    return redirect(url_for('kepindahan.index'))
