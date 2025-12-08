# routes/admin.py - Admin Routes
from flask import Blueprint, render_template, session, flash, redirect, url_for
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# ============ DECORATORS ============

def admin_required(f):
    """Decorator to check if user is admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('loggedIn'):
            flash('Please login first!', 'error')
            return redirect(url_for('auth.login'))
        if session.get('role') != 'admin':
            flash('Admin access required!', 'error')
            return redirect(url_for('auth.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@admin_required
def admin_dashboard():
    """Admin dashboard - empty for now"""
    return render_template('admin_dashboard.html')
