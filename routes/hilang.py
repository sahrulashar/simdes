from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from database import get_connection
from datetime import datetime
from utils.security import login_required, admin_required

hilang_bp = Blueprint('hilang', __name__, url_prefix='/hilang')

# ----------------------------
# Autocomplete NIK dan Nama
# ----------------------------
@hilang_bp.route('/cari-nik')
@login_required
def cari_nik():
    term = request.args.get('term', '')
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT nik, nama FROM penduduk
            WHERE nik LIKE %s OR nama LIKE %s
            LIMIT 10
        """, (f"%{term}%", f"%{term}%"))
        hasil = [f"{row['nik']} - {row['nama']}" for row in cursor.fetchall()]
    return jsonify(hasil)

# ----------------------------
# Ambil data lengkap berdasarkan NIK
# ----------------------------
@hilang_bp.route('/penduduk/<nik>')
@login_required
def get_penduduk(nik):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT nik, nama, jenis_kelamin, tempat_lahir, tanggal_lahir, alamat
            FROM penduduk
            WHERE nik = %s
        """, (nik,))
        row = cursor.fetchone()
        if row:
            return jsonify({
                'nik': row['nik'],
                'nama': row['nama'],
                'jenis_kelamin': 'Laki-laki' if row['jenis_kelamin'] == 'L' else 'Perempuan',
                'tempat_lahir': row['tempat_lahir'],
                'tanggal_lahir': row['tanggal_lahir'].strftime('%Y-%m-%d') if row['tanggal_lahir'] else '',
                'alamat': row['alamat']
            })
    return jsonify({})

# ----------------------------
# Halaman daftar surat hilang
# ----------------------------
@hilang_bp.route('/admin')
@login_required
@admin_required
def admin_index():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM hilang ORDER BY created_at DESC")
        data = cursor.fetchall()
    return render_template('hilang/index.html', data=data)

# ----------------------------
# Tambah Surat Hilang
# ----------------------------
@hilang_bp.route('/admin/tambah', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_tambah():
    if request.method == 'POST':
        nik = request.form['nik']
        nama = request.form['nama']
        jenis_kelamin = request.form['jenis_kelamin']
        tempat_lahir = request.form['tempat_lahir']
        tanggal_lahir = request.form['tanggal_lahir']
        alamat = request.form['alamat']
        keterangan = request.form['keterangan']
        pembuat = 'Admin'
        no_surat = f"HIL-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO hilang 
                (no_surat, nik, nama, jenis_kelamin, tempat_lahir, tanggal_lahir,
                 alamat, keterangan, status, pembuat_surat)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'pending', %s)
            """, (no_surat, nik, nama, jenis_kelamin, tempat_lahir,
                  tanggal_lahir, alamat, keterangan, pembuat))
            conn.commit()
            flash("Surat Keterangan Hilang berhasil ditambahkan.", "success")
            return redirect(url_for('hilang.admin_index'))

    return render_template('hilang/admin_tambah.html')

# ----------------------------
# Edit Surat Hilang
# ----------------------------
@hilang_bp.route('/admin/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_edit(id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM hilang WHERE id = %s", (id,))
        data = cursor.fetchone()

    if not data:
        flash("Data tidak ditemukan", "danger")
        return redirect(url_for('hilang.admin_index'))

    if request.method == 'POST':
        nama = request.form['nama']
        jenis_kelamin = request.form['jenis_kelamin']
        tempat_lahir = request.form['tempat_lahir']
        tanggal_lahir = request.form['tanggal_lahir']
        alamat = request.form['alamat']
        keterangan = request.form['keterangan']

        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE hilang 
                SET nama=%s, jenis_kelamin=%s, tempat_lahir=%s, tanggal_lahir=%s,
                    alamat=%s, keterangan=%s
                WHERE id=%s
            """, (nama, jenis_kelamin, tempat_lahir, tanggal_lahir,
                  alamat, keterangan, id))
            conn.commit()
            flash("Data surat hilang berhasil diperbarui", "success")
            return redirect(url_for('hilang.admin_index'))

    return render_template('hilang/admin_tambah.html', data=data, edit=True)

# ----------------------------
# Approve Surat Hilang
# ----------------------------
@hilang_bp.route('/admin/approve/<int:id>')
@login_required
@admin_required
def admin_approve(id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("UPDATE hilang SET status='approved' WHERE id=%s", (id,))
        conn.commit()
    flash("Surat berhasil di-approve", "success")
    return redirect(url_for('hilang.admin_index'))

# ----------------------------
# Detail Surat Hilang
# ----------------------------
@hilang_bp.route('/admin/detail/<int:id>')
@login_required
@admin_required
def admin_detail(id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM hilang WHERE id = %s", (id,))
        data = cursor.fetchone()

    if not data:
        flash("Data tidak ditemukan", "danger")
        return redirect(url_for('hilang.admin_index'))

    return render_template('hilang/admin_detail.html', data=data)

# ----------------------------
# Cetak Surat Hilang
# ----------------------------
@hilang_bp.route('/admin/cetak/<int:id>')
@login_required
@admin_required
def admin_cetak(id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM hilang WHERE id = %s", (id,))
        data = cursor.fetchone()

    if not data:
        flash("Data tidak ditemukan", "danger")
        return redirect(url_for('hilang.admin_index'))

    return render_template('hilang/cetak.html', data=data)
