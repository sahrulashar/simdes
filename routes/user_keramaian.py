# routes/user_keramaian.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime, date
from database import get_connection

user_keramaian_bp = Blueprint('user_keramaian', __name__, url_prefix='/keramaian')


def get_client_ip():
    """Ambil IP dari pengunjung, termasuk jika di balik proxy"""
    if request.headers.getlist("X-Forwarded-For"):
        return request.headers.getlist("X-Forwarded-For")[0]
    return request.remote_addr


# -------------------------------
# Halaman Form Surat Keramaian untuk User
# -------------------------------
@user_keramaian_bp.route('/form', methods=['GET', 'POST'])
def form_keramaian():
    conn = get_connection()
    with conn.cursor() as cursor:
        ip = get_client_ip()
        today = date.today()

        # Log kunjungan harian
        cursor.execute("""
            SELECT COUNT(*) AS total 
            FROM kunjungan 
            WHERE ip_address=%s AND tanggal=%s
        """, (ip, today))
        exists = cursor.fetchone()['total']

        if not exists:
            cursor.execute("""
                INSERT INTO kunjungan (tanggal, ip_address, created_at) 
                VALUES (%s, %s, NOW())
            """, (today, ip))
            conn.commit()

        cursor.execute("""
            SELECT COUNT(*) AS total 
            FROM kunjungan 
            WHERE tanggal = %s
        """, (today,))
        jumlah_kunjungan = cursor.fetchone()['total']

        # Submit form
        if request.method == 'POST':
            nik = request.form['nik']
            nama = request.form['nama']
            umur = request.form['umur']
            pekerjaan = request.form['pekerjaan']
            alamat = request.form['alamat']
            kegiatan = request.form['kegiatan']
            tanggal_acara = request.form['tanggal_acara']
            tempat = request.form['tempat']
            dusun = request.form['dusun']
            pembuat = 'User'
            no_surat = f"KRM-{datetime.now().strftime('%Y%m%d%H%M%S')}"

            cursor.execute("""
                INSERT INTO keramaian (
                    no_surat, nik, nama, umur, pekerjaan, alamat,
                    kegiatan, tanggal_acara, tempat, dusun, status, pembuat_surat
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'pending', %s)
            """, (no_surat, nik, nama, umur, pekerjaan, alamat,
                  kegiatan, tanggal_acara, tempat, dusun, pembuat))
            conn.commit()

            flash("Permohonan berhasil dikirim. Silakan tunggu konfirmasi dari kantor desa.", "success")
            return redirect(url_for('user_keramaian.form_keramaian'))

    conn.close()
    return render_template('user/keramaian_form.html', now=datetime.now, jumlah_kunjungan=jumlah_kunjungan)


# -------------------------------
# API: Ambil Data Otomatis dari KK & NIK
# -------------------------------
@user_keramaian_bp.route('/ambil-data')
def ambil_data_penduduk_keramaian():
    no_kk = request.args.get('no_kk')
    nik = request.args.get('nik')

    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT 
                p.nama,
                TIMESTAMPDIFF(YEAR, p.tanggal_lahir, CURDATE()) AS umur,
                p.pekerjaan,
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
            WHERE p.nik = %s AND p.no_kk = %s
        """, (nik, no_kk))
        row = cursor.fetchone()

        if row:
            return jsonify({
                'found': True,
                'nama': row['nama'],
                'umur': row['umur'],
                'pekerjaan': row['pekerjaan'],
                'alamat': row['alamat']
            })
        else:
            return jsonify({'found': False})
