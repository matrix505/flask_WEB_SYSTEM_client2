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
    """User dashboard page"""
    if session.get('role') == 'admin':
        return redirect(url_for('admin.admin_dashboard'))
    user = models.get_user_by_id(session.get('user_id'))
    return render_template('user_dashboard.html', user=user)


@user_bp.route('/profile')
@login_required
def profile():
    """User profile page (view only)"""
    user = models.get_user_by_id(session.get('user_id'))
    return render_template('profile.html', user=user)

@user_bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Edit profile page"""
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
            return render_template('edit_profile.html', user=user)
        existing = models.get_user_by_email(email)
        if existing and existing['id'] != user['id']:
            flash('Email already used by another user!', 'error')
            return render_template('edit_profile.html', user=user)
        models.update_user(user['id'], firstname, middlename, lastname, birthday, contact, email)
        session['firstname'] = firstname
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('user.profile'))
    return render_template('edit_profile.html', user=user)

@user_bp.route('/games')
@login_required
def games():
    """Games page - only for verified users"""
    # Sample games data - replace with actual database query when games are implemented
    games_data = [
        {
            'id': 1,
            'title': 'Snake Game',
            'description': 'Classic snake game where you control a snake to eat food and grow longer.',
            'image': '/static/images/snake.jpg',
            'url': '/play/snake'
        },
        {
            'id': 2,
            'title': 'Tetris',
            'description': 'Arrange falling blocks to create complete lines and score points.',
            'image': '/static/images/tetris.jpg',
            'url': '/play/tetris'
        },
        {
            'id': 3,
            'title': 'Puzzle Quest',
            'description': 'Solve challenging puzzles and brain teasers to test your logic.',
            'image': '/static/images/puzzle.jpg',
            'url': '/play/puzzle'
        },
        {
            'id': 4,
            'title': 'Card Memory',
            'description': 'Match pairs of cards in this memory game to improve your concentration.',
            'image': '/static/images/memory.jpg',
            'url': '/play/memory'
        }
    ]
    return render_template('games.html', games=games_data)
