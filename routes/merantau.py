from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from database import get_connection
from datetime import datetime
from utils.security import login_required, admin_required

merantau_bp = Blueprint('merantau', __name__, url_prefix='/merantau')

def gen_no_surat():
    return f"SMR-{datetime.now().strftime('%Y%m%d%H%M%S')}"


# ==================== AUTOCOMPLETE NIK & DATA ====================
@merantau_bp.route('/cari-nik')
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


@merantau_bp.route('/penduduk/<nik>')
@login_required
def get_penduduk(nik):
    conn = get_connection()
    with conn.cursor() as c:
        c.execute("""
            SELECT nama, tempat_lahir, tanggal_lahir, pekerjaan, alamat
            FROM penduduk WHERE nik=%s
        """, (nik,))
        r = c.fetchone()
        if r:
            return jsonify({
                'nama': r['nama'],
                'tempat_lahir': r['tempat_lahir'],
                'tanggal_lahir': r['tanggal_lahir'].strftime('%Y-%m-%d') if r['tanggal_lahir'] else '',
                'pekerjaan': r['pekerjaan'],
                'alamat': r['alamat']
            })
    return jsonify({})


# ======================= INDEX =======================
@merantau_bp.route('/admin')
@login_required
@admin_required
def admin_index():
    conn = get_connection()
    with conn.cursor() as c:
        c.execute("SELECT * FROM s_merantau ORDER BY created_at DESC")
        data = c.fetchall()
    return render_template('merantau/index.html', data=data)


# ======================= TAMBAH =======================
@merantau_bp.route('/admin/tambah', methods=['GET','POST'])
@login_required
@admin_required
def admin_tambah():
    if request.method == 'POST':
        nik = request.form['nik']
        nama = request.form['nama']
        tempat_lahir = request.form['tempat_lahir']
        tanggal_lahir = request.form['tanggal_lahir']
        pekerjaan = request.form['pekerjaan']
        alamat = request.form['alamat']
        nama_pasangan = request.form['nama_pasangan']
        tujuan_merantau = request.form['tujuan_merantau']

        no_surat = gen_no_surat()
        pembuat = 'Admin'

        conn = get_connection()
        with conn.cursor() as c:
            c.execute("""
                INSERT INTO s_merantau
                (no_surat, nik, nama, tempat_lahir, tanggal_lahir, pekerjaan, alamat,
                 nama_pasangan, tujuan_merantau, status, pembuat_surat)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,'pending',%s)
            """, (no_surat, nik, nama, tempat_lahir, tanggal_lahir, pekerjaan, alamat,
                  nama_pasangan, tujuan_merantau, pembuat))
            conn.commit()
        flash('Surat Merantau berhasil ditambahkan.', 'success')
        return redirect(url_for('merantau.admin_index'))

    return render_template('merantau/admin_tambah.html')


# ======================= EDIT =======================
@merantau_bp.route('/admin/edit/<int:id>', methods=['GET','POST'])
@login_required
@admin_required
def admin_edit(id):
    conn = get_connection()
    with conn.cursor() as c:
        c.execute("SELECT * FROM s_merantau WHERE id=%s", (id,))
        data = c.fetchone()
    if not data:
        flash('Data tidak ditemukan', 'danger')
        return redirect(url_for('merantau.admin_index'))

    if request.method == 'POST':
        nama = request.form['nama']
        tempat_lahir = request.form['tempat_lahir']
        tanggal_lahir = request.form['tanggal_lahir']
        pekerjaan = request.form['pekerjaan']
        alamat = request.form['alamat']
        nama_pasangan = request.form['nama_pasangan']
        tujuan_merantau = request.form['tujuan_merantau']

        with conn.cursor() as c:
            c.execute("""
                UPDATE s_merantau SET
                nama=%s, tempat_lahir=%s, tanggal_lahir=%s, pekerjaan=%s, alamat=%s,
                nama_pasangan=%s, tujuan_merantau=%s
                WHERE id=%s
            """, (nama, tempat_lahir, tanggal_lahir, pekerjaan, alamat,
                  nama_pasangan, tujuan_merantau, id))
            conn.commit()
        flash('Data Merantau berhasil diperbarui', 'success')
        return redirect(url_for('merantau.admin_index'))

    return render_template('merantau/admin_tambah.html', data=data, edit=True)


# ======================= DETAIL =======================
@merantau_bp.route('/admin/detail/<int:id>')
@login_required
@admin_required
def admin_detail(id):
    conn = get_connection()
    with conn.cursor() as c:
        c.execute("SELECT * FROM s_merantau WHERE id=%s", (id,))
        data = c.fetchone()
    if not data:
        flash('Data tidak ditemukan', 'danger')
        return redirect(url_for('merantau.admin_index'))
    return render_template('merantau/admin_detail.html', data=data)


# ======================= APPROVE =======================
@merantau_bp.route('/admin/approve/<int:id>')
@login_required
@admin_required
def admin_approve(id):
    conn = get_connection()
    with conn.cursor() as c:
        c.execute("UPDATE s_merantau SET status='approved' WHERE id=%s", (id,))
        conn.commit()
    flash('Surat Merantau berhasil di-approve', 'success')
    return redirect(url_for('merantau.admin_index'))


# ======================= CETAK =======================
@merantau_bp.route('/admin/cetak/<int:id>')
@login_required
@admin_required
def admin_cetak(id):
    conn = get_connection()
    with conn.cursor() as c:
        c.execute("SELECT * FROM s_merantau WHERE id=%s", (id,))
        data = c.fetchone()
    if not data:
        flash('Data tidak ditemukan', 'danger')
        return redirect(url_for('merantau.admin_index'))
    return render_template('merantau/cetak.html', data=data)
