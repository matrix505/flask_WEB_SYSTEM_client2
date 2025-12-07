# routes/user.py - User Routes
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from functools import wraps
import models

user_bp = Blueprint('user', __name__)

# ============ DECORATORS ============

def login_required(f):
    """Decorator to check if user is logged in"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('loggedIn'):
            flash('Please login first!', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# ============ USER ROUTES ============

@user_bp.route('/dashboard')
@login_required
def user_dashboard():
    """User dashboard"""
    if session.get('role') == 'admin':
        return redirect(url_for('admin.admin_dashboard'))
    
    user = models.get_user_by_id(session.get('user_id'))
    return render_template('user_dashboard.html', user=user)

@user_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile page"""
    user = models.get_user_by_id(session.get('user_id'))
    
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        middlename = request.form.get('middlename', '')
        lastname = request.form.get('lastname')
        birthday = request.form.get('birthday')
        contact = request.form.get('contact')
        email = request.form.get('email')
        
        # Validation
        if not all([firstname, lastname, birthday, contact, email]):
            flash('Please fill all required fields!', 'error')
            return render_template('profile.html', user=user)
        
        # Check if email is taken by another user
        existing = models.get_user_by_email(email)
        if existing and existing['id'] != user['id']:
            flash('Email already used by another user!', 'error')
            return render_template('profile.html', user=user)
        
        # Update user
        models.update_user(user['id'], firstname, middlename, lastname, 
                          birthday, contact, email)
        
        # Update session
        session['firstname'] = firstname
        
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('user.profile'))
    
    return render_template('profile.html', user=user)

@user_bp.route('/games')
@login_required
def games():
    """Games page - only for verified users"""
    return render_template('games.html')
