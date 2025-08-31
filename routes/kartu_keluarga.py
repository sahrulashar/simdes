from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database import get_connection
from utils.security import login_required, admin_required

kk_bp = Blueprint('kk', __name__)

# ------------------------
# TAMPILAN DATA KK
# ------------------------
@kk_bp.route('/kk')
@login_required
@admin_required
def index():
    keyword = request.args.get('q', '')

    conn = get_connection()
    with conn.cursor() as cursor:
        if keyword:
            sql = """
                SELECT * FROM kartu_keluarga
                WHERE no_kk LIKE %s OR dusun LIKE %s OR desa LIKE %s OR kecamatan LIKE %s
            """
            like = f"%{keyword}%"
            cursor.execute(sql, (like, like, like, like))
        else:
            cursor.execute("SELECT * FROM kartu_keluarga")
        data = cursor.fetchall()

    return render_template('kartu_keluarga/index.html', data=data, keyword=keyword)

# ------------------------
# TAMBAH DATA KK
# ------------------------
@kk_bp.route('/kk/tambah', methods=['GET', 'POST'])
@login_required
@admin_required
def tambah():
    if request.method == 'POST':
        no_kk = request.form.get('no_kk', '').strip()
        dusun = request.form.get('dusun', '').strip()
        rt = request.form.get('rt', '').strip()
        rw = request.form.get('rw', '').strip()
        desa = request.form.get('desa', '').strip()
        kecamatan = request.form.get('kecamatan', '').strip()
        kabupaten = request.form.get('kabupaten', '').strip()
        provinsi = request.form.get('provinsi', '').strip()

        if not no_kk:
            flash('Nomor KK tidak boleh kosong.', 'warning')
            return redirect(request.url)

        conn = get_connection()
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO kartu_keluarga (no_kk, dusun, rt, rw, desa, kecamatan, kabupaten, provinsi)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (no_kk, dusun, rt, rw, desa, kecamatan, kabupaten, provinsi))
            conn.commit()

        flash('Data KK berhasil ditambahkan', 'success')
        return redirect(url_for('kk.index'))

    return render_template('kartu_keluarga/tambah.html')

# ------------------------
# EDIT DATA KK
# ------------------------
@kk_bp.route('/kk/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit(id):
    conn = get_connection()
    with conn.cursor() as cursor:
        if request.method == 'POST':
            sql = """
                UPDATE kartu_keluarga SET no_kk=%s, dusun=%s, rt=%s, rw=%s, desa=%s,
                kecamatan=%s, kabupaten=%s, provinsi=%s WHERE id=%s
            """
            cursor.execute(sql, (
                request.form['no_kk'].strip(),
                request.form['dusun'].strip(),
                request.form['rt'].strip(),
                request.form['rw'].strip(),
                request.form['desa'].strip(),
                request.form['kecamatan'].strip(),
                request.form['kabupaten'].strip(),
                request.form['provinsi'].strip(),
                id
            ))
            conn.commit()
            flash('Data KK berhasil diubah', 'success')
            return redirect(url_for('kk.index'))
        else:
            cursor.execute("SELECT * FROM kartu_keluarga WHERE id=%s", (id,))
            data = cursor.fetchone()
            if not data:
                flash('Data tidak ditemukan.', 'danger')
                return redirect(url_for('kk.index'))
            return render_template('kartu_keluarga/tambah.html', data=data, edit=True)

# ------------------------
# HAPUS DATA KK
# ------------------------
@kk_bp.route('/kk/hapus/<int:id>')
@login_required
@admin_required
def hapus(id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM kartu_keluarga WHERE id=%s", (id,))
        conn.commit()
    flash('Data KK berhasil dihapus', 'danger')
    return redirect(url_for('kk.index'))
