from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
from database import get_connection
from utils.security import login_required, admin_required

s_kematian_bp = Blueprint('s_kematian', __name__, url_prefix='/s-kematian')


def gen_no_surat():
    return f"SKK-{datetime.now().strftime('%Y%m%d%H%M%S')}"


# ------------------- AUTOCOMPLETE & GET DATA -------------------
@s_kematian_bp.route('/cari-nik')
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


@s_kematian_bp.route('/penduduk/<nik>')
@login_required
def get_penduduk(nik):
    conn = get_connection()
    with conn.cursor() as c:
        c.execute("""
            SELECT nama, tempat_lahir, tanggal_lahir, jenis_kelamin, alamat
            FROM penduduk WHERE nik=%s
        """, (nik,))
        r = c.fetchone()
        if r:
            return jsonify({
                'nama': r['nama'],
                'tempat_lahir': r['tempat_lahir'],
                'tanggal_lahir': r['tanggal_lahir'].strftime('%Y-%m-%d') if r['tanggal_lahir'] else '',
                'jenis_kelamin': r['jenis_kelamin'],
                'alamat': r['alamat']
            })
    return jsonify({})


# ------------------- INDEX -------------------
@s_kematian_bp.route('/admin')
@login_required
@admin_required
def admin_index():
    conn = get_connection()
    with conn.cursor() as c:
        c.execute("SELECT * FROM s_kematian ORDER BY created_at DESC")
        data = c.fetchall()
    return render_template('s_kematian/index.html', data=data)


# ------------------- TAMBAH -------------------
@s_kematian_bp.route('/admin/tambah', methods=['GET','POST'])
@login_required
@admin_required
def admin_tambah():
    if request.method == 'POST':
        nik = request.form['nik']
        nama = request.form['nama']
        tempat_lahir = request.form['tempat_lahir']
        tanggal_lahir = request.form['tanggal_lahir']
        jenis_kelamin = request.form['jenis_kelamin']
        alamat = request.form['alamat']

        tanggal_meninggal = request.form['tanggal_meninggal']
        tempat_meninggal = request.form['tempat_meninggal']

        no_surat = gen_no_surat()
        pembuat = 'Admin'

        conn = get_connection()
        with conn.cursor() as c:
            c.execute("""
                INSERT INTO s_kematian
                (no_surat, nik, nama, tempat_lahir, tanggal_lahir, jenis_kelamin, alamat,
                 tanggal_meninggal, tempat_meninggal, status, pembuat_surat)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,'pending',%s)
            """, (no_surat, nik, nama, tempat_lahir, tanggal_lahir, jenis_kelamin, alamat,
                  tanggal_meninggal, tempat_meninggal, pembuat))
            conn.commit()
        flash("Surat Kematian berhasil ditambahkan", "success")
        return redirect(url_for('s_kematian.admin_index'))

    return render_template('s_kematian/admin_tambah.html')


# ------------------- EDIT -------------------
@s_kematian_bp.route('/admin/edit/<int:id>', methods=['GET','POST'])
@login_required
@admin_required
def admin_edit(id):
    conn = get_connection()
    with conn.cursor() as c:
        c.execute("SELECT * FROM s_kematian WHERE id=%s", (id,))
        data = c.fetchone()

    if not data:
        flash("Data tidak ditemukan", "danger")
        return redirect(url_for('s_kematian.admin_index'))

    if request.method == 'POST':
        tanggal_meninggal = request.form['tanggal_meninggal']
        tempat_meninggal = request.form['tempat_meninggal']

        with conn.cursor() as c:
            c.execute("""
                UPDATE s_kematian
                SET tanggal_meninggal=%s, tempat_meninggal=%s
                WHERE id=%s
            """, (tanggal_meninggal, tempat_meninggal, id))
            conn.commit()
        flash("Data Kematian berhasil diperbarui", "success")
        return redirect(url_for('s_kematian.admin_index'))

    return render_template('s_kematian/admin_tambah.html', data=data, edit=True)


# ------------------- DETAIL -------------------
@s_kematian_bp.route('/admin/detail/<int:id>')
@login_required
@admin_required
def admin_detail(id):
    conn = get_connection()
    with conn.cursor() as c:
        c.execute("SELECT * FROM s_kematian WHERE id=%s", (id,))
        data = c.fetchone()
    if not data:
        flash("Data tidak ditemukan", "danger")
        return redirect(url_for('s_kematian.admin_index'))
    return render_template('s_kematian/admin_detail.html', data=data)


# ------------------- APPROVE -------------------
@s_kematian_bp.route('/admin/approve/<int:id>')
@login_required
@admin_required
def admin_approve(id):
    conn = get_connection()
    with conn.cursor() as c:
        c.execute("UPDATE s_kematian SET status='approved' WHERE id=%s", (id,))
        conn.commit()
    flash("Surat Kematian berhasil di-approve", "success")
    return redirect(url_for('s_kematian.admin_index'))


# ------------------- CETAK -------------------
@s_kematian_bp.route('/admin/cetak/<int:id>')
@login_required
@admin_required
def admin_cetak(id):
    conn = get_connection()
    with conn.cursor() as c:
        c.execute("SELECT * FROM s_kematian WHERE id=%s", (id,))
        data = c.fetchone()
    if not data:
        flash("Data tidak ditemukan", "danger")
        return redirect(url_for('s_kematian.admin_index'))
    return render_template('s_kematian/cetak.html', data=data)
