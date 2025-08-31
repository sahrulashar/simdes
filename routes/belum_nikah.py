from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from database import get_connection
from datetime import datetime
from utils.security import login_required, admin_required

belum_nikah_bp = Blueprint('belum_nikah', __name__, url_prefix='/belum-nikah')


# ----------------------------
# Helper: Konversi Jenis Kelamin
# ----------------------------
def convert_gender(jk):
    if jk in ['L', 'l']:
        return 'Laki-laki'
    elif jk in ['P', 'p']:
        return 'Perempuan'
    return jk


# ----------------------------
# Autocomplete NIK dan Nama
# ----------------------------
@belum_nikah_bp.route('/cari-nik')
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
@belum_nikah_bp.route('/penduduk/<nik>')
@login_required
def get_penduduk(nik):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT nik, nama, jenis_kelamin, tempat_lahir, tanggal_lahir,
                   pekerjaan, alamat
            FROM penduduk
            WHERE nik = %s
        """, (nik,))
        row = cursor.fetchone()
        if row:
            return jsonify({
                'nik': row['nik'],
                'nama': row['nama'],
                'jenis_kelamin': convert_gender(row['jenis_kelamin']),
                'tempat_lahir': row['tempat_lahir'],
                'tanggal_lahir': row['tanggal_lahir'].strftime('%Y-%m-%d') if row['tanggal_lahir'] else '',
                'pekerjaan': row['pekerjaan'],
                'alamat': row['alamat']
            })
    return jsonify({})


# ----------------------------
# Halaman daftar surat (Admin)
# ----------------------------
@belum_nikah_bp.route('/admin')
@login_required
@admin_required
def admin_index():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM belum_nikah ORDER BY created_at DESC")
        data = cursor.fetchall()
    return render_template('belum_nikah/index.html', data=data)


# ----------------------------
# Tambah Surat Belum Nikah
# ----------------------------
@belum_nikah_bp.route('/admin/tambah', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_tambah():
    if request.method == 'POST':
        try:
            nik = request.form['nik']
            nama = request.form['nama']
            jenis_kelamin = convert_gender(request.form['jenis_kelamin'])
            tempat_lahir = request.form['tempat_lahir']
            tanggal_lahir = request.form['tanggal_lahir']
            pekerjaan = request.form['pekerjaan']
            alamat = request.form['alamat']
            pembuat = 'Admin'
            no_surat = f"BN-{datetime.now().strftime('%Y%m%d%H%M%S')}"

            conn = get_connection()
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO belum_nikah 
                    (no_surat, nik, nama, jenis_kelamin, tempat_lahir, tanggal_lahir,
                     pekerjaan, alamat, status, pembuat_surat)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'pending', %s)
                """, (no_surat, nik, nama, jenis_kelamin, tempat_lahir,
                      tanggal_lahir, pekerjaan, alamat, pembuat))
                conn.commit()
                flash("Surat Belum Nikah berhasil ditambahkan.", "success")
                return redirect(url_for('belum_nikah.admin_index'))
        except Exception as e:
            conn.rollback()
            flash(f"Gagal menambahkan surat: {e}", "danger")

    return render_template('belum_nikah/admin_tambah.html')


# ----------------------------
# Edit Surat
# ----------------------------
@belum_nikah_bp.route('/admin/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_edit(id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM belum_nikah WHERE id = %s", (id,))
        data = cursor.fetchone()

    if not data:
        flash("Data tidak ditemukan", "danger")
        return redirect(url_for('belum_nikah.admin_index'))

    if request.method == 'POST':
        try:
            nama = request.form['nama']
            jenis_kelamin = convert_gender(request.form['jenis_kelamin'])
            tempat_lahir = request.form['tempat_lahir']
            tanggal_lahir = request.form['tanggal_lahir']
            pekerjaan = request.form['pekerjaan']
            alamat = request.form['alamat']

            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE belum_nikah 
                    SET nama=%s, jenis_kelamin=%s, tempat_lahir=%s, tanggal_lahir=%s,
                        pekerjaan=%s, alamat=%s
                    WHERE id=%s
                """, (nama, jenis_kelamin, tempat_lahir, tanggal_lahir,
                      pekerjaan, alamat, id))
                conn.commit()
                flash("Data surat berhasil diperbarui", "success")
                return redirect(url_for('belum_nikah.admin_index'))
        except Exception as e:
            conn.rollback()
            flash(f"Gagal memperbarui data: {e}", "danger")

    return render_template('belum_nikah/admin_tambah.html', data=data, edit=True)


# ----------------------------
# Approve Surat
# ----------------------------
@belum_nikah_bp.route('/admin/approve/<int:id>')
@login_required
@admin_required
def admin_approve(id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("UPDATE belum_nikah SET status='approved' WHERE id=%s", (id,))
        conn.commit()
    flash("Surat berhasil di-approve", "success")
    return redirect(url_for('belum_nikah.admin_index'))


# ----------------------------
# Detail Surat
# ----------------------------
@belum_nikah_bp.route('/admin/detail/<int:id>')
@login_required
@admin_required
def admin_detail(id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM belum_nikah WHERE id = %s", (id,))
        data = cursor.fetchone()

    if not data:
        flash("Data tidak ditemukan", "danger")
        return redirect(url_for('belum_nikah.admin_index'))

    return render_template('belum_nikah/admin_detail.html', data=data)


# ----------------------------
# Cetak Surat
# ----------------------------
@belum_nikah_bp.route('/admin/cetak/<int:id>')
@login_required
@admin_required
def admin_cetak(id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM belum_nikah WHERE id = %s", (id,))
        data = cursor.fetchone()

    if not data:
        flash("Data tidak ditemukan", "danger")
        return redirect(url_for('belum_nikah.admin_index'))

    return render_template('belum_nikah/cetak.html', data=data)
