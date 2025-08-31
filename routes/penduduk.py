from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from database import get_connection
from utils.security import login_required, admin_required

penduduk_bp = Blueprint('penduduk', __name__)

# -------------------------------
# List Semua Penduduk
# -------------------------------
@penduduk_bp.route('/penduduk')
@login_required
@admin_required
def index():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT p.*, kk.dusun
            FROM penduduk p
            LEFT JOIN kartu_keluarga kk ON p.no_kk = kk.no_kk
        """)
        data = cursor.fetchall()
    return render_template('penduduk/index.html', data=data)

# -------------------------------
# Tambah Penduduk
# -------------------------------
@penduduk_bp.route('/penduduk/tambah', methods=['GET', 'POST'])
@login_required
@admin_required
def tambah():
    conn = get_connection()
    with conn.cursor() as cursor:
        if request.method == 'POST':
            try:
                sql = """
                    INSERT INTO penduduk
                    (no_kk, nik, nama, alamat, jenis_kelamin, tempat_lahir, tanggal_lahir,
                     agama, pendidikan, pekerjaan, status_kawin, kewarganegaraan)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    request.form['no_kk'],
                    request.form['nik'],
                    request.form['nama'],
                    request.form['alamat'],
                    request.form['jenis_kelamin'],
                    request.form['tempat_lahir'],
                    request.form['tanggal_lahir'],
                    request.form['agama'],
                    request.form['pendidikan'],
                    request.form['pekerjaan'],
                    request.form['status_kawin'],
                    request.form['kewarganegaraan']
                ))
                conn.commit()
                flash('Data penduduk berhasil ditambahkan', 'success')
                return redirect(url_for('penduduk.index'))
            except Exception as e:
                conn.rollback()
                flash(f'Gagal menambahkan penduduk: {e}', 'danger')

        cursor.execute("SELECT no_kk, dusun FROM kartu_keluarga ORDER BY no_kk")
        daftar_kk = cursor.fetchall()

    return render_template('penduduk/tambah.html', daftar_kk=daftar_kk)

# -------------------------------
# Detail Penduduk
# -------------------------------
@penduduk_bp.route('/penduduk/detail/<int:id>')
@login_required
@admin_required
def detail(id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT p.*, kk.dusun
            FROM penduduk p
            LEFT JOIN kartu_keluarga kk ON p.no_kk = kk.no_kk
            WHERE p.id = %s
        """, (id,))
        data = cursor.fetchone()
    return render_template('penduduk/detail.html', data=data)

# -------------------------------
# Edit Penduduk
# -------------------------------
@penduduk_bp.route('/penduduk/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit(id):
    conn = get_connection()
    with conn.cursor() as cursor:
        if request.method == 'POST':
            try:
                sql = """
                    UPDATE penduduk
                    SET no_kk=%s, nik=%s, nama=%s, alamat=%s, jenis_kelamin=%s,
                        tempat_lahir=%s, tanggal_lahir=%s, agama=%s, pendidikan=%s,
                        pekerjaan=%s, status_kawin=%s, kewarganegaraan=%s
                    WHERE id = %s
                """
                cursor.execute(sql, (
                    request.form['no_kk'], request.form['nik'], request.form['nama'],
                    request.form['alamat'], request.form['jenis_kelamin'], request.form['tempat_lahir'],
                    request.form['tanggal_lahir'], request.form['agama'], request.form['pendidikan'],
                    request.form['pekerjaan'], request.form['status_kawin'], request.form['kewarganegaraan'],
                    id
                ))
                conn.commit()
                flash('Data penduduk berhasil diubah', 'success')
                return redirect(url_for('penduduk.index'))
            except Exception as e:
                conn.rollback()
                flash(f"Gagal memperbarui data: {e}", "danger")

        cursor.execute("SELECT * FROM penduduk WHERE id = %s", (id,))
        data = cursor.fetchone()
        cursor.execute("SELECT no_kk, dusun FROM kartu_keluarga ORDER BY no_kk")
        daftar_kk = cursor.fetchall()

    return render_template('penduduk/tambah.html', data=data, daftar_kk=daftar_kk, edit=True)

# -------------------------------
# Hapus Penduduk
# -------------------------------
@penduduk_bp.route('/penduduk/hapus/<int:id>')
@login_required
@admin_required
def hapus(id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM penduduk WHERE id = %s", (id,))
            conn.commit()
            flash('Data penduduk berhasil dihapus', 'danger')
    except Exception as e:
        conn.rollback()
        flash(f"Gagal menghapus data: {e}", "danger")
    return redirect(url_for('penduduk.index'))

# -------------------------------
# Auto-complete KK
# -------------------------------
@penduduk_bp.route('/penduduk/cari-kk')
@login_required
def cari_kk():
    term = request.args.get('term', '')
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT no_kk, dusun FROM kartu_keluarga
            WHERE no_kk LIKE %s OR dusun LIKE %s
            LIMIT 10
        """, (f"%{term}%", f"%{term}%"))
        hasil = [f"{row['no_kk']} - {row['dusun']}" for row in cursor.fetchall()]
    return jsonify(hasil)

# -------------------------------
# Detail Nama + Tanggal Lahir dari NIK
# -------------------------------
@penduduk_bp.route('/penduduk/detail-by-nik/<nik>')
@login_required
def detail_by_nik(nik):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT nama, tanggal_lahir FROM penduduk WHERE nik = %s", (nik,))
        row = cursor.fetchone()
        if row:
            return jsonify({
                'nama': row['nama'],
                'tanggal_lahir': row['tanggal_lahir'].strftime('%Y-%m-%d') if row['tanggal_lahir'] else ''
            })
    return jsonify({})
