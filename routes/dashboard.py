from flask import Blueprint, render_template, session
from database import get_connection
from utils.security import login_required, role_required

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
@role_required('admin')  # Hanya admin yang boleh mengakses dashboard
def dashboard():
    conn = get_connection()
    
    with conn.cursor() as cursor:
        # Total penduduk
        cursor.execute("SELECT COUNT(*) AS total_penduduk FROM penduduk")
        total_penduduk = cursor.fetchone()['total_penduduk']

        # Total laki-laki
        cursor.execute("SELECT COUNT(*) AS total_laki FROM penduduk WHERE jenis_kelamin = 'L'")
        total_laki = cursor.fetchone()['total_laki']

        # Total perempuan
        cursor.execute("SELECT COUNT(*) AS total_perempuan FROM penduduk WHERE jenis_kelamin = 'P'")
        total_perempuan = cursor.fetchone()['total_perempuan']

        # Total kepala keluarga
        cursor.execute("SELECT COUNT(*) AS total_kk FROM kartu_keluarga")
        total_kk = cursor.fetchone()['total_kk']

        # Total berita
        cursor.execute("SELECT COUNT(*) AS total_berita FROM berita")
        total_berita = cursor.fetchone()['total_berita']

    # Render halaman dashboard
    return render_template(
        'dashboard.html',
        total_penduduk=total_penduduk,
        total_laki=total_laki,
        total_perempuan=total_perempuan,
        total_kk=total_kk,
        total_berita=total_berita,
        nama_user=session.get('nama', 'Pengguna'),
        level=session.get('level', 'User')
    )
