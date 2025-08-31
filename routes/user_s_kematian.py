from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime, date
from database import get_connection

user_s_kematian_bp = Blueprint('user_s_kematian', __name__, url_prefix='/s-kematian')


def get_client_ip():
    if request.headers.getlist("X-Forwarded-For"):
        return request.headers.getlist("X-Forwarded-For")[0]
    return request.remote_addr


# -------------------------------
# Form User SK Kematian
# -------------------------------
@user_s_kematian_bp.route('/form', methods=['GET', 'POST'])
def form_s_kematian():
    conn = get_connection()
    with conn.cursor() as cursor:
        ip = get_client_ip()
        today = date.today()

        # log kunjungan
        cursor.execute("""
            SELECT COUNT(*) AS total 
            FROM kunjungan 
            WHERE ip_address=%s AND tanggal=%s
        """, (ip, today))
        if cursor.fetchone()['total'] == 0:
            cursor.execute("""
                INSERT INTO kunjungan (tanggal, ip_address, created_at) 
                VALUES (%s,%s,NOW())
            """, (today, ip))
            conn.commit()

        cursor.execute("SELECT COUNT(*) AS total FROM kunjungan WHERE tanggal=%s", (today,))
        jumlah_kunjungan = cursor.fetchone()['total']

        # submit form
        if request.method == 'POST':
            no_kk = request.form['no_kk']
            nik = request.form['nik']
            nama = request.form['nama']
            tempat_lahir = request.form['tempat_lahir']
            tanggal_lahir = request.form['tanggal_lahir']
            jenis_kelamin = request.form['jenis_kelamin']
            alamat = request.form['alamat']

            tanggal_meninggal = request.form['tanggal_meninggal']
            tempat_meninggal = request.form['tempat_meninggal']

            no_surat = f"SKK-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            pembuat = 'User'

            cursor.execute("""
                INSERT INTO s_kematian
                (no_surat, nik, nama, tempat_lahir, tanggal_lahir, jenis_kelamin, alamat,
                 tanggal_meninggal, tempat_meninggal, status, pembuat_surat)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,'pending',%s)
            """, (no_surat, nik, nama, tempat_lahir, tanggal_lahir, jenis_kelamin, alamat,
                  tanggal_meninggal, tempat_meninggal, pembuat))
            conn.commit()

            flash("Permohonan berhasil dikirim. Silakan ambil surat di kantor desa.", "success")
            return redirect(url_for('user_s_kematian.form_s_kematian'))

    conn.close()
    return render_template('user/s_kematian_form.html', now=datetime.now, jumlah_kunjungan=jumlah_kunjungan)


# -------------------------------
# API: Ambil Data Penduduk by KK & NIK
# -------------------------------
@user_s_kematian_bp.route('/ambil-data')
def ambil_data():
    no_kk = request.args.get('no_kk')
    nik = request.args.get('nik')

    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT 
                p.nama,
                p.tempat_lahir,
                p.tanggal_lahir,
                p.jenis_kelamin,
                CONCAT_WS(', ',
                    kk.dusun,
                    CONCAT('RT ', kk.rt, '/RW ', kk.rw),
                    CONCAT('Desa ', kk.desa),
                    CONCAT('Kec. ', kk.kecamatan),
                    kk.kabupaten,
                    kk.provinsi
                ) AS alamat
            FROM penduduk p
            JOIN kartu_keluarga kk ON p.no_kk = kk.no_kk
            WHERE p.nik=%s AND p.no_kk=%s
        """, (nik, no_kk))
        row = cursor.fetchone()

        if row:
            return jsonify({
                'found': True,
                'nama': row['nama'],
                'tempat_lahir': row['tempat_lahir'],
                'tanggal_lahir': row['tanggal_lahir'].strftime('%Y-%m-%d') if row['tanggal_lahir'] else '',
                'jenis_kelamin': row['jenis_kelamin'],
                'alamat': row['alamat']
            })
    return jsonify({'found': False})
