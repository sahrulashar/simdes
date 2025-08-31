from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database import get_connection
from datetime import datetime
from utils.security import login_required, admin_required

kelahiran_bp = Blueprint('kelahiran', __name__, url_prefix='/kelahiran')

# ----------------------------
# Generate Nomor Kelahiran Otomatis
# ----------------------------
def generate_no_kelahiran():
    today_str = datetime.today().strftime('%Y%m%d')
    prefix = f"KLH-{today_str}-"
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) AS jumlah FROM kelahiran WHERE DATE(tanggal_lahir) = CURDATE()")
        row = cursor.fetchone()
        count = row['jumlah'] + 1
    return f"{prefix}{str(count).zfill(3)}"

# ----------------------------
# Tampilkan Data Kelahiran
# ----------------------------
@kelahiran_bp.route('/')
@login_required
@admin_required
def index():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM kelahiran ORDER BY id DESC")
        data = cursor.fetchall()
    return render_template('kelahiran/index.html', data=data)

# ----------------------------
# Tambah Data Kelahiran
# ----------------------------
@kelahiran_bp.route('/tambah', methods=['GET', 'POST'])
@login_required
@admin_required
def tambah():
    conn = get_connection()
    if request.method == 'POST':
        no_kelahiran = generate_no_kelahiran()
        nama = request.form.get('nama', '').strip()
        tempat_lahir = request.form.get('tempat_lahir', '').strip()
        tanggal_lahir = request.form.get('tanggal_lahir', '').strip()
        berat = request.form.get('berat', '').strip()
        jenis_kelamin = request.form.get('jenis_kelamin', '')
        nama_ayah = request.form.get('nama_ayah', '').strip()
        nama_ibu = request.form.get('nama_ibu', '').strip()
        alamat = request.form.get('alamat', '').strip()
        pelapor = request.form.get('pelapor', '').strip()

        if not nama or not tanggal_lahir or not jenis_kelamin:
            flash('Nama, Tanggal Lahir, dan Jenis Kelamin wajib diisi.', 'warning')
            return redirect(request.url)

        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO kelahiran
                    (no_kelahiran, nama, tempat_lahir, tanggal_lahir, berat,
                     jenis_kelamin, nama_ayah, nama_ibu, alamat, pelapor)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (no_kelahiran, nama, tempat_lahir, tanggal_lahir, berat,
                      jenis_kelamin, nama_ayah, nama_ibu, alamat, pelapor))
                conn.commit()
                flash('Data kelahiran berhasil ditambahkan', 'success')
                return redirect(url_for('kelahiran.index'))
        except Exception as e:
            conn.rollback()
            flash(f'Gagal menambahkan data: {e}', 'danger')

    return render_template('kelahiran/tambah.html', edit=False)

# ----------------------------
# Edit Data Kelahiran
# ----------------------------
@kelahiran_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit(id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM kelahiran WHERE id = %s", (id,))
        data = cursor.fetchone()
        if not data:
            flash("Data tidak ditemukan", "danger")
            return redirect(url_for('kelahiran.index'))

    if request.method == 'POST':
        nama = request.form['nama']
        tempat_lahir = request.form['tempat_lahir']
        tanggal_lahir = request.form['tanggal_lahir']
        berat = request.form['berat']
        jenis_kelamin = request.form['jenis_kelamin']
        nama_ayah = request.form['nama_ayah']
        nama_ibu = request.form['nama_ibu']
        alamat = request.form['alamat']
        pelapor = request.form['pelapor']

        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE kelahiran SET
                    nama=%s, tempat_lahir=%s, tanggal_lahir=%s, berat=%s,
                    jenis_kelamin=%s, nama_ayah=%s, nama_ibu=%s, alamat=%s, pelapor=%s
                    WHERE id = %s
                """, (nama, tempat_lahir, tanggal_lahir, berat, jenis_kelamin,
                      nama_ayah, nama_ibu, alamat, pelapor, id))
                conn.commit()
                flash('Data kelahiran berhasil diperbarui', 'success')
                return redirect(url_for('kelahiran.index'))
        except Exception as e:
            conn.rollback()
            flash(f'Gagal memperbarui data: {e}', 'danger')

    return render_template('kelahiran/tambah.html', data=data, edit=True)

# ----------------------------
# Detail Data Kelahiran
# ----------------------------
@kelahiran_bp.route('/detail/<int:id>')
@login_required
@admin_required
def detail(id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM kelahiran WHERE id = %s", (id,))
        data = cursor.fetchone()
    if not data:
        flash("Data tidak ditemukan", "danger")
        return redirect(url_for('kelahiran.index'))
    return render_template('kelahiran/detail.html', data=data)

# ----------------------------
# Hapus Data Kelahiran
# ----------------------------
@kelahiran_bp.route('/hapus/<int:id>')
@login_required
@admin_required
def hapus(id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM kelahiran WHERE id = %s", (id,))
            conn.commit()
            flash('Data berhasil dihapus', 'danger')
    except:
        conn.rollback()
        flash('Gagal menghapus data', 'danger')
    return redirect(url_for('kelahiran.index'))
