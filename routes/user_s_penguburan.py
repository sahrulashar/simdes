from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime, date
from database import get_connection

user_s_penguburan_bp = Blueprint('user_s_penguburan', __name__, url_prefix='/s-penguburan')


def get_client_ip():
    if request.headers.getlist("X-Forwarded-For"):
        return request.headers.getlist("X-Forwarded-For")[0]
    return request.remote_addr


# -------------------------------
# Form User SK Penguburan
# -------------------------------
@user_s_penguburan_bp.route('/form', methods=['GET', 'POST'])
def form_s_penguburan():
    conn = get_connection()
    with conn.cursor() as cursor:
        ip = get_client_ip()
        today = date.today()

        # log kunjungan
        cursor.execute("SELECT COUNT(*) AS total FROM kunjungan WHERE ip_address=%s AND tanggal=%s", (ip, today))
        if cursor.fetchone()['total'] == 0:
            cursor.execute("INSERT INTO kunjungan (tanggal, ip_address, created_at) VALUES (%s,%s,NOW())", (today, ip))
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

            # Normalisasi JK biar sesuai ENUM('L','P')
            if jenis_kelamin.lower().startswith('l'):
                jenis_kelamin = 'L'
            elif jenis_kelamin.lower().startswith('p'):
                jenis_kelamin = 'P'

            hari_meninggal = request.form['hari_meninggal']
            jam_meninggal = request.form['jam_meninggal']
            hari_penguburan = request.form['hari_penguburan']
            tanggal_penguburan = request.form['tanggal_penguburan']
            lokasi_penguburan = request.form['lokasi_penguburan']
            jam_penguburan = request.form['jam_penguburan']

            no_surat = f"SPG-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            pembuat = 'User'

            cursor.execute("""
                INSERT INTO s_penguburan
                (no_surat, nik, nama, tempat_lahir, tanggal_lahir, jenis_kelamin, alamat,
                 hari_meninggal, jam_meninggal, hari_penguburan, tanggal_penguburan, lokasi_penguburan, jam_penguburan,
                 status, pembuat_surat)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'pending',%s)
            """, (no_surat, nik, nama, tempat_lahir, tanggal_lahir, jenis_kelamin, alamat,
                  hari_meninggal, jam_meninggal, hari_penguburan, tanggal_penguburan, lokasi_penguburan, jam_penguburan, pembuat))
            conn.commit()

            flash("Permohonan berhasil dikirim. Silakan ambil surat di kantor desa.", "success")
            return redirect(url_for('user_s_penguburan.form_s_penguburan'))

    conn.close()
    return render_template('user/s_penguburan_form.html', now=datetime.now, jumlah_kunjungan=jumlah_kunjungan)


# -------------------------------
# API: Ambil Data Penduduk by KK & NIK
# -------------------------------
@user_s_penguburan_bp.route('/ambil-data')
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
            # Tampilkan "Laki-laki / Perempuan" ke user, simpan aslinya tetap 'L'/'P'
            return jsonify({
                'found': True,
                'nama': row['nama'],
                'tempat_lahir': row['tempat_lahir'],
                'tanggal_lahir': row['tanggal_lahir'].strftime('%Y-%m-%d') if row['tanggal_lahir'] else '',
                'jenis_kelamin': 'Laki-laki' if row['jenis_kelamin'] == 'L' else 'Perempuan',
                'alamat': row['alamat']
            })
    return jsonify({'found': False})
