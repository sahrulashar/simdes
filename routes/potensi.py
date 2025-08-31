from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database import get_connection
from datetime import date
import os
from werkzeug.utils import secure_filename
import pymysql
from utils.security import login_required, admin_required

potensi_bp = Blueprint('potensi', __name__)

UPLOAD_FOLDER = 'static/uploads/potensi'


@potensi_bp.route('/potensi')
@login_required
@admin_required
def potensi_index():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM potensi_desa ORDER BY tanggal DESC")
        data = cursor.fetchall()
    return render_template('potensi/index.html', potensi_list=data)


@potensi_bp.route('/potensi/tambah', methods=['GET', 'POST'])
@login_required
@admin_required
def potensi_tambah():
    if request.method == 'POST':
        judul = request.form['judul']
        tanggal = request.form['tanggal']
        penulis = request.form['penulis']
        sub_judul_list = request.form.getlist('sub_judul[]')
        deskripsi_list = request.form.getlist('deskripsi[]')

        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO potensi_desa (judul, tanggal, penulis) VALUES (%s, %s, %s)", (judul, tanggal, penulis))
            potensi_id = cursor.lastrowid

            for i, (sub_judul, deskripsi) in enumerate(zip(sub_judul_list, deskripsi_list)):
                cursor.execute("INSERT INTO sub_potensi (potensi_id, sub_judul, deskripsi) VALUES (%s, %s, %s)", (potensi_id, sub_judul, deskripsi))
                sub_id = cursor.lastrowid

                for file in request.files.getlist(f'gambar_{i}[]'):
                    if file and file.filename:
                        filename = secure_filename(file.filename)
                        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                        filepath = os.path.join(UPLOAD_FOLDER, filename)
                        file.save(filepath)

                        cursor.execute("INSERT INTO gambar_subpotensi (sub_potensi_id, file_gambar) VALUES (%s, %s)", (sub_id, filename))

            conn.commit()
            flash('Potensi berhasil ditambahkan', 'success')
        return redirect(url_for('potensi.potensi_index'))

    return render_template('potensi/tambah.html')


@potensi_bp.route('/potensi/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def potensi_edit(id):
    conn = get_connection()
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        if request.method == 'POST':
            judul = request.form['judul']
            tanggal = request.form['tanggal']
            penulis = request.form['penulis']

            cursor.execute("UPDATE potensi_desa SET judul=%s, tanggal=%s, penulis=%s WHERE id=%s", (judul, tanggal, penulis, id))

            # Hapus sub dan gambar lama
            cursor.execute("SELECT id FROM sub_potensi WHERE potensi_id = %s", (id,))
            sub_ids = [row['id'] for row in cursor.fetchall()]
            if sub_ids:
                cursor.execute("DELETE FROM gambar_subpotensi WHERE sub_potensi_id IN %s", (sub_ids,))
                cursor.execute("DELETE FROM sub_potensi WHERE potensi_id = %s", (id,))

            sub_judul_list = request.form.getlist('sub_judul[]')
            deskripsi_list = request.form.getlist('deskripsi[]')

            for i, (sub_judul, deskripsi) in enumerate(zip(sub_judul_list, deskripsi_list)):
                cursor.execute("INSERT INTO sub_potensi (potensi_id, sub_judul, deskripsi) VALUES (%s, %s, %s)", (id, sub_judul, deskripsi))
                sub_id = cursor.lastrowid

                for file in request.files.getlist(f'gambar_{i}[]'):
                    if file and file.filename:
                        filename = secure_filename(file.filename)
                        filepath = os.path.join(UPLOAD_FOLDER, filename)
                        file.save(filepath)
                        cursor.execute("INSERT INTO gambar_subpotensi (sub_potensi_id, file_gambar) VALUES (%s, %s)", (sub_id, filename))

            conn.commit()
            flash('Potensi berhasil diperbarui', 'success')
            return redirect(url_for('potensi.potensi_index'))

        cursor.execute("SELECT * FROM potensi_desa WHERE id=%s", (id,))
        data = cursor.fetchone()
        if not data:
            flash('Data tidak ditemukan', 'danger')
            return redirect(url_for('potensi.potensi_index'))

        cursor.execute("""
            SELECT sp.id, sp.sub_judul, sp.deskripsi,
                   (SELECT GROUP_CONCAT(file_gambar) 
                    FROM gambar_subpotensi 
                    WHERE sub_potensi_id = sp.id) AS gambar_list
            FROM sub_potensi sp
            WHERE sp.potensi_id = %s
        """, (id,))
        sub_potensi = cursor.fetchall()

    return render_template('potensi/edit.html', potensi=data, sub_potensi=sub_potensi)


@potensi_bp.route('/potensi/hapus/<int:id>', methods=['POST'])
@login_required
@admin_required
def potensi_hapus(id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM potensi_desa WHERE id=%s", (id,))
        conn.commit()
        flash('Potensi berhasil dihapus', 'success')
    return redirect(url_for('potensi.potensi_index'))


@potensi_bp.route('/potensi/detail/<int:id>')
@login_required
@admin_required
def potensi_detail_admin(id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM potensi_desa WHERE id = %s", (id,))
        potensi = cursor.fetchone()

        if not potensi:
            flash('Data potensi tidak ditemukan', 'danger')
            return redirect(url_for('potensi.potensi_index'))

        cursor.execute("SELECT * FROM sub_potensi WHERE potensi_id = %s", (id,))
        sub_potensi = cursor.fetchall()

        for sub in sub_potensi:
            cursor.execute("SELECT file_gambar FROM gambar_subpotensi WHERE sub_potensi_id = %s", (sub['id'],))
            gambar = cursor.fetchall()
            sub['gambar_list'] = ",".join([g['file_gambar'] for g in gambar]) if gambar else ""

    return render_template('potensi/detail.html', potensi=potensi, sub_potensi=sub_potensi)
