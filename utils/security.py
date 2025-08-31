from functools import wraps
from flask import session, redirect, url_for, flash

# --- LOGIN WAJIB ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Silakan login terlebih dahulu.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# --- KHUSUS UNTUK ROLE TERTENTU (admin, user, dll) ---
def role_required(required_role):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Silakan login terlebih dahulu.', 'warning')
                return redirect(url_for('auth.login'))

            current_role = session.get('level')
            if current_role != required_role:
                flash(f'Akses ditolak. Halaman ini hanya untuk pengguna dengan level {required_role}.', 'danger')
                return redirect(url_for('dashboard.dashboard'))

            return f(*args, **kwargs)
        return decorated_function
    return wrapper

# --- ALIAS UNTUK USER BIASA ---
user_required = role_required('user')
admin_required = role_required('admin')
