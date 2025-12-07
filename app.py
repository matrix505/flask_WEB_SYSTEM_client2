# app.py - Main Flask Application
from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
import models
import os
import time
from email_helper import generate_otp, send_otp_email
from config import SECRET_KEY,ALLOWED_EXTENSIONS

app = Flask(__name__)
app.secret_key = SECRET_KEY



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ============ DECORATORS ============

def login_required(f):
    """Decorator to check if user is logged in"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('loggedIn'):
            flash('Please login first!', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to check if user is admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('loggedIn'):
            flash('Please login first!', 'error')
            return redirect(url_for('login'))
        if session.get('role') != 'admin':
            flash('Admin access required!', 'error')
            return redirect(url_for('user_dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# ============ PUBLIC ROUTES ============

@app.route('/')
def index():
    """Homepage"""
    user = None
    if session.get('loggedIn'):
        user = models.get_user_by_id(session.get('user_id'))
    content = models.get_site_content()
    admin = models.get_admin_user()
    return render_template('index.html', user=user, content=content, admin=admin)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if session.get('loggedIn'):
        if session.get('role') == 'admin':
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('user_dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Validate input
        if not username or not password:
            flash('Please fill all fields!', 'error')
            return render_template('login.html')
        
        # Verify credentials
        user = models.verify_login(username, password)
        
        if user:
            # Set session variables
            session['loggedIn'] = True
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['firstname'] = user['firstname']
            session['role'] = user['role']
            
            flash(f'Welcome back, {user["firstname"]}!', 'success')
            
            # Redirect based on role
            if user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid username or password, or account is deactivated!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    flash('You have been logged out!', 'success')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page"""
    if session.get('loggedIn'):
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        middlename = request.form.get('middlename', '')
        lastname = request.form.get('lastname')
        birthday = request.form.get('birthday')
        contact = request.form.get('contact')
        
        # Validation
        errors = []
        
        if not all([username, password, email, firstname, lastname, birthday, contact]):
            errors.append('Please fill all required fields!')
        
        if password != confirm_password:
            errors.append('Passwords do not match!')
        
        if len(password) < 6:
            errors.append('Password must be at least 6 characters!')
        
        if models.get_user_by_username(username):
            errors.append('Username already exists!')
        
        if models.get_user_by_email(email):
            errors.append('Email already registered!')
        
        # Check for spam
        if models.check_email_spam(email):
            errors.append('Too many OTP requests. Please try again later.')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('register.html')
        
        # Save pending registration
        models.save_pending_registration(username, password, email, firstname, 
                                         middlename, lastname, birthday, contact)
        
        # Generate and save OTP
        otp = generate_otp()
        models.save_otp(email, otp)
        models.log_email_sent(email)
        
        # Send OTP email
        send_otp_email(email, otp)
        
        # Store email in session for verification
        session['pending_email'] = email
        
        flash('OTP has been sent to your email!', 'success')
        return redirect(url_for('verify_otp'))
    
    return render_template('register.html')

@app.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    """OTP verification page"""
    if not session.get('pending_email'):
        flash('Please register first!', 'error')
        return redirect(url_for('register'))
    
    if request.method == 'POST':
        otp_code = request.form.get('otp')
        email = session.get('pending_email')
        
        if models.verify_otp(email, otp_code):
            # Complete registration
            models.complete_registration(email)
            session.pop('pending_email', None)
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Invalid or expired OTP!', 'error')
    
    return render_template('verify_otp.html', email=session.get('pending_email'))

@app.route('/resend-otp')
def resend_otp():
    """Resend OTP"""
    email = session.get('pending_email')
    if not email:
        flash('Please register first!', 'error')
        return redirect(url_for('register'))
    
    # Check spam
    if models.check_email_spam(email):
        flash('Too many OTP requests. Please try again later.', 'error')
        return redirect(url_for('verify_otp'))
    
    # Generate new OTP
    otp = generate_otp()
    models.save_otp(email, otp)
    models.log_email_sent(email)
    send_otp_email(email, otp)
    
    flash('New OTP has been sent!', 'success')
    return redirect(url_for('verify_otp'))

# ============ USER ROUTES ============

@app.route('/dashboard')
@login_required
def user_dashboard():
    """User dashboard"""
    if session.get('role') == 'admin':
        return redirect(url_for('admin_dashboard'))
    
    user = models.get_user_by_id(session.get('user_id'))
    return render_template('user_dashboard.html', user=user)

@app.route('/profile', methods=['GET', 'POST'])
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
        return redirect(url_for('profile'))
    
    return render_template('profile.html', user=user)

@app.route('/games')
@login_required
def games():
    """Games page - only for verified users"""
    return render_template('games.html')

# ============ ADMIN ROUTES ============

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    """Admin dashboard"""
    users = models.get_all_users()
    user = models.get_user_by_id(session.get('user_id'))
    return render_template('admin_dashboard.html', users=users, user=user)

@app.route('/admin/users')
@admin_required
def admin_users():
    """Admin users management"""
    users = models.get_all_users()
    return render_template('admin_users.html', users=users)

@app.route('/admin/add-user', methods=['GET', 'POST'])
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
        return redirect(url_for('admin_users'))
    
    return render_template('admin_add_user.html')

@app.route('/admin/edit-user/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_user(user_id):
    """Admin edit user"""
    user = models.get_user_by_id(user_id)
    
    if not user:
        flash('User not found!', 'error')
        return redirect(url_for('admin_users'))
    
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
        return redirect(url_for('admin_users'))
    
    return render_template('admin_edit_user.html', user=user)

@app.route('/admin/delete-user/<int:user_id>')
@admin_required
def admin_delete_user(user_id):
    """Admin delete user"""
    # don't allow admin to delete themselves
    if user_id == session.get('user_id'):
        flash('You cannot delete yourself!', 'error')
        return redirect(url_for('admin_users'))
    
    models.delete_user(user_id)
    flash('User deleted successfully!', 'success')
    return redirect(url_for('admin_users'))


@app.route('/admin/toggle-user/<int:user_id>')
@admin_required
def admin_toggle_user(user_id):
    """Admin activate/deactivate user"""
    if user_id == session.get('user_id'):
        flash('You cannot deactivate yourself!', 'error')
        return redirect(url_for('admin_users'))
    
    user = models.get_user_by_id(user_id)
    if user:
        new_status = 0 if user['is_active'] == 1 else 1
        models.update_user_status(user_id, new_status)
        status_text = 'activated' if new_status == 1 else 'deactivated'
        flash(f'User {status_text} successfully!', 'success')
    
    return redirect(url_for('admin_users'))

@app.route('/admin/content', methods=['GET', 'POST'])
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
        return redirect(url_for('admin_content'))
    
    content = models.get_site_content()
    return render_template('admin_content.html', content=content, now=int(time.time()))

@app.route('/admin/upload-profile', methods=['POST'])
@admin_required
def admin_upload_profile():
    """Admin upload profile image"""
    if 'profile_image' not in request.files:
        flash('No file selected!', 'error')
        return redirect(url_for('admin_content'))
    
    file = request.files['profile_image']
    
    if file.filename == '':
        flash('No file selected!', 'error')
        return redirect(url_for('admin_content'))
    
    if file and allowed_file(file.filename):
        upload_folder = os.path.join(app.root_path, 'static', 'images')
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        filepath = os.path.join(upload_folder, 'profile.png')
        file.save(filepath)
        
        flash('Profile image updated successfully!', 'success')
    else:
        flash('Invalid file type! Please use PNG, JPG, or JPEG.', 'error')
    
    return redirect(url_for('admin_content'))

# error page

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# ============ RUN APP ============

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
