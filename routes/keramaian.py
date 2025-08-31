from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from database import get_connection
from datetime import datetime
from utils.security import login_required, admin_required

keramaian_bp = Blueprint('keramaian', __name__, url_prefix='/keramaian')


# ----------------------------
# Autocomplete NIK dan Nama
# ----------------------------
@keramaian_bp.route('/cari-nik')
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
@keramaian_bp.route('/penduduk/<nik>')
@login_required
def get_penduduk(nik):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT nama,
                   TIMESTAMPDIFF(YEAR, tanggal_lahir, CURDATE()) AS umur,
                   pekerjaan,
                   alamat
            FROM penduduk
            WHERE nik = %s
        """, (nik,))
        row = cursor.fetchone()
        if row:
            return jsonify({
                'nama': row['nama'],
                'umur': row['umur'],
                'pekerjaan': row['pekerjaan'],
                'alamat': row['alamat']
            })
    return jsonify({})


# ----------------------------
# Halaman daftar surat keramaian
# ----------------------------
@keramaian_bp.route('/admin')
@login_required
@admin_required
def admin_index():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM keramaian ORDER BY created_at DESC")
        data = cursor.fetchall()
    return render_template('keramaian/index.html', data=data)


# ----------------------------
# Tambah Surat Keramaian
# ----------------------------
@keramaian_bp.route('/admin/tambah', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_tambah():
    if request.method == 'POST':
        nik = request.form['nik']
        nama = request.form['nama']
        umur = request.form['umur']
        pekerjaan = request.form['pekerjaan']
        alamat = request.form['alamat']
        kegiatan = request.form['kegiatan']
        tanggal_acara = request.form['tanggal_acara']
        tempat = request.form['tempat']
        dusun = request.form['dusun']
        pembuat = 'Admin'
        no_surat = f"KRM-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO keramaian 
                (no_surat, nik, nama, umur, pekerjaan, alamat, kegiatan, tanggal_acara,
                 tempat, dusun, status, pembuat_surat)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'pending', %s)
            """, (no_surat, nik, nama, umur, pekerjaan, alamat, kegiatan, tanggal_acara,
                  tempat, dusun, pembuat))
            conn.commit()
            flash("Surat Keramaian berhasil ditambahkan.", "success")
            return redirect(url_for('keramaian.admin_index'))

    return render_template('keramaian/admin_tambah.html')


# ----------------------------
# Edit Surat Keramaian
# ----------------------------
@keramaian_bp.route('/admin/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_edit(id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM keramaian WHERE id = %s", (id,))
        data = cursor.fetchone()

    if not data:
        flash("Data tidak ditemukan", "danger")
        return redirect(url_for('keramaian.admin_index'))

    if request.method == 'POST':
        nama = request.form['nama']
        umur = request.form['umur']
        pekerjaan = request.form['pekerjaan']
        alamat = request.form['alamat']
        kegiatan = request.form['kegiatan']
        tanggal_acara = request.form['tanggal_acara']
        tempat = request.form['tempat']
        dusun = request.form['dusun']

        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE keramaian 
                SET nama=%s, umur=%s, pekerjaan=%s, alamat=%s,
                    kegiatan=%s, tanggal_acara=%s, tempat=%s, dusun=%s
                WHERE id=%s
            """, (nama, umur, pekerjaan, alamat, kegiatan,
                  tanggal_acara, tempat, dusun, id))
            conn.commit()
            flash("Data surat keramaian berhasil diperbarui", "success")
            return redirect(url_for('keramaian.admin_index'))

    return render_template('keramaian/admin_tambah.html', data=data, edit=True)


# ----------------------------
# Approve Surat Keramaian
# ----------------------------
@keramaian_bp.route('/admin/approve/<int:id>')
@login_required
@admin_required
def admin_approve(id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("UPDATE keramaian SET status='approved' WHERE id=%s", (id,))
        conn.commit()
    flash("Surat berhasil di-approve", "success")
    return redirect(url_for('keramaian.admin_index'))


# ----------------------------
# Detail Surat Keramaian
# ----------------------------
@keramaian_bp.route('/admin/detail/<int:id>')
@login_required
@admin_required
def admin_detail(id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM keramaian WHERE id = %s", (id,))
        data = cursor.fetchone()

    if not data:
        flash("Data tidak ditemukan", "danger")
        return redirect(url_for('keramaian.admin_index'))

    return render_template('keramaian/admin_detail.html', data=data)


# ----------------------------
# Cetak Surat Keramaian
# ----------------------------
@keramaian_bp.route('/admin/cetak/<int:id>')
@login_required
@admin_required
def admin_cetak(id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM keramaian WHERE id = %s", (id,))
        data = cursor.fetchone()

    if not data:
        flash("Data tidak ditemukan", "danger")
        return redirect(url_for('keramaian.admin_index'))

    return render_template('keramaian/cetak.html', data=data)
