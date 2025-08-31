from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database import get_connection

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nik = request.form['nik']
        password = request.form['password']

        conn = get_connection()
        with conn.cursor() as cursor:
            sql = "SELECT * FROM users WHERE nik=%s AND password=%s"
            cursor.execute(sql, (nik, password))
            user = cursor.fetchone()

        if user:
            session['user_id'] = user['id']
            session['nama'] = user['nama']
            session['level'] = user['level']
            return redirect(url_for('dashboard.dashboard'))
        else:
            flash('Login gagal. Periksa NIK dan password.', 'danger')
            return redirect(url_for('auth.login'))

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
