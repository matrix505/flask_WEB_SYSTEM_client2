# routes/admin.py - Admin Routes
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from functools import wraps
import models
import os
import time
from config import Image_EXTENSIONS as ALLOWED_EXTENSIONS

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# ============ HELPER FUNCTIONS ============

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
            return redirect(url_for('user.user_dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# ============ ADMIN ROUTES ============

@admin_bp.route('/dashboard')
@admin_required
def admin_dashboard():
    """Admin dashboard"""
    users = models.get_all_users()
    user = models.get_user_by_id(session.get('user_id'))
    return render_template('admin_dashboard.html', users=users, user=user)

@admin_bp.route('/users')
@admin_required
def admin_users():
    """Admin users management"""
    users = models.get_all_users()
    return render_template('admin_users.html', users=users)

@admin_bp.route('/add-user', methods=['GET', 'POST'])
@admin_required
def admin_add_user():
    """Admin add new user"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        middlename = request.form.get('middlename', '')
        lastname = request.form.get('lastname')
        birthday = request.form.get('birthday')
        contact = request.form.get('contact')
        role = request.form.get('role', 'user')
        
        # Validation
        errors = []
        
        if not all([username, password, email, firstname, lastname, birthday, contact]):
            errors.append('Please fill all required fields!')
        
        if models.get_user_by_username(username):
            errors.append('Username already exists!')
        
        if models.get_user_by_email(email):
            errors.append('Email already registered!')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('admin_add_user.html')
        
        # Create user
        models.create_user(username, password, email, firstname, middlename, 
                          lastname, birthday, contact, role)
        
        flash('User created successfully!', 'success')
        return redirect(url_for('admin.admin_users'))
    
    return render_template('admin_add_user.html')

@admin_bp.route('/edit-user/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_user(user_id):
    """Admin edit user"""
    user = models.get_user_by_id(user_id)
    
    if not user:
        flash('User not found!', 'error')
        return redirect(url_for('admin.admin_users'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        middlename = request.form.get('middlename', '')
        lastname = request.form.get('lastname')
        birthday = request.form.get('birthday')
        contact = request.form.get('contact')
        role = request.form.get('role')
        
        # Validation
        errors = []
        
        if not all([username, email, firstname, lastname, birthday, contact]):
            errors.append('Please fill all required fields!')
        
        # Check username conflict
        existing = models.get_user_by_username(username)
        if existing and existing['id'] != user_id:
            errors.append('Username already exists!')
        
        # Check email conflict
        existing = models.get_user_by_email(email)
        if existing and existing['id'] != user_id:
            errors.append('Email already used!')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('admin_edit_user.html', user=user)
        
        
        models.admin_update_user(user_id, username, email, firstname, middlename, 
                                 lastname, birthday, contact, role)
        
        flash('User updated successfully!', 'success')
        return redirect(url_for('admin.admin_users'))
    
    return render_template('admin_edit_user.html', user=user)

@admin_bp.route('/delete-user/<int:user_id>')
@admin_required
def admin_delete_user(user_id):
    """Admin delete user"""
    # don't allow admin to delete themselves
    if user_id == session.get('user_id'):
        flash('You cannot delete yourself!', 'error')
        return redirect(url_for('admin.admin_users'))
    
    models.delete_user(user_id)
    flash('User deleted successfully!', 'success')
    return redirect(url_for('admin.admin_users'))


@admin_bp.route('/toggle-user/<int:user_id>')
@admin_required
def admin_toggle_user(user_id):
    """Admin activate/deactivate user"""
    if user_id == session.get('user_id'):
        flash('You cannot deactivate yourself!', 'error')
        return redirect(url_for('admin.admin_users'))
    
    user = models.get_user_by_id(user_id)
    if user:
        new_status = 0 if user['is_active'] == 1 else 1
        models.update_user_status(user_id, new_status)
        status_text = 'activated' if new_status == 1 else 'deactivated'
        flash(f'User {status_text} successfully!', 'success')
    
    return redirect(url_for('admin.admin_users'))

@admin_bp.route('/content', methods=['GET', 'POST'])
@admin_required
def admin_content():
    """Admin edit homepage content"""
    if request.method == 'POST':
        models.update_site_content('site_title', request.form.get('site_title', ''))
        models.update_site_content('tagline', request.form.get('tagline', ''))
        models.update_site_content('about_me', request.form.get('about_me', ''))
        models.update_site_content('dream_job_title', request.form.get('dream_job_title', ''))
        models.update_site_content('dream_job_text', request.form.get('dream_job_text', ''))
        
        flash('Homepage content updated successfully!', 'success')
        return redirect(url_for('admin.admin_content'))
    
    content = models.get_site_content()
    return render_template('admin_content.html', content=content, now=int(time.time()))

@admin_bp.route('/upload-profile', methods=['POST'])
@admin_required
def admin_upload_profile():
    """Admin upload profile image"""
    if 'profile_image' not in request.files:
        flash('No file selected!', 'error')
        return redirect(url_for('admin.admin_content'))
    
    file = request.files['profile_image']
    
    if file.filename == '':
        flash('No file selected!', 'error')
        return redirect(url_for('admin.admin_content'))
    
    if file and allowed_file(file.filename):
        upload_folder = os.path.join(current_app.root_path, 'static', 'images')
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        filepath = os.path.join(upload_folder, 'profile.png')
        file.save(filepath)
        
        flash('Profile image updated successfully!', 'success')
    else:
        flash('Invalid file type! Please use PNG, JPG, or JPEG.', 'error')
    
    return redirect(url_for('admin.admin_content'))
