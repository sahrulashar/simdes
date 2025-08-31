from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from database import get_connection
from datetime import datetime
from utils.security import login_required, admin_required

sku_bp = Blueprint('sku', __name__, url_prefix='/sku')

def gen_no_surat():
    return f"SKU-{datetime.now().strftime('%Y%m%d%H%M%S')}"

# ===== Autocomplete & Ambil Data Penduduk =====
@sku_bp.route('/cari-nik')
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

@sku_bp.route('/penduduk/<nik>')
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

# ===== Index =====
@sku_bp.route('/admin')
@login_required
@admin_required
def admin_index():
    conn = get_connection()
    with conn.cursor() as c:
        c.execute("SELECT * FROM sku ORDER BY created_at DESC")
        data = c.fetchall()
    return render_template('sku/index.html', data=data)

# ===== Tambah =====
@sku_bp.route('/admin/tambah', methods=['GET','POST'])
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
        nama_usaha = request.form['nama_usaha']
        tempat_usaha = request.form['tempat_usaha']
        dusun = request.form['dusun']

        no_surat = gen_no_surat()
        pembuat = 'Admin'

        conn = get_connection()
        with conn.cursor() as c:
            c.execute("""
                INSERT INTO sku
                (no_surat, nik, nama, tempat_lahir, tanggal_lahir, pekerjaan, alamat,
                 nama_usaha, tempat_usaha, dusun, status, pembuat_surat)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'pending',%s)
            """, (no_surat, nik, nama, tempat_lahir, tanggal_lahir, pekerjaan, alamat,
                  nama_usaha, tempat_usaha, dusun, pembuat))
            conn.commit()
        flash('SKU berhasil ditambahkan.', 'success')
        return redirect(url_for('sku.admin_index'))
    return render_template('sku/admin_tambah.html')

# ===== Edit =====
@sku_bp.route('/admin/edit/<int:id>', methods=['GET','POST'])
@login_required
@admin_required
def admin_edit(id):
    conn = get_connection()
    with conn.cursor() as c:
        c.execute("SELECT * FROM sku WHERE id=%s", (id,))
        data = c.fetchone()
    if not data:
        flash('Data tidak ditemukan', 'danger')
        return redirect(url_for('sku.admin_index'))

    if request.method == 'POST':
        nama = request.form['nama']
        tempat_lahir = request.form['tempat_lahir']
        tanggal_lahir = request.form['tanggal_lahir']
        pekerjaan = request.form['pekerjaan']
        alamat = request.form['alamat']
        nama_usaha = request.form['nama_usaha']
        tempat_usaha = request.form['tempat_usaha']
        dusun = request.form['dusun']

        with conn.cursor() as c:
            c.execute("""
                UPDATE sku SET
                nama=%s, tempat_lahir=%s, tanggal_lahir=%s, pekerjaan=%s, alamat=%s,
                nama_usaha=%s, tempat_usaha=%s, dusun=%s
                WHERE id=%s
            """, (nama, tempat_lahir, tanggal_lahir, pekerjaan, alamat,
                  nama_usaha, tempat_usaha, dusun, id))
            conn.commit()
        flash('SKU berhasil diperbarui', 'success')
        return redirect(url_for('sku.admin_index'))

    return render_template('sku/admin_tambah.html', data=data, edit=True)

# ===== Detail =====
@sku_bp.route('/admin/detail/<int:id>')
@login_required
@admin_required
def admin_detail(id):
    conn = get_connection()
    with conn.cursor() as c:
        c.execute("SELECT * FROM sku WHERE id=%s", (id,))
        data = c.fetchone()
    if not data:
        flash('Data tidak ditemukan', 'danger')
        return redirect(url_for('sku.admin_index'))
    return render_template('sku/admin_detail.html', data=data)

# ===== Approve =====
@sku_bp.route('/admin/approve/<int:id>')
@login_required
@admin_required
def admin_approve(id):
    conn = get_connection()
    with conn.cursor() as c:
        c.execute("UPDATE sku SET status='approved' WHERE id=%s", (id,))
        conn.commit()
    flash('Surat di-approve', 'success')
    return redirect(url_for('sku.admin_index'))

# ===== Cetak =====
@sku_bp.route('/admin/cetak/<int:id>')
@login_required
@admin_required
def admin_cetak(id):
    conn = get_connection()
    with conn.cursor() as c:
        c.execute("SELECT * FROM sku WHERE id=%s", (id,))
        data = c.fetchone()
    if not data:
        flash('Data tidak ditemukan', 'danger')
        return redirect(url_for('sku.admin_index'))
    return render_template('sku/cetak.html', data=data)
