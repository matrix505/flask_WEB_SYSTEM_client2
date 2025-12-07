# email_helper.py - Email Sending Helper
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import EMAIL_CONFIG

def generate_otp():
    """Generate a 6-digit OTP"""
    return str(random.randint(100000, 999999))

def send_otp_email(to_email, otp_code):
    """Send OTP to user's email"""
    # # Print OTP to console for testing (remove in production)
    # print(f"\n{'='*50}")
    # print(f"OTP Code for {to_email}: {otp_code}")
    # print(f"{'='*50}\n")
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_CONFIG['email']
        msg['To'] = to_email
        msg['Subject'] = 'Your OTP Code - Flask Blog'
        
        body = f"""
        Hello!
        
        Your OTP code for registration is: {otp_code}
        
        This code will expire in 5 minutes.
        
        If you didn't request this code, please ignore this email.
        
        Best regards,
        Flask Blog Team
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Connect and send
        server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
        server.starttls()
        server.login(EMAIL_CONFIG['email'], EMAIL_CONFIG['password'])
        server.send_message(msg)
        server.quit()
        
        return True
    except Exception as e:
        print(f"Email Error: {e}")
        # For demo purposes, return True even if email fails
        # In production, you should handle this properly
        return False  # Change to False in production
