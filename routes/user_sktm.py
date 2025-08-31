from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime, date
from database import get_connection

user_sktm_bp = Blueprint('user_sktm', __name__, url_prefix='/sktm')


def get_client_ip():
    """Ambil IP dari pengunjung, termasuk jika di balik proxy"""
    if request.headers.getlist("X-Forwarded-For"):
        return request.headers.getlist("X-Forwarded-For")[0]
    return request.remote_addr


# -------------------------------
# Halaman Form SKTM untuk User
# -------------------------------
@user_sktm_bp.route('/form', methods=['GET', 'POST'])
def form_sktm():
    conn = get_connection()
    with conn.cursor() as cursor:
        ip = get_client_ip()
        today = date.today()

        # Hitung kunjungan harian
        cursor.execute("""
            SELECT COUNT(*) AS total 
            FROM kunjungan 
            WHERE ip_address=%s AND tanggal=%s
        """, (ip, today))
        row = cursor.fetchone()
        exists = row['total']

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

        # Form submission
        if request.method == 'POST':
            no_kk = request.form['no_kk']
            nik = request.form['nik']
            nama = request.form['nama']
            alamat = request.form['alamat']
            keperluan = request.form['keperluan']
            pembuat = 'User'
            no_surat = f"SKTM-{datetime.now().strftime('%Y%m%d%H%M%S')}"

            cursor.execute("""
                INSERT INTO sktm (
                    no_surat, no_kk, nik, nama, alamat, keperluan, status, pembuat_surat
                )
                VALUES (%s, %s, %s, %s, %s, %s, 'pending', %s)
            """, (no_surat, no_kk, nik, nama, alamat, keperluan, pembuat))
            conn.commit()

            flash("Permohonan berhasil dikirim. Silakan ambil surat di kantor desa.", "success")
            return redirect(url_for('user_sktm.form_sktm'))

    conn.close()
    return render_template('user/sktm_form.html', now=datetime.now, jumlah_kunjungan=jumlah_kunjungan)


# -------------------------------
# API: Ambil Data Otomatis dari KK & NIK
# -------------------------------
@user_sktm_bp.route('/ambil-data')
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
                'jenis_kelamin': 'Laki-Laki' if row['jenis_kelamin'] == 'L' else 'Perempuan',
                'tempat_lahir': row['tempat_lahir'],
                'tanggal_lahir': row['tanggal_lahir'].strftime('%Y-%m-%d') if row['tanggal_lahir'] else '',
                'alamat': row['alamat']
            })
        else:
            return jsonify({'found': False})
