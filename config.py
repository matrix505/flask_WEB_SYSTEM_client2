import os

SECRET_KEY = 'secret'

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # 
    'database': 'flask_blog_db'
}

# Email settings 
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'email': '',
    'password': ''
}

OTP_EXPIRY_MINUTES = 5

Image_EXTENSIONS = {'png', 'jpg', 'jpeg'}
