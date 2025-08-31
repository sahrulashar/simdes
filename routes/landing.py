from flask import Blueprint, render_template, request
from datetime import date
from database import get_connection
from datetime import datetime

landing_bp = Blueprint('landing', __name__)

def get_client_ip():
    """Ambil IP dari pengunjung, termasuk jika di balik proxy"""
    if request.headers.getlist("X-Forwarded-For"):
        return request.headers.getlist("X-Forwarded-For")[0]
    return request.remote_addr

@landing_bp.route('/')
def index():
    conn = get_connection()
    with conn.cursor() as cursor:
        
        # Cek kunjungan harian berdasarkan IP
        ip = get_client_ip()
        today = date.today()

        cursor.execute("SELECT COUNT(*) AS total FROM kunjungan WHERE ip_address=%s AND tanggal=%s", (ip, today))
        row = cursor.fetchone()
        exists = row['total']

        if not exists:
            cursor.execute("INSERT INTO kunjungan (tanggal, ip_address, created_at) VALUES (%s, %s, NOW())", (today, ip))
            conn.commit()

        cursor.execute("SELECT COUNT(*) AS total FROM kunjungan WHERE tanggal = %s", (today,))
        jumlah_kunjungan = cursor.fetchone()['total']

        # Ambil data aparat desa
        cursor.execute("SELECT nama, jabatan, foto, kontak FROM aparat_desa ORDER BY created_at ASC")
        aparat = cursor.fetchall()

        # Ambil galeri terbaru (maks 8)
        cursor.execute("SELECT gambar FROM galeri ORDER BY created_at DESC LIMIT 8")
        galeri = cursor.fetchall()

        # Ambil berita terbaru (maks 3)
        cursor.execute("SELECT * FROM berita ORDER BY id DESC LIMIT 3")
        berita_terbaru = cursor.fetchall()

        # --- Statistik Administrasi Penduduk ---
        cursor.execute("SELECT COUNT(*) AS total FROM penduduk")
        total_penduduk = cursor.fetchone()['total']

        cursor.execute("SELECT COUNT(*) AS total FROM kartu_keluarga")
        total_kk = cursor.fetchone()['total']

        cursor.execute("SELECT COUNT(*) AS total FROM penduduk WHERE jenis_kelamin = 'L'")
        total_laki = cursor.fetchone()['total']

        cursor.execute("SELECT COUNT(*) AS total FROM penduduk WHERE jenis_kelamin = 'P'")
        total_perempuan = cursor.fetchone()['total']

        cursor.execute("SELECT COUNT(*) AS total FROM pendatang")
        total_sementara = cursor.fetchone()['total']

        cursor.execute("SELECT COUNT(*) AS total FROM kepindahan")
        total_mutasi = cursor.fetchone()['total']

        cursor.execute("SELECT * FROM potensi_desa ORDER BY tanggal DESC LIMIT 2")
        potensi_list = cursor.fetchall()

        for potensi in potensi_list:
            cursor.execute("""
                SELECT sp.id, sp.sub_judul,
                       (SELECT file_gambar FROM gambar_subpotensi 
                        WHERE sub_potensi_id = sp.id LIMIT 1) AS gambar
                FROM sub_potensi sp
                WHERE sp.potensi_id = %s
                LIMIT 1
            """, (potensi['id'],))
            sub = cursor.fetchone()
            if sub:
                potensi['sub_judul'] = sub['sub_judul']
                potensi['gambar'] = sub['gambar']
            else:
                potensi['sub_judul'] = ''
                potensi['gambar'] = ''

    conn.close()
    return render_template(
        'index.html',
        aparat=aparat,
        galeri=galeri,
        jumlah_kunjungan=jumlah_kunjungan,
        berita_terbaru=berita_terbaru,
        total_penduduk=total_penduduk,
        total_kk=total_kk,
        total_laki=total_laki,
        total_perempuan=total_perempuan,
        total_sementara=total_sementara,
        total_mutasi=total_mutasi,
        potensi_list=potensi_list,
        now=datetime.now
    )

@landing_bp.route('/berita/<slug>')
def detail_berita_user(slug):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM berita WHERE slug = %s", (slug,))
        berita = cursor.fetchone()
    conn.close()

    if not berita:
        return render_template("404.html"), 404  # atau redirect ke index jika kamu belum punya 404.html

    return render_template('user/berita_detail.html', berita=berita,now=datetime.now)

@landing_bp.route('/profil-desa')
def profil_desa():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT nama, jabatan, foto, kontak FROM aparat_desa ORDER BY created_at ASC")
        aparat = cursor.fetchall()

        ip = get_client_ip()
        today = date.today()

        cursor.execute("SELECT COUNT(*) AS total FROM kunjungan WHERE ip_address=%s AND tanggal=%s", (ip, today))
        row = cursor.fetchone()
        exists = row['total']

        if not exists:
            cursor.execute("INSERT INTO kunjungan (tanggal, ip_address, created_at) VALUES (%s, %s, NOW())", (today, ip))
            conn.commit()
        # Ambil berita terbaru (maks 3)

        cursor.execute("SELECT COUNT(*) AS total FROM kunjungan WHERE tanggal = %s", (today,))
        jumlah_kunjungan = cursor.fetchone()['total']
        
        cursor.execute("SELECT * FROM berita ORDER BY id DESC LIMIT 3")
        berita_terbaru = cursor.fetchall()
    return render_template('user/profil_desa.html',now=datetime.now, aparat=aparat, berita_terbaru=berita_terbaru, jumlah_kunjungan=jumlah_kunjungan)

@landing_bp.route('/potensi-desa')
def potensi_desa_user():
    conn = get_connection()
    with conn.cursor() as cursor:
        ip = get_client_ip()
        today = date.today()

        cursor.execute("SELECT COUNT(*) AS total FROM kunjungan WHERE ip_address=%s AND tanggal=%s", (ip, today))
        row = cursor.fetchone()
        exists = row['total']

        if not exists:
            cursor.execute("INSERT INTO kunjungan (tanggal, ip_address, created_at) VALUES (%s, %s, NOW())", (today, ip))
            conn.commit()
        # Ambil berita terbaru (maks 3)

        cursor.execute("SELECT COUNT(*) AS total FROM kunjungan WHERE tanggal = %s", (today,))
        jumlah_kunjungan = cursor.fetchone()['total'] 

        cursor.execute("SELECT * FROM potensi_desa ORDER BY tanggal DESC")
        potensi_list = cursor.fetchall()

        for potensi in potensi_list:
            cursor.execute("""
                SELECT sp.id, sp.sub_judul,
                       (SELECT file_gambar FROM gambar_subpotensi 
                        WHERE sub_potensi_id = sp.id LIMIT 1) AS gambar
                FROM sub_potensi sp
                WHERE sp.potensi_id = %s
                LIMIT 1
            """, (potensi['id'],))
            sub = cursor.fetchone()
            if sub:
                potensi['sub_judul'] = sub['sub_judul']
                potensi['gambar'] = sub['gambar']
            else:
                potensi['sub_judul'] = ''
                potensi['gambar'] = ''
    conn.close()
    return render_template('user/potensi_desa.html', now=datetime.now, potensi_list=potensi_list, jumlah_kunjungan=jumlah_kunjungan)

@landing_bp.route('/potensi/<int:id>')
def potensi_detail(id):
    conn = get_connection()
    with conn.cursor() as cursor:
        ip = get_client_ip()
        today = date.today()

        cursor.execute("SELECT COUNT(*) AS total FROM kunjungan WHERE ip_address=%s AND tanggal=%s", (ip, today))
        row = cursor.fetchone()
        exists = row['total']

        if not exists:
            cursor.execute("INSERT INTO kunjungan (tanggal, ip_address, created_at) VALUES (%s, %s, NOW())", (today, ip))
            conn.commit()
        # Ambil berita terbaru (maks 3)

        cursor.execute("SELECT COUNT(*) AS total FROM kunjungan WHERE tanggal = %s", (today,))
        jumlah_kunjungan = cursor.fetchone()['total'] 

        cursor.execute("SELECT * FROM potensi_desa WHERE id = %s", (id,))
        potensi = cursor.fetchone()

        if not potensi:
            return render_template("404.html"), 404

        cursor.execute("""
            SELECT sp.id, sp.sub_judul, sp.deskripsi,
                   (SELECT file_gambar FROM gambar_subpotensi 
                    WHERE sub_potensi_id = sp.id LIMIT 1) AS file_gambar
            FROM sub_potensi sp
            WHERE sp.potensi_id = %s
        """, (id,))
        subpotensi_list = cursor.fetchall()

    conn.close()
    return render_template(
        'user/potensi_detail.html',
        potensi=potensi,
        subpotensi_list=subpotensi_list,
        now=datetime.now,
        jumlah_kunjungan=jumlah_kunjungan
    )
@landing_bp.route('/berita')
def user_berita_list():
    conn = get_connection()
    with conn.cursor() as cursor:
        ip = get_client_ip()
        today = date.today()

        cursor.execute("SELECT COUNT(*) AS total FROM kunjungan WHERE ip_address=%s AND tanggal=%s", (ip, today))
        row = cursor.fetchone()
        exists = row['total']

        if not exists:
            cursor.execute("INSERT INTO kunjungan (tanggal, ip_address, created_at) VALUES (%s, %s, NOW())", (today, ip))
            conn.commit()
        # Ambil berita terbaru (maks 3)

        cursor.execute("SELECT COUNT(*) AS total FROM kunjungan WHERE tanggal = %s", (today,))
        jumlah_kunjungan = cursor.fetchone()['total'] 
        cursor.execute("SELECT * FROM berita ORDER BY created_at DESC")
        berita_list = cursor.fetchall()
        
    conn.close()
    return render_template('user/berita.html', berita_list=berita_list, now=datetime.now, jumlah_kunjungan=jumlah_kunjungan)

@landing_bp.route('/galeri')
def galeri_user():
    conn = get_connection()
    with conn.cursor() as cursor:
        ip = get_client_ip()
        today = date.today()

        # Cek kunjungan harian
        cursor.execute("SELECT COUNT(*) AS total FROM kunjungan WHERE ip_address=%s AND tanggal=%s", (ip, today))
        row = cursor.fetchone()
        exists = row['total']

        if not exists:
            cursor.execute("INSERT INTO kunjungan (tanggal, ip_address, created_at) VALUES (%s, %s, NOW())", (today, ip))
            conn.commit()

        # Total kunjungan hari ini
        cursor.execute("SELECT COUNT(*) AS total FROM kunjungan WHERE tanggal = %s", (today,))
        jumlah_kunjungan = cursor.fetchone()['total']

        # Ambil 12 galeri terbaru
        cursor.execute("SELECT * FROM galeri ORDER BY created_at DESC LIMIT 12")
        galeri = cursor.fetchall()

    conn.close()
    return render_template(
        'user/galeri.html',
        galeri=galeri,
        jumlah_kunjungan=jumlah_kunjungan,
        now=datetime.now
    )
