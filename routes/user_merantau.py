from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime, date
from database import get_connection

user_merantau_bp = Blueprint('user_merantau', __name__, url_prefix='/merantau')


def get_client_ip():
    if request.headers.getlist("X-Forwarded-For"):
        return request.headers.getlist("X-Forwarded-For")[0]
    return request.remote_addr


# -------------------------------
# Halaman Form Merantau (User)
# -------------------------------
@user_merantau_bp.route('/form', methods=['GET', 'POST'])
def form_merantau():
    conn = get_connection()
    with conn.cursor() as cursor:
        ip = get_client_ip()
        today = date.today()

        # log kunjungan
        cursor.execute("SELECT COUNT(*) AS total FROM kunjungan WHERE ip_address=%s AND tanggal=%s", (ip, today))
        exists = cursor.fetchone()['total']
        if not exists:
            cursor.execute("INSERT INTO kunjungan (tanggal, ip_address, created_at) VALUES (%s,%s,NOW())", (today, ip))
            conn.commit()

        cursor.execute("SELECT COUNT(*) AS total FROM kunjungan WHERE tanggal=%s", (today,))
        jumlah_kunjungan = cursor.fetchone()['total']

        if request.method == 'POST':
            nik = request.form['nik']
            nama = request.form['nama']
            tempat_lahir = request.form['tempat_lahir']
            tanggal_lahir = request.form['tanggal_lahir']
            pekerjaan = request.form['pekerjaan']
            alamat = request.form['alamat']
            nama_pasangan = request.form['nama_pasangan']
            tujuan_merantau = request.form['tujuan_merantau']

            no_surat = f"SMR-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            pembuat = 'User'

            cursor.execute("""
                INSERT INTO s_merantau
                (no_surat, nik, nama, tempat_lahir, tanggal_lahir, pekerjaan, alamat,
                 nama_pasangan, tujuan_merantau, status, pembuat_surat)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,'pending',%s)
            """, (no_surat, nik, nama, tempat_lahir, tanggal_lahir, pekerjaan, alamat,
                  nama_pasangan, tujuan_merantau, pembuat))
            conn.commit()

            flash("Permohonan berhasil dikirim. Silakan tunggu konfirmasi dari kantor desa.", "success")
            return redirect(url_for('user_merantau.form_merantau'))

    conn.close()
    return render_template('user/merantau_form.html', now=datetime.now, jumlah_kunjungan=jumlah_kunjungan)


# -------------------------------
# API: Ambil Data Otomatis KK+NIK
# -------------------------------
@user_merantau_bp.route('/ambil-data')
def ambil_data_merantau():
    no_kk = request.args.get('no_kk')
    nik = request.args.get('nik')

    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT p.nama, p.tempat_lahir, p.tanggal_lahir, p.pekerjaan,
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
                'pekerjaan': row['pekerjaan'],
                'alamat': row['alamat']
            })
    return jsonify({'found': False})
