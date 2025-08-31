from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from database import get_connection
from datetime import datetime
from utils.security import login_required, admin_required

izin_potong_bp = Blueprint('izin_potong', __name__, url_prefix='/izin-potong')


def gen_no_surat():
    return f"SIP-{datetime.now().strftime('%Y%m%d%H%M%S')}"


# ------------------- AUTOCOMPLETE & GET DATA -------------------
@izin_potong_bp.route('/cari-nik')
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


@izin_potong_bp.route('/penduduk/<nik>')
@login_required
def get_penduduk(nik):
    conn = get_connection()
    with conn.cursor() as c:
        c.execute("""
            SELECT nama, tempat_lahir, tanggal_lahir, jenis_kelamin, pekerjaan, alamat
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
                'alamat': r['alamat']
            })
    return jsonify({})
    

# ------------------- INDEX -------------------
@izin_potong_bp.route('/admin')
@login_required
@admin_required
def admin_index():
    conn = get_connection()
    with conn.cursor() as c:
        c.execute("SELECT * FROM s_izin_potong ORDER BY created_at DESC")
        data = c.fetchall()
    return render_template('izin_potong/index.html', data=data)


# ------------------- TAMBAH -------------------
@izin_potong_bp.route('/admin/tambah', methods=['GET','POST'])
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
        alamat = request.form['alamat']

        jenis_hewan = request.form['jenis_hewan']
        jumlah_ekor = request.form['jumlah_ekor']
        umur_hewan = request.form['umur_hewan']
        tanggal_potong = request.form['tanggal_potong']
        acara = request.form['acara']
        nama_anak = request.form['nama_anak']
        tempat_acara = request.form['tempat_acara']

        no_surat = gen_no_surat()
        pembuat = 'Admin'

        conn = get_connection()
        with conn.cursor() as c:
            c.execute("""
                INSERT INTO s_izin_potong
                (no_surat, nik, nama, tempat_lahir, tanggal_lahir, jenis_kelamin, pekerjaan, alamat,
                 jenis_hewan, jumlah_ekor, umur_hewan, tanggal_potong, acara, nama_anak, tempat_acara,
                 status, pembuat_surat)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,
                        %s,%s,%s,%s,%s,%s,%s,
                        'pending',%s)
            """, (no_surat, nik, nama, tempat_lahir, tanggal_lahir, jenis_kelamin, pekerjaan, alamat,
                  jenis_hewan, jumlah_ekor, umur_hewan, tanggal_potong, acara, nama_anak, tempat_acara,
                  pembuat))
            conn.commit()
        flash("Surat Izin Potong berhasil ditambahkan", "success")
        return redirect(url_for('izin_potong.admin_index'))

    return render_template('izin_potong/admin_tambah.html')


# ------------------- EDIT -------------------
@izin_potong_bp.route('/admin/edit/<int:id>', methods=['GET','POST'])
@login_required
@admin_required
def admin_edit(id):
    conn = get_connection()
    with conn.cursor() as c:
        c.execute("SELECT * FROM s_izin_potong WHERE id=%s", (id,))
        data = c.fetchone()

    if not data:
        flash("Data tidak ditemukan", "danger")
        return redirect(url_for('izin_potong.admin_index'))

    if request.method == 'POST':
        jenis_hewan = request.form['jenis_hewan']
        jumlah_ekor = request.form['jumlah_ekor']
        umur_hewan = request.form['umur_hewan']
        tanggal_potong = request.form['tanggal_potong']
        acara = request.form['acara']
        nama_anak = request.form['nama_anak']
        tempat_acara = request.form['tempat_acara']

        with conn.cursor() as c:
            c.execute("""
                UPDATE s_izin_potong
                SET jenis_hewan=%s, jumlah_ekor=%s, umur_hewan=%s,
                    tanggal_potong=%s, acara=%s, nama_anak=%s, tempat_acara=%s
                WHERE id=%s
            """, (jenis_hewan, jumlah_ekor, umur_hewan,
                  tanggal_potong, acara, nama_anak, tempat_acara, id))
            conn.commit()
        flash("Data Izin Potong berhasil diperbarui", "success")
        return redirect(url_for('izin_potong.admin_index'))

    return render_template('izin_potong/admin_tambah.html', data=data, edit=True)


# ------------------- DETAIL -------------------
@izin_potong_bp.route('/admin/detail/<int:id>')
@login_required
@admin_required
def admin_detail(id):
    conn = get_connection()
    with conn.cursor() as c:
        c.execute("SELECT * FROM s_izin_potong WHERE id=%s", (id,))
        data = c.fetchone()
    if not data:
        flash("Data tidak ditemukan", "danger")
        return redirect(url_for('izin_potong.admin_index'))
    return render_template('izin_potong/admin_detail.html', data=data)


# ------------------- APPROVE -------------------
@izin_potong_bp.route('/admin/approve/<int:id>')
@login_required
@admin_required
def admin_approve(id):
    conn = get_connection()
    with conn.cursor() as c:
        c.execute("UPDATE s_izin_potong SET status='approved' WHERE id=%s", (id,))
        conn.commit()
    flash("Surat Izin Potong berhasil di-approve", "success")
    return redirect(url_for('izin_potong.admin_index'))


# ------------------- CETAK -------------------
@izin_potong_bp.route('/admin/cetak/<int:id>')
@login_required
@admin_required
def admin_cetak(id):
    conn = get_connection()
    with conn.cursor() as c:
        c.execute("SELECT * FROM s_izin_potong WHERE id=%s", (id,))
        data = c.fetchone()
    if not data:
        flash("Data tidak ditemukan", "danger")
        return redirect(url_for('izin_potong.admin_index'))
    return render_template('izin_potong/cetak.html', data=data)
