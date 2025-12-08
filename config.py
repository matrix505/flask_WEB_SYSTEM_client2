import os

SECRET_KEY = 'secret'

DB_CONFIG = {
    'host': os.getenv('db_host'),
    'user': os.getenv('db_user'),
    'password': os.getenv('db_password'),  # 
    'database': 'flask_blog_db'
}

# Email settings 
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'email': os.getenv('mail_email'),
    'password': os.getenv('mail_password')
}

OTP_EXPIRY_MINUTES = 5

Image_EXTENSIONS = {'png', 'jpg', 'jpeg'}
