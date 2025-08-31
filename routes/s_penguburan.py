from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
from database import get_connection
from utils.security import login_required, admin_required

s_penguburan_bp = Blueprint('s_penguburan', __name__, url_prefix='/s-penguburan')


def gen_no_surat():
    return f"SPG-{datetime.now().strftime('%Y%m%d%H%M%S')}"


# ------------------- AUTOCOMPLETE & GET DATA -------------------
@s_penguburan_bp.route('/cari-nik')
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


@s_penguburan_bp.route('/penduduk/<nik>')
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
@s_penguburan_bp.route('/admin')
@login_required
@admin_required
def admin_index():
    conn = get_connection()
    with conn.cursor() as c:
        c.execute("SELECT * FROM s_penguburan ORDER BY created_at DESC")
        data = c.fetchall()
    return render_template('s_penguburan/index.html', data=data)


# ------------------- TAMBAH -------------------
@s_penguburan_bp.route('/admin/tambah', methods=['GET','POST'])
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

        hari_meninggal = request.form['hari_meninggal']
        jam_meninggal = request.form['jam_meninggal']
        hari_penguburan = request.form['hari_penguburan']
        tanggal_penguburan = request.form['tanggal_penguburan']
        lokasi_penguburan = request.form['lokasi_penguburan']
        jam_penguburan = request.form['jam_penguburan']

        no_surat = gen_no_surat()
        pembuat = 'Admin'

        conn = get_connection()
        with conn.cursor() as c:
            c.execute("""
                INSERT INTO s_penguburan
                (no_surat, nik, nama, tempat_lahir, tanggal_lahir, jenis_kelamin, alamat,
                 hari_meninggal, jam_meninggal, hari_penguburan, tanggal_penguburan, lokasi_penguburan, jam_penguburan,
                 status, pembuat_surat)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'pending',%s)
            """, (no_surat, nik, nama, tempat_lahir, tanggal_lahir, jenis_kelamin, alamat,
                  hari_meninggal, jam_meninggal, hari_penguburan, tanggal_penguburan, lokasi_penguburan, jam_penguburan, pembuat))
            conn.commit()
        flash("Surat Penguburan berhasil ditambahkan", "success")
        return redirect(url_for('s_penguburan.admin_index'))

    return render_template('s_penguburan/admin_tambah.html')


# ------------------- EDIT -------------------
@s_penguburan_bp.route('/admin/edit/<int:id>', methods=['GET','POST'])
@login_required
@admin_required
def admin_edit(id):
    conn = get_connection()
    with conn.cursor() as c:
        c.execute("SELECT * FROM s_penguburan WHERE id=%s", (id,))
        data = c.fetchone()

    if not data:
        flash("Data tidak ditemukan", "danger")
        return redirect(url_for('s_penguburan.admin_index'))

    if request.method == 'POST':
        hari_meninggal = request.form['hari_meninggal']
        jam_meninggal = request.form['jam_meninggal']
        hari_penguburan = request.form['hari_penguburan']
        tanggal_penguburan = request.form['tanggal_penguburan']
        lokasi_penguburan = request.form['lokasi_penguburan']
        jam_penguburan = request.form['jam_penguburan']

        with conn.cursor() as c:
            c.execute("""
                UPDATE s_penguburan
                SET hari_meninggal=%s, jam_meninggal=%s,
                    hari_penguburan=%s, tanggal_penguburan=%s,
                    lokasi_penguburan=%s, jam_penguburan=%s
                WHERE id=%s
            """, (hari_meninggal, jam_meninggal, hari_penguburan, tanggal_penguburan, lokasi_penguburan, jam_penguburan, id))
            conn.commit()
        flash("Data Penguburan berhasil diperbarui", "success")
        return redirect(url_for('s_penguburan.admin_index'))

    return render_template('s_penguburan/admin_tambah.html', data=data, edit=True)


# ------------------- DETAIL -------------------
@s_penguburan_bp.route('/admin/detail/<int:id>')
@login_required
@admin_required
def admin_detail(id):
    conn = get_connection()
    with conn.cursor() as c:
        c.execute("SELECT * FROM s_penguburan WHERE id=%s", (id,))
        data = c.fetchone()
    if not data:
        flash("Data tidak ditemukan", "danger")
        return redirect(url_for('s_penguburan.admin_index'))
    return render_template('s_penguburan/admin_detail.html', data=data)


# ------------------- APPROVE -------------------
@s_penguburan_bp.route('/admin/approve/<int:id>')
@login_required
@admin_required
def admin_approve(id):
    conn = get_connection()
    with conn.cursor() as c:
        c.execute("UPDATE s_penguburan SET status='approved' WHERE id=%s", (id,))
        conn.commit()
    flash("Surat Penguburan berhasil di-approve", "success")
    return redirect(url_for('s_penguburan.admin_index'))


# ------------------- CETAK -------------------
@s_penguburan_bp.route('/admin/cetak/<int:id>')
@login_required
@admin_required
def admin_cetak(id):
    conn = get_connection()
    with conn.cursor() as c:
        c.execute("SELECT * FROM s_penguburan WHERE id=%s", (id,))
        data = c.fetchone()
    if not data:
        flash("Data tidak ditemukan", "danger")
        return redirect(url_for('s_penguburan.admin_index'))
    return render_template('s_penguburan/cetak.html', data=data)
