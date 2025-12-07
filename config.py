# config.py - Database and App Configuration
import os

# Flask App Configuration
SECRET_KEY = 'secret'

# Database Configuration for XAMPP MySQL
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # 
    'database': 'flask_blog_db'
}

# Email Configuration (use your own email settings)
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'email': 'matthewsuarez40@gmail.com',
    'password': 'izfhgluxowcgundp'
}

# OTP Settings
OTP_EXPIRY_MINUTES = 5

Image_EXTENSIONS = {'png', 'jpg', 'jpeg'}
