from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime, date
from database import get_connection

user_belum_nikah_bp = Blueprint('user_belum_nikah', __name__, url_prefix='/belum-nikah')


def get_client_ip():
    """Ambil IP dari pengunjung, termasuk jika di balik proxy"""
    if request.headers.getlist("X-Forwarded-For"):
        return request.headers.getlist("X-Forwarded-For")[0]
    return request.remote_addr


# -------------------------------
# Halaman Form Belum Nikah untuk User
# -------------------------------
@user_belum_nikah_bp.route('/form', methods=['GET', 'POST'])
def form_belum_nikah():
    conn = get_connection()
    with conn.cursor() as cursor:
        ip = get_client_ip()
        today = date.today()

        # Hitung kunjungan harian (log pengunjung)
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

        # Jika form disubmit
        if request.method == 'POST':
            nik = request.form['nik']
            nama = request.form['nama']
            jenis_kelamin = request.form['jenis_kelamin']
            tempat_lahir = request.form['tempat_lahir']
            tanggal_lahir = request.form['tanggal_lahir']
            pekerjaan = request.form['pekerjaan']
            alamat = request.form['alamat']
            pembuat = 'User'
            no_surat = f"BN-{datetime.now().strftime('%Y%m%d%H%M%S')}"

            # Konversi gender
            if jenis_kelamin == 'L':
                jenis_kelamin = 'Laki-laki'
            elif jenis_kelamin == 'P':
                jenis_kelamin = 'Perempuan'

            cursor.execute("""
                INSERT INTO belum_nikah (
                    no_surat, nik, nama, jenis_kelamin, tempat_lahir, tanggal_lahir,
                    pekerjaan, alamat, status, pembuat_surat
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'pending', %s)
            """, (no_surat, nik, nama, jenis_kelamin, tempat_lahir,
                  tanggal_lahir, pekerjaan, alamat, pembuat))
            conn.commit()

            flash("Permohonan berhasil dikirim. Silakan ambil surat di kantor desa.", "success")
            return redirect(url_for('user_belum_nikah.form_belum_nikah'))

    conn.close()
    return render_template('user/belum_nikah_form.html', now=datetime.now, jumlah_kunjungan=jumlah_kunjungan)


# -------------------------------
# API: Ambil Data Otomatis dari KK & NIK
# -------------------------------
@user_belum_nikah_bp.route('/ambil-data')
def ambil_data_penduduk():
    no_kk = request.args.get('no_kk')
    nik = request.args.get('nik')

    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT 
                p.nama,
                p.jenis_kelamin,
                p.tempat_lahir,
                p.tanggal_lahir,
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
                'jenis_kelamin': 'Laki-laki' if row['jenis_kelamin'] == 'L' else 'Perempuan',
                'tempat_lahir': row['tempat_lahir'],
                'tanggal_lahir': row['tanggal_lahir'].strftime('%Y-%m-%d') if row['tanggal_lahir'] else '',
                'pekerjaan': row['pekerjaan'],
                'alamat': row['alamat']
            })
        else:
            return jsonify({'found': False})
