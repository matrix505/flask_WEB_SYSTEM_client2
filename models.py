# models.py - User Model and Database Operations
from database import execute_query, execute_one
from datetime import datetime
import hashlib

def hash_password(password):
    """Simple password hashing"""
    return hashlib.sha256(password.encode()).hexdigest()

# ============ USER OPERATIONS ============

def create_user(username, password, email, firstname, middlename, lastname, 
                birthday, contact, role='user'):
    """Create a new user in the database"""
    hashed_pw = hash_password(password)
    query = """
        INSERT INTO users (username, password, email, firstname, middlename, 
                          lastname, birthday, contact, role, is_active, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 1, NOW())
    """
    params = (username, hashed_pw, email, firstname, middlename, lastname, 
              birthday, contact, role)
    return execute_query(query, params)

def get_user_by_username(username):
    """Get user by username"""
    query = "SELECT * FROM users WHERE username = %s"
    return execute_one(query, (username,))

def get_user_by_email(email):
    """Get user by email"""
    query = "SELECT * FROM users WHERE email = %s"
    return execute_one(query, (email,))

def get_user_by_id(user_id):
    """Get user by ID"""
    query = "SELECT * FROM users WHERE id = %s"
    return execute_one(query, (user_id,))

def verify_login(username, password):
    """Verify user login credentials"""
    user = get_user_by_username(username)
    if user and user['password'] == hash_password(password):
        if user['is_active'] == 1:
            return user
    return None

def get_admin_user():
    """Get the first admin user for homepage display"""
    query = "SELECT * FROM users WHERE role = 'admin' LIMIT 1"
    return execute_one(query)

def get_all_users():
    """Get all users from database"""
    query = "SELECT * FROM users ORDER BY id DESC"
    return execute_query(query, fetch=True)

def update_user(user_id, firstname, middlename, lastname, birthday, contact, email):
    """Update user profile information"""
    query = """
        UPDATE users SET firstname=%s, middlename=%s, lastname=%s, 
                        birthday=%s, contact=%s, email=%s
        WHERE id = %s
    """
    params = (firstname, middlename, lastname, birthday, contact, email, user_id)
    return execute_query(query, params)

def update_user_status(user_id, is_active):
    """Activate or deactivate a user"""
    query = "UPDATE users SET is_active = %s WHERE id = %s"
    return execute_query(query, (is_active, user_id))

def delete_user(user_id):
    """Delete a user from database"""
    query = "DELETE FROM users WHERE id = %s"
    return execute_query(query, (user_id,))

def admin_update_user(user_id, username, email, firstname, middlename, lastname, 
                      birthday, contact, role):
    """Admin update user with all fields"""
    query = """
        UPDATE users SET username=%s, email=%s, firstname=%s, middlename=%s, 
                        lastname=%s, birthday=%s, contact=%s, role=%s
        WHERE id = %s
    """
    params = (username, email, firstname, middlename, lastname, birthday, 
              contact, role, user_id)
    return execute_query(query, params)

# ============ OTP OPERATIONS ============

def save_otp(email, otp_code):
    """Save OTP to database"""
    # Delete old OTPs for this email first
    delete_query = "DELETE FROM otp_codes WHERE email = %s"
    execute_query(delete_query, (email,))
    
    # Insert new OTP
    query = "INSERT INTO otp_codes (email, otp_code, created_at) VALUES (%s, %s, NOW())"
    return execute_query(query, (email, otp_code))

def verify_otp(email, otp_code):
    """Verify OTP code"""
    query = """
        SELECT * FROM otp_codes 
        WHERE email = %s AND otp_code = %s 
        AND created_at > DATE_SUB(NOW(), INTERVAL 5 MINUTE)
    """
    result = execute_one(query, (email, otp_code))
    if result:
        # Delete used OTP
        delete_query = "DELETE FROM otp_codes WHERE email = %s"
        execute_query(delete_query, (email,))
        return True
    return False

def check_email_spam(email):
    """Check if too many OTPs sent recently (spam prevention)"""
    query = """
        SELECT COUNT(*) as count FROM email_log 
        WHERE email = %s AND sent_at > DATE_SUB(NOW(), INTERVAL 1 HOUR)
    """
    result = execute_one(query, (email,))
    if result and result['count'] >= 3:
        return True  # Too many emails sent
    return False

def log_email_sent(email):
    """Log email sent for spam prevention"""
    query = "INSERT INTO email_log (email, sent_at) VALUES (%s, NOW())"
    return execute_query(query, (email,))

# ============ PENDING REGISTRATION ============

def save_pending_registration(username, password, email, firstname, middlename, 
                              lastname, birthday, contact):
    """Save pending registration data"""
    # Delete old pending registration for this email
    delete_query = "DELETE FROM pending_registrations WHERE email = %s"
    execute_query(delete_query, (email,))
    
    hashed_pw = hash_password(password)
    query = """
        INSERT INTO pending_registrations 
        (username, password, email, firstname, middlename, lastname, birthday, contact, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
    """
    params = (username, hashed_pw, email, firstname, middlename, lastname, birthday, contact)
    return execute_query(query, params)

def get_pending_registration(email):
    """Get pending registration by email"""
    query = "SELECT * FROM pending_registrations WHERE email = %s"
    return execute_one(query, (email,))

def complete_registration(email):
    """Complete registration by moving from pending to users"""
    pending = get_pending_registration(email)
    if pending:
        query = """
            INSERT INTO users (username, password, email, firstname, middlename, 
                              lastname, birthday, contact, role, is_active, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'user', 1, NOW())
        """
        params = (pending['username'], pending['password'], pending['email'], 
                  pending['firstname'], pending['middlename'], pending['lastname'],
                  pending['birthday'], pending['contact'])
        result = execute_query(query, params)
        
        # Delete pending registration
        delete_query = "DELETE FROM pending_registrations WHERE email = %s"
        execute_query(delete_query, (email,))
        
        return result
    return None

# ============ SITE CONTENT OPERATIONS ============

def get_site_content():
    """Get all site content as dictionary"""
    query = "SELECT content_key, content_value FROM site_content"
    results = execute_query(query, fetch=True)
    content = {}
    if results:
        for row in results:
            content[row['content_key']] = row['content_value']
    return content

def update_site_content(content_key, content_value):
    """Update site content by key"""
    query = """
        INSERT INTO site_content (content_key, content_value) 
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE content_value = %s
    """
    return execute_query(query, (content_key, content_value, content_value))

# ============ GAME OPERATIONS ============

def get_all_games():
    """Get all games from database"""
    query = "SELECT * FROM games ORDER BY id"
    return execute_query(query, fetch=True)

def get_enabled_games():
    """Get only enabled games"""
    query = "SELECT * FROM games WHERE is_enabled = 1 ORDER BY id"
    return execute_query(query, fetch=True)

def get_game_by_id(game_id):
    """Get game by ID"""
    query = "SELECT * FROM games WHERE id = %s"
    return execute_one(query, (game_id,))

def get_game_by_name(game_name):
    """Get game by name"""
    query = "SELECT * FROM games WHERE name = %s"
    return execute_one(query, (game_name,))

def toggle_game_status(game_id):
    """Toggle game enabled/disabled status"""
    game = get_game_by_id(game_id)
    if game:
        new_status = 0 if game['is_enabled'] == 1 else 1
        query = "UPDATE games SET is_enabled = %s WHERE id = %s"
        execute_query(query, (new_status, game_id))
        return new_status
    return None
