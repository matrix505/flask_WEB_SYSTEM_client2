# routes/user.py - User Routes
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from functools import wraps
import models
import subprocess

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
    # For now, no recent game data - can be implemented later
    recent_game = None
    return render_template('user_dashboard.html', user=user, recent_game=recent_game)


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
    games_data = models.get_enabled_games()
    return render_template('games.html', games=games_data)

@user_bp.route('/play/<game>')
@login_required
def play_game(game):
    """Launch the selected game"""
    game_obj = models.get_game_by_id(game)  # Assuming game is id, but wait, it's name
    # Actually, the url is /play/tic_tac_toe, so game is the name
    # Need to get game by name
    # Add function to get by name
    # For now, check if enabled by finding the game
    games = models.get_enabled_games()
    game_names = [g['name'] for g in games]
    if game in game_names:
        game_files = {
            'tic_tac_toe': 'tic_tac_toe.py',
            'rock_paper_scissors': 'rock_paper_scissors.py',
            'number_guessing': 'number_guessing.py',
            'simple_pong': 'simple_pong.py',
            'memory_match': 'memory_match.py'
        }
        if game in game_files:
            subprocess.Popen(['python', f'games/{game_files[game]}'])
            flash(f'Launching {game.replace("_", " ").title()}...', 'success')
        else:
            flash('Game not found!', 'error')
    else:
        flash('Game is currently disabled!', 'error')
    return redirect(url_for('user.games'))
