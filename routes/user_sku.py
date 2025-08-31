# routes/user_sku.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime, date
from database import get_connection

user_sku_bp = Blueprint('user_sku', __name__, url_prefix='/sku')


def get_client_ip():
    """Ambil IP dari pengunjung, termasuk jika di balik proxy"""
    if request.headers.getlist("X-Forwarded-For"):
        return request.headers.getlist("X-Forwarded-For")[0]
    return request.remote_addr


# -------------------------------
# Halaman Form SKU untuk User
# -------------------------------
@user_sku_bp.route('/form', methods=['GET', 'POST'])
def form_sku():
    conn = get_connection()
    with conn.cursor() as cursor:
        ip = get_client_ip()
        today = date.today()

        # Log kunjungan harian
        cursor.execute("""
            SELECT COUNT(*) AS total FROM kunjungan
            WHERE ip_address=%s AND tanggal=%s
        """, (ip, today))
        exists = cursor.fetchone()['total']
        if not exists:
            cursor.execute("""
                INSERT INTO kunjungan (tanggal, ip_address, created_at)
                VALUES (%s, %s, NOW())
            """, (today, ip))
            conn.commit()

        cursor.execute("SELECT COUNT(*) AS total FROM kunjungan WHERE tanggal=%s", (today,))
        jumlah_kunjungan = cursor.fetchone()['total']

        if request.method == 'POST':
            # Data pemohon (autofill)
            nik = request.form['nik']
            nama = request.form['nama']
            tempat_lahir = request.form['tempat_lahir']
            tanggal_lahir = request.form['tanggal_lahir']
            pekerjaan = request.form['pekerjaan']
            alamat = request.form['alamat']

            # Data usaha (diinput user)
            nama_usaha = request.form['nama_usaha']
            tempat_usaha = request.form['tempat_usaha']
            dusun = request.form['dusun']

            pembuat = 'User'
            no_surat = f"SKU-{datetime.now().strftime('%Y%m%d%H%M%S')}"

            cursor.execute("""
                INSERT INTO sku
                (no_surat, nik, nama, tempat_lahir, tanggal_lahir, pekerjaan, alamat,
                 nama_usaha, tempat_usaha, dusun, status, pembuat_surat)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'pending',%s)
            """, (no_surat, nik, nama, tempat_lahir, tanggal_lahir, pekerjaan, alamat,
                  nama_usaha, tempat_usaha, dusun, pembuat))
            conn.commit()

            flash("Permohonan berhasil dikirim. Silakan tunggu konfirmasi dari kantor desa.", "success")
            return redirect(url_for('user_sku.form_sku'))

    conn.close()
    return render_template('user/sku_form.html', now=datetime.now, jumlah_kunjungan=jumlah_kunjungan)


# -------------------------------
# API: Ambil Data Otomatis dari KK & NIK
# -------------------------------
@user_sku_bp.route('/ambil-data')
def ambil_data_penduduk_sku():
    no_kk = request.args.get('no_kk')
    nik = request.args.get('nik')

    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT 
                p.nama,
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
                'tempat_lahir': row['tempat_lahir'],
                'tanggal_lahir': row['tanggal_lahir'].strftime('%Y-%m-%d') if row['tanggal_lahir'] else '',
                'pekerjaan': row['pekerjaan'],
                'alamat': row['alamat']
            })
        else:
            return jsonify({'found': False})
