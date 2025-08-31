from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from database import get_connection
from datetime import datetime
from utils.security import login_required, admin_required

pendatang_bp = Blueprint('pendatang', __name__, url_prefix='/pendatang')

# -----------------------------------
# Generate Nomor Kedatangan Otomatis
# -----------------------------------
def generate_no_kedatangan():
    today_str = datetime.today().strftime('%Y%m%d')
    prefix = f"PD-{today_str}-"
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) AS jumlah FROM pendatang WHERE DATE(created_at) = CURDATE()")
        result = cursor.fetchone()
        count = result['jumlah'] + 1 if result and result['jumlah'] else 1
    return f"{prefix}{str(count).zfill(3)}"

# -----------------------------------
# Halaman Utama (List Pendatang)
# -----------------------------------
@pendatang_bp.route('/')
@login_required
@admin_required
def index():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM pendatang ORDER BY id DESC")
        data = cursor.fetchall()
    return render_template('pendatang/index.html', data=data)

# -----------------------------------
# Tambah Pendatang
# -----------------------------------
@pendatang_bp.route('/tambah', methods=['GET', 'POST'])
@login_required
@admin_required
def tambah():
    conn = get_connection()
    if request.method == 'POST':
        no_kedatangan = generate_no_kedatangan()
        nik = request.form.get('nik', '').strip()
        nama = request.form.get('nama', '').strip()
        tanggal_datang = request.form.get('tanggal_datang', '')
        asal = request.form.get('asal', '').strip()

        if not nik or not nama or not tanggal_datang:
            flash("NIK, Nama, dan Tanggal Datang wajib diisi.", "warning")
            return redirect(request.url)

        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO pendatang (no_kedatangan, nik, nama, tanggal_datang, asal)
                VALUES (%s, %s, %s, %s, %s)
            """, (no_kedatangan, nik, nama, tanggal_datang, asal))
            conn.commit()
            flash("Data pendatang berhasil ditambahkan", "success")
            return redirect(url_for('pendatang.index'))

    return render_template('pendatang/tambah.html')

# -----------------------------------
# Auto-Fill Nama Berdasarkan NIK
# -----------------------------------
@pendatang_bp.route('/penduduk/<nik>')
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
# Edit Data Pendatang
# -----------------------------------
@pendatang_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit(id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM pendatang WHERE id = %s", (id,))
        data = cursor.fetchone()
        if not data:
            flash("Data tidak ditemukan", "danger")
            return redirect(url_for('pendatang.index'))

    if request.method == 'POST':
        nik = request.form.get('nik', '').strip()
        nama = request.form.get('nama', '').strip()
        tanggal_datang = request.form.get('tanggal_datang', '')
        asal = request.form.get('asal', '').strip()

        if not nik or not nama or not tanggal_datang:
            flash("NIK, Nama, dan Tanggal Datang wajib diisi.", "warning")
            return redirect(request.url)

        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE pendatang
                    SET nik=%s, nama=%s, tanggal_datang=%s, asal=%s
                    WHERE id=%s
                """, (nik, nama, tanggal_datang, asal, id))
                conn.commit()
                flash("Data pendatang berhasil diperbarui", "success")
                return redirect(url_for('pendatang.index'))
        except Exception as e:
            conn.rollback()
            flash(f"Gagal memperbarui data: {e}", "danger")

    return render_template('pendatang/tambah.html', data=data, edit=True)

# -----------------------------------
# Hapus Pendatang
# -----------------------------------
@pendatang_bp.route('/hapus/<int:id>')
@login_required
@admin_required
def hapus(id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM pendatang WHERE id = %s", (id,))
            conn.commit()
            flash("Data pendatang berhasil dihapus", "danger")
    except Exception as e:
        conn.rollback()
        flash(f"Gagal menghapus data: {e}", "danger")
    return redirect(url_for('pendatang.index'))
