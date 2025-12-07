
# Flask Personal Website System

This is a simple personal website and blog system built with Python Flask. It supports user registration, login, admin management, profile editing, and a games page. The project is designed for beginners and 2nd year college students.

---

## 🚀 Features

- User registration and login (with OTP email verification)
- Two roles: Admin and User
- Admin dashboard for managing users and homepage content
- User dashboard for personal info and games
- Profile editing and image upload
- Responsive design (works on mobile and desktop)
- Modern magenta & black theme

---

## 🖥️ Requirements

- Python 3.8 or higher
- XAMPP (for MySQL database)
- Web browser (Chrome, Firefox, Edge, etc.)
- Code editor (VS Code recommended)

---

## 📝 Setup Instructions

### 1. Install XAMPP

1. Download XAMPP from [apachefriends.org](https://www.apachefriends.org/)
2. Install and open XAMPP Control Panel
3. Start **Apache** and **MySQL**

### 2. Get the Project Files

Download or clone the repository:

```bash
git clone https://github.com/matrix505/flask_WEB_SYSTEM_client2.git
```
Or download the ZIP and extract it.

### 3. Install Python Libraries

Open a terminal in the project folder and run:

```bash
pip install -r requirements.txt
# or
python -m pip install -r requirements.txt
```

This installs Flask, mysql-connector-python, and other needed packages.

### 4. Setup the Database

Run the setup script to create the database and tables:

```bash
python setup_database.py
```

This will:
- Create the database `flask_blog_db`
- Add all tables and default accounts

### 5. Start the Website

```bash
python app.py
```

### 6. Open in Your Browser

Go to: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 👤 Default Accounts

| Role  | Username  | Password  |
|-------|-----------|-----------|
| Admin | admin     | admin123  |
| User  | testuser  | user123   |

---

## 📁 Project Structure

```
flask_app2/
├── app.py                # Main Flask app
├── config.py             # Settings (database, email)
├── database.py           # Database helper
├── models.py             # Database operations
├── email_helper.py       # Email/OTP functions
├── setup_database.py     # Database setup script
├── requirements.txt      # Python dependencies
├── README.md             # This file
│
├── static/
│   ├── css/
│   │   └── style.css     # Stylesheet
│   └── images/
│       └── profile.png   # Profile image
│
└── templates/
    ├── base.html
    ├── index.html
    ├── login.html
    ├── register.html
    ├── verify_otp.html
    ├── user_dashboard.html
    ├── profile.html
    ├── games.html
    ├── admin_dashboard.html
    ├── admin_users.html
    ├── admin_add_user.html
    ├── admin_edit_user.html
    ├── admin_content.html
    └── 404.html
```

---

## ⚙️ Configuration

### Database Settings

Edit `config.py` if you want to change database details:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',           # XAMPP default is empty
    'database': 'flask_blog_db'
}
```

### Email Settings (for OTP)

To send OTP codes by email, update `config.py`:

```python
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'email': 'your_email@gmail.com', # 
    'password': 'your_app_password'   # Use Gmail App Password
}
```

**How to get a Gmail App Password:**
1. Go to your Google Account > Security
2. Turn on 2-Step Verification
3. Go to App Passwords and generate one

**Tip:** If you don't set up email, the OTP code will show in the terminal during registration.

---

## 🛠️ Troubleshooting

| Problem                | Solution                                  |
|------------------------|-------------------------------------------|
| MySQL connection error | Make sure XAMPP MySQL is running          |
| Module not found       | Run `pip install -r requirements.txt`     |
| Port already in use    | Change port in `app.py` or close other apps|
| Email not sending      | Check EMAIL_CONFIG in `config.py`         |

---

## 🧑‍💻 Technologies Used

- Python Flask (backend)
- MySQL (database, via XAMPP)
- HTML, CSS, Jinja2 (frontend)
- Font Awesome 6 (icons)
- SHA256 password hashing, session management

---

## 👨‍🎓 Author

Created by a 2nd Year Computer Science Student  
December 2025
