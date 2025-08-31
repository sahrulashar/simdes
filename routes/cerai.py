from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from database import get_connection
from datetime import datetime
from utils.security import login_required, admin_required

cerai_bp = Blueprint('cerai', __name__, url_prefix='/cerai')

def gen_no_surat():
    return f"SCR-{datetime.now().strftime('%Y%m%d%H%M%S')}"


# ================= AUTOCOMPLETE & DATA PENDUDUK =================
@cerai_bp.route('/cari-nik')
@login_required
def cari_nik():
    term = request.args.get('term', '')
    conn = get_connection()
    with conn.cursor() as c:
        c.execute("""
            SELECT nik, nama FROM penduduk
            WHERE nik LIKE %s OR nama LIKE %s
            LIMIT 10
        """, (f"%{term}%", f"%{term}%"))
        return jsonify([f"{r['nik']} - {r['nama']}" for r in c.fetchall()])


@cerai_bp.route('/penduduk/<nik>')
@login_required
def get_penduduk(nik):
    conn = get_connection()
    with conn.cursor() as c:
        c.execute("""
            SELECT nama, tempat_lahir, tanggal_lahir, jenis_kelamin, pekerjaan, agama, alamat
            FROM penduduk WHERE nik=%s
        """, (nik,))
        r = c.fetchone()
        if r:
            return jsonify({
                'nama': r['nama'],
                'tempat_lahir': r['tempat_lahir'],
                'tanggal_lahir': r['tanggal_lahir'].strftime('%Y-%m-%d') if r['tanggal_lahir'] else '',
                'jenis_kelamin': r['jenis_kelamin'],
                'pekerjaan': r['pekerjaan'],
                'agama': r['agama'],
                'alamat': r['alamat']
            })
    return jsonify({})


# ================== INDEX ==================
@cerai_bp.route('/admin')
@login_required
@admin_required
def admin_index():
    conn = get_connection()
    with conn.cursor() as c:
        c.execute("SELECT * FROM s_cerai ORDER BY created_at DESC")
        data = c.fetchall()
    return render_template('cerai/index.html', data=data)


# ================== TAMBAH ==================
@cerai_bp.route('/admin/tambah', methods=['GET','POST'])
@login_required
@admin_required
def admin_tambah():
    if request.method == 'POST':
        nik = request.form['nik']
        nama = request.form['nama']
        tempat_lahir = request.form['tempat_lahir']
        tanggal_lahir = request.form['tanggal_lahir']
        jenis_kelamin = request.form['jenis_kelamin']
        pekerjaan = request.form['pekerjaan']
        agama = request.form['agama']
        alamat = request.form['alamat']
        nama_pasangan = request.form['nama_pasangan']
        tahun_cerai = request.form['tahun_cerai']

        no_surat = gen_no_surat()
        pembuat = 'Admin'

        conn = get_connection()
        with conn.cursor() as c:
            c.execute("""
                INSERT INTO s_cerai
                (no_surat, nik, nama, tempat_lahir, tanggal_lahir, jenis_kelamin, pekerjaan, agama, alamat,
                 nama_pasangan, tahun_cerai, status, pembuat_surat)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'pending',%s)
            """, (no_surat, nik, nama, tempat_lahir, tanggal_lahir, jenis_kelamin,
                  pekerjaan, agama, alamat, nama_pasangan, tahun_cerai, pembuat))
            conn.commit()
        flash('Surat Cerai berhasil ditambahkan.', 'success')
        return redirect(url_for('cerai.admin_index'))

    return render_template('cerai/admin_tambah.html')


# ================== EDIT ==================
@cerai_bp.route('/admin/edit/<int:id>', methods=['GET','POST'])
@login_required
@admin_required
def admin_edit(id):
    conn = get_connection()
    with conn.cursor() as c:
        c.execute("SELECT * FROM s_cerai WHERE id=%s", (id,))
        data = c.fetchone()
    if not data:
        flash('Data tidak ditemukan', 'danger')
        return redirect(url_for('cerai.admin_index'))

    if request.method == 'POST':
        nama = request.form['nama']
        tempat_lahir = request.form['tempat_lahir']
        tanggal_lahir = request.form['tanggal_lahir']
        jenis_kelamin = request.form['jenis_kelamin']
        pekerjaan = request.form['pekerjaan']
        agama = request.form['agama']
        alamat = request.form['alamat']
        nama_pasangan = request.form['nama_pasangan']
        tahun_cerai = request.form['tahun_cerai']

        with conn.cursor() as c:
            c.execute("""
                UPDATE s_cerai SET
                nama=%s, tempat_lahir=%s, tanggal_lahir=%s, jenis_kelamin=%s,
                pekerjaan=%s, agama=%s, alamat=%s, nama_pasangan=%s, tahun_cerai=%s
                WHERE id=%s
            """, (nama, tempat_lahir, tanggal_lahir, jenis_kelamin,
                  pekerjaan, agama, alamat, nama_pasangan, tahun_cerai, id))
            conn.commit()
        flash('Data Cerai berhasil diperbarui', 'success')
        return redirect(url_for('cerai.admin_index'))

    return render_template('cerai/admin_tambah.html', data=data, edit=True)


# ================== DETAIL ==================
@cerai_bp.route('/admin/detail/<int:id>')
@login_required
@admin_required
def admin_detail(id):
    conn = get_connection()
    with conn.cursor() as c:
        c.execute("SELECT * FROM s_cerai WHERE id=%s", (id,))
        data = c.fetchone()
    if not data:
        flash('Data tidak ditemukan', 'danger')
        return redirect(url_for('cerai.admin_index'))
    return render_template('cerai/admin_detail.html', data=data)


# ================== APPROVE ==================
@cerai_bp.route('/admin/approve/<int:id>')
@login_required
@admin_required
def admin_approve(id):
    conn = get_connection()
    with conn.cursor() as c:
        c.execute("UPDATE s_cerai SET status='approved' WHERE id=%s", (id,))
        conn.commit()
    flash('Surat Cerai berhasil di-approve', 'success')
    return redirect(url_for('cerai.admin_index'))


# ================== CETAK ==================
@cerai_bp.route('/admin/cetak/<int:id>')
@login_required
@admin_required
def admin_cetak(id):
    conn = get_connection()
    with conn.cursor() as c:
        c.execute("SELECT * FROM s_cerai WHERE id=%s", (id,))
        data = c.fetchone()
    if not data:
        flash('Data tidak ditemukan', 'danger')
        return redirect(url_for('cerai.admin_index'))
    return render_template('cerai/cetak.html', data=data)
