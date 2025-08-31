from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from database import get_connection
from datetime import datetime
from utils.security import login_required, admin_required

skm_bp = Blueprint('skm', __name__, url_prefix='/skm')

# ============== UTIL PENOMORAN (opsional, simple timestamp) ==============
def gen_no_surat():
    return f"SKM-{datetime.now().strftime('%Y%m%d%H%M%S')}"

# ===================== AUTOCOMPLETE & AMBIL DATA PENDUDUK =================
@skm_bp.route('/cari-nik')
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
        hasil = [f"{r['nik']} - {r['nama']}" for r in c.fetchall()]
    return jsonify(hasil)

@skm_bp.route('/penduduk/<nik>')
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

# =============================== INDEX ===================================
@skm_bp.route('/admin')
@login_required
@admin_required
def admin_index():
    conn = get_connection()
    with conn.cursor() as c:
        c.execute("SELECT * FROM s_kurang_mampu ORDER BY created_at DESC")
        data = c.fetchall()
    return render_template('skm/index.html', data=data)

# =============================== TAMBAH ==================================
@skm_bp.route('/admin/tambah', methods=['GET','POST'])
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
        pembuat = 'Admin'
        no_surat = gen_no_surat()

        conn = get_connection()
        with conn.cursor() as c:
            c.execute("""
                INSERT INTO s_kurang_mampu
                (no_surat, nik, nama, tempat_lahir, tanggal_lahir, pekerjaan, alamat, status, pembuat_surat)
                VALUES (%s,%s,%s,%s,%s,%s,%s,'pending',%s)
            """, (no_surat, nik, nama, tempat_lahir, tanggal_lahir, pekerjaan, alamat, pembuat))
            conn.commit()
        flash('Surat Keterangan Kurang Mampu berhasil ditambahkan.', 'success')
        return redirect(url_for('skm.admin_index'))

    return render_template('skm/admin_tambah.html')

# ================================ EDIT ===================================
@skm_bp.route('/admin/edit/<int:id>', methods=['GET','POST'])
@login_required
@admin_required
def admin_edit(id):
    conn = get_connection()
    with conn.cursor() as c:
        c.execute("SELECT * FROM s_kurang_mampu WHERE id=%s", (id,))
        data = c.fetchone()

    if not data:
        flash('Data tidak ditemukan', 'danger')
        return redirect(url_for('skm.admin_index'))

    if request.method == 'POST':
        nama = request.form['nama']
        tempat_lahir = request.form['tempat_lahir']
        tanggal_lahir = request.form['tanggal_lahir']
        pekerjaan = request.form['pekerjaan']
        alamat = request.form['alamat']

        with conn.cursor() as c:
            c.execute("""
                UPDATE s_kurang_mampu SET
                nama=%s, tempat_lahir=%s, tanggal_lahir=%s, pekerjaan=%s, alamat=%s
                WHERE id=%s
            """, (nama, tempat_lahir, tanggal_lahir, pekerjaan, alamat, id))
            conn.commit()
        flash('Data SKM berhasil diperbarui', 'success')
        return redirect(url_for('skm.admin_index'))

    return render_template('skm/admin_tambah.html', data=data, edit=True)

# =============================== DETAIL ==================================
@skm_bp.route('/admin/detail/<int:id>')
@login_required
@admin_required
def admin_detail(id):
    conn = get_connection()
    with conn.cursor() as c:
        c.execute("SELECT * FROM s_kurang_mampu WHERE id=%s", (id,))
        data = c.fetchone()

    if not data:
        flash('Data tidak ditemukan', 'danger')
        return redirect(url_for('skm.admin_index'))

    return render_template('skm/admin_detail.html', data=data)

# ============================== APPROVE ==================================
@skm_bp.route('/admin/approve/<int:id>')
@login_required
@admin_required
def admin_approve(id):
    conn = get_connection()
    with conn.cursor() as c:
        c.execute("UPDATE s_kurang_mampu SET status='approved' WHERE id=%s", (id,))
        conn.commit()
    flash('Surat berhasil di-approve', 'success')
    return redirect(url_for('skm.admin_index'))

# ================================ CETAK ==================================
@skm_bp.route('/admin/cetak/<int:id>')
@login_required
@admin_required
def admin_cetak(id):
    conn = get_connection()
    with conn.cursor() as c:
        c.execute("SELECT * FROM s_kurang_mampu WHERE id=%s", (id,))
        data = c.fetchone()

    if not data:
        flash('Data tidak ditemukan', 'danger')
        return redirect(url_for('skm.admin_index'))

    return render_template('skm/cetak.html', data=data)
