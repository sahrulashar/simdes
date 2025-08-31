from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from database import get_connection
from datetime import datetime
from utils.security import login_required, admin_required

sktm_bp = Blueprint('sktm', __name__, url_prefix='/sktm')

# ----------------------------
# Autocomplete NIK dan Nama
# ----------------------------
@sktm_bp.route('/cari-nik')
@login_required
def cari_nik_sktm():
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
@sktm_bp.route('/penduduk/<nik>')
@login_required
def get_penduduk_sktm(nik):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT p.no_kk, p.nama, p.jenis_kelamin, p.tempat_lahir, p.tanggal_lahir, p.alamat,
                   kk.desa, kk.kecamatan, kk.kabupaten, kk.provinsi
            FROM penduduk p
            LEFT JOIN kartu_keluarga kk ON p.no_kk = kk.no_kk
            WHERE p.nik = %s
        """, (nik,))
        row = cursor.fetchone()
        if row:
            return jsonify({
                'no_kk': row['no_kk'],
                'nama': row['nama'],
                'jenis_kelamin': row['jenis_kelamin'],
                'tempat_lahir': row['tempat_lahir'],
                'tanggal_lahir': row['tanggal_lahir'].strftime('%Y-%m-%d') if row['tanggal_lahir'] else '',
                'alamat': row['alamat'],
                'desa': row['desa'],
                'kecamatan': row['kecamatan'],
                'kabupaten': row['kabupaten'],
                'provinsi': row['provinsi']
            })
    return jsonify({})

# ----------------------------
# Halaman daftar SKTM (Admin)
# ----------------------------
@sktm_bp.route('/admin')
@login_required
@admin_required
def admin_index():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM sktm ORDER BY created_at DESC")
        data = cursor.fetchall()
    return render_template('sktm/index.html', data=data)

# ----------------------------
# Tambah SKTM (Admin)
# ----------------------------
@sktm_bp.route('/admin/tambah', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_tambah():
    if request.method == 'POST':
        nik = request.form['nik']
        no_kk = request.form['no_kk']
        nama = request.form['nama']
        jenis_kelamin = request.form['jenis_kelamin']
        tempat_lahir = request.form['tempat_lahir']
        tanggal_lahir = request.form['tanggal_lahir']
        alamat = request.form['alamat']
        keperluan = request.form['keperluan']
        pembuat = 'Admin'
        no_surat = f"SKTM-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO sktm 
                (no_surat, no_kk, nik, nama, jenis_kelamin, tempat_lahir, tanggal_lahir,
                 alamat, keperluan, status, pembuat_surat)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'pending', %s)
            """, (no_surat, no_kk, nik, nama, jenis_kelamin, tempat_lahir, tanggal_lahir,
                  alamat, keperluan, pembuat))
            conn.commit()
            flash("Surat SKTM berhasil ditambahkan.", "success")
            return redirect(url_for('sktm.admin_index'))

    return render_template('sktm/admin_tambah.html')

# ----------------------------
# Edit SKTM
# ----------------------------
@sktm_bp.route('/admin/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_edit(id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM sktm WHERE id = %s", (id,))
        data = cursor.fetchone()

    if not data:
        flash("Data tidak ditemukan", "danger")
        return redirect(url_for('sktm.admin_index'))

    if request.method == 'POST':
        no_kk = request.form['no_kk']
        nik = request.form['nik']
        nama = request.form['nama']
        jenis_kelamin = request.form['jenis_kelamin']
        tempat_lahir = request.form['tempat_lahir']
        tanggal_lahir = request.form['tanggal_lahir']
        alamat = request.form['alamat']
        keperluan = request.form['keperluan']

        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE sktm 
                SET no_kk=%s, nik=%s, nama=%s, jenis_kelamin=%s,
                    tempat_lahir=%s, tanggal_lahir=%s, alamat=%s, keperluan=%s
                WHERE id=%s
            """, (no_kk, nik, nama, jenis_kelamin, tempat_lahir,
                  tanggal_lahir, alamat, keperluan, id))
            conn.commit()
            flash("Data SKTM berhasil diperbarui", "success")
            return redirect(url_for('sktm.admin_index'))

    return render_template('sktm/admin_tambah.html', data=data, edit=True)

# ----------------------------
# Approve SKTM
# ----------------------------
@sktm_bp.route('/admin/approve/<int:id>')
@login_required
@admin_required
def admin_approve(id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("UPDATE sktm SET status='approved' WHERE id=%s", (id,))
        conn.commit()
    flash("Surat berhasil di-approve", "success")
    return redirect(url_for('sktm.admin_index'))

# ----------------------------
# Detail SKTM
# ----------------------------
@sktm_bp.route('/admin/detail/<int:id>')
@login_required
@admin_required
def admin_detail(id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM sktm WHERE id = %s", (id,))
        data = cursor.fetchone()

    if not data:
        flash("Data tidak ditemukan", "danger")
        return redirect(url_for('sktm.admin_index'))

    return render_template('sktm/admin_detail.html', data=data)

# ----------------------------
# Cetak SKTM
# ----------------------------
@sktm_bp.route('/admin/cetak/<int:id>')
@login_required
@admin_required
def admin_cetak(id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM sktm WHERE id = %s", (id,))
        data = cursor.fetchone()

    if not data:
        flash("Data tidak ditemukan", "danger")
        return redirect(url_for('sktm.admin_index'))

    return render_template('sktm/cetak.html', data=data)
