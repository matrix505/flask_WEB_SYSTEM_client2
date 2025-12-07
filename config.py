
import os

# Flask App Configuration
SECRET_KEY = 'secret'


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

OTP_EXPIRY_MINUTES = 5

Image_EXTENSIONS = {'png', 'jpg', 'jpeg'}
