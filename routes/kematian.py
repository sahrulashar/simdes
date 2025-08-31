from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from database import get_connection
from datetime import datetime
from utils.security import login_required, admin_required

kematian_bp = Blueprint('kematian', __name__, url_prefix='/kematian')

# ----------------------------
# Generate nomor kematian otomatis
# ----------------------------
def generate_no_kematian():
    today_str = datetime.today().strftime('%Y%m%d')
    prefix = f"KM-{today_str}-"
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) AS jumlah FROM kematian WHERE DATE(created_at) = CURDATE()")
        result = cursor.fetchone()
        count = result['jumlah'] + 1 if result and result['jumlah'] else 1
    return f"{prefix}{str(count).zfill(3)}"

# ----------------------------
# Halaman utama (list data)
# ----------------------------
@kematian_bp.route('/')
@login_required
@admin_required
def index():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM kematian ORDER BY id DESC")
        data = cursor.fetchall()
    return render_template('kematian/index.html', data=data)

# ----------------------------
# Tambah data kematian
# ----------------------------
@kematian_bp.route('/tambah', methods=['GET', 'POST'])
@login_required
@admin_required
def tambah():
    conn = get_connection()
    if request.method == 'POST':
        no_kematian = generate_no_kematian()
        nik = request.form['nik'].strip()
        nama = request.form['nama'].strip()
        tanggal_lahir = request.form['tanggal_lahir']
        tanggal_meninggal = request.form['tanggal_meninggal']
        tempat_meninggal = request.form['tempat_meninggal']
        umur = request.form['umur']
        sebab = request.form['sebab']
        tempat_makam = request.form['tempat_makam']
        pelapor = request.form['pelapor']
        hubungan_pelapor = request.form['hubungan_pelapor']

        # Validasi wajib
        if not nik or not nama or not tanggal_meninggal:
            flash("NIK, Nama, dan Tanggal Meninggal wajib diisi.", "warning")
            return redirect(request.url)

        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO kematian
                (no_kematian, nik, nama, tanggal_lahir, tanggal_meninggal,
                 tempat_meninggal, umur, sebab, tempat_makam,
                 pelapor, hubungan_pelapor)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                no_kematian, nik, nama, tanggal_lahir, tanggal_meninggal,
                tempat_meninggal, umur, sebab, tempat_makam,
                pelapor, hubungan_pelapor
            ))
            conn.commit()
            flash("Data kematian berhasil ditambahkan", "success")
            return redirect(url_for('kematian.index'))

    return render_template('kematian/tambah.html')

# ----------------------------
# Autocomplete NIK dan nama
# ----------------------------
@kematian_bp.route('/cari-nik')
@login_required
def cari_nik():
    term = request.args.get('term', '')
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT nik, nama FROM penduduk
            WHERE nik LIKE %s OR nama LIKE %s
            LIMIT 10
        """, (f"%{term}%", f"%{term}%"))
        hasil = [f"{row['nik']} - {row['nama']}" for row in cursor.fetchall()]
    return jsonify(hasil)

# ----------------------------
# Ambil data penduduk berdasarkan NIK
# ----------------------------
@kematian_bp.route('/penduduk/<nik>')
@login_required
def get_penduduk(nik):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT nama, tanggal_lahir FROM penduduk WHERE nik = %s", (nik,))
        row = cursor.fetchone()
        if row:
            return jsonify({
                'nama': row['nama'],
                'tanggal_lahir': row['tanggal_lahir'].strftime('%Y-%m-%d') if row['tanggal_lahir'] else ''
            })
    return jsonify({})

# ----------------------------
# Detail data kematian
# ----------------------------
@kematian_bp.route('/detail/<int:id>')
@login_required
@admin_required
def detail(id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM kematian WHERE id = %s", (id,))
        data = cursor.fetchone()

    if not data:
        flash("Data tidak ditemukan", "danger")
        return redirect(url_for('kematian.index'))

    umur = ''
    if data['tanggal_lahir'] and data['tanggal_meninggal']:
        try:
            lahir = data['tanggal_lahir']
            meninggal = data['tanggal_meninggal']
            umur = meninggal.year - lahir.year - ((meninggal.month, meninggal.day) < (lahir.month, lahir.day))
        except Exception:
            umur = ''

    data['umur_otomatis'] = umur
    return render_template('kematian/detail.html', data=data)

# ----------------------------
# Edit data kematian
# ----------------------------
@kematian_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit(id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM kematian WHERE id = %s", (id,))
        data = cursor.fetchone()

        if not data:
            flash("Data tidak ditemukan", "danger")
            return redirect(url_for('kematian.index'))

    if request.method == 'POST':
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE kematian
                    SET nik=%s, nama=%s, tanggal_lahir=%s, tanggal_meninggal=%s,
                        tempat_meninggal=%s, umur=%s, sebab=%s, tempat_makam=%s,
                        pelapor=%s, hubungan_pelapor=%s
                    WHERE id=%s
                """, (
                    request.form['nik'],
                    request.form['nama'],
                    request.form['tanggal_lahir'],
                    request.form['tanggal_meninggal'],
                    request.form['tempat_meninggal'],
                    request.form['umur'],
                    request.form['sebab'],
                    request.form['tempat_makam'],
                    request.form['pelapor'],
                    request.form['hubungan_pelapor'],
                    id
                ))
                conn.commit()
                flash("Data kematian berhasil diperbarui", "success")
                return redirect(url_for('kematian.index'))
        except Exception as e:
            conn.rollback()
            flash(f"Gagal memperbarui data: {e}", "danger")

    return render_template('kematian/tambah.html', data=data, edit=True)

# ----------------------------
# Hapus data kematian
# ----------------------------
@kematian_bp.route('/hapus/<int:id>')
@login_required
@admin_required
def hapus(id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM kematian WHERE id = %s", (id,))
            conn.commit()
            flash("Data kematian berhasil dihapus", "danger")
    except Exception as e:
        conn.rollback()
        flash(f"Gagal menghapus data: {e}", "danger")
    return redirect(url_for('kematian.index'))
