from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime, date
from database import get_connection

user_izin_potong_bp = Blueprint('user_izin_potong', __name__, url_prefix='/izin-potong')


def get_client_ip():
    if request.headers.getlist("X-Forwarded-For"):
        return request.headers.getlist("X-Forwarded-For")[0]
    return request.remote_addr


# -------------------------------
# Form User SK Izin Potong
# -------------------------------
@user_izin_potong_bp.route('/form', methods=['GET', 'POST'])
def form_izin_potong():
    conn = get_connection()
    with conn.cursor() as cursor:
        ip = get_client_ip()
        today = date.today()

        # log kunjungan harian
        cursor.execute("SELECT COUNT(*) AS total FROM kunjungan WHERE ip_address=%s AND tanggal=%s", (ip, today))
        exists = cursor.fetchone()['total']
        if not exists:
            cursor.execute("INSERT INTO kunjungan (tanggal, ip_address, created_at) VALUES (%s,%s,NOW())", (today, ip))
            conn.commit()

        cursor.execute("SELECT COUNT(*) AS total FROM kunjungan WHERE tanggal=%s", (today,))
        jumlah_kunjungan = cursor.fetchone()['total']

        # proses submit
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

            no_surat = f"SIP-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            pembuat = 'User'

            cursor.execute("""
                INSERT INTO s_izin_potong
                (no_surat, nik, nama, tempat_lahir, tanggal_lahir, jenis_kelamin, pekerjaan, alamat,
                 jenis_hewan, jumlah_ekor, umur_hewan, tanggal_potong, acara, nama_anak, tempat_acara,
                 status, pembuat_surat)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,
                        %s,%s,%s,%s,%s,%s,%s,
                        'pending',%s)
            """, (no_surat, nik, nama, tempat_lahir, tanggal_lahir, jenis_kelamin, pekerjaan, alamat,
                  jenis_hewan, jumlah_ekor, umur_hewan, tanggal_potong, acara, nama_anak, tempat_acara, pembuat))
            conn.commit()

            flash("Permohonan berhasil dikirim. Silakan ambil surat di kantor desa.", "success")
            return redirect(url_for('user_izin_potong.form_izin_potong'))

    conn.close()
    return render_template('user/izin_potong_form.html', now=datetime.now, jumlah_kunjungan=jumlah_kunjungan)


# -------------------------------
# API: Ambil Data Penduduk by NIK
# -------------------------------
@user_izin_potong_bp.route('/ambil-data')
def ambil_data():
    nik = request.args.get('nik')
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT p.nama, p.tempat_lahir, p.tanggal_lahir, p.jenis_kelamin, p.pekerjaan,
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
            WHERE p.nik=%s
        """, (nik,))
        row = cursor.fetchone()
        if row:
            return jsonify({
                'found': True,
                'nama': row['nama'],
                'tempat_lahir': row['tempat_lahir'],
                'tanggal_lahir': row['tanggal_lahir'].strftime('%Y-%m-%d') if row['tanggal_lahir'] else '',
                'jenis_kelamin': row['jenis_kelamin'],
                'pekerjaan': row['pekerjaan'],
                'alamat': row['alamat']
            })
    return jsonify({'found': False})
