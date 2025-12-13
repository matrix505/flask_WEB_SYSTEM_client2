# Flask Web Application

A comprehensive Flask-based web application featuring user authentication, admin panel, mini-games, and email OTP verification system.

for the web documentation : https://github.com/matrix505/flask_WEB_SYSTEM_client2

## Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Database Schema](#database-schema)
- [Key Components](#key-components)
- [API Routes](#api-routes)
- [Games](#games)
- [Configuration](#configuration)
- [Usage](#usage)

## Features

### User Management
- User registration with email OTP verification
- Secure login/logout system
- User profile management
- Role-based access control (User/Admin)

### Admin Panel
- User management (view, edit, activate/deactivate, delete users)
- Site content management
- Admin dashboard with user statistics

### Games
- Tic-Tac-Toe
- Rock Paper Scissors
- Number Guessing Game
- Memory Match
- Simple Pong

### Security Features
- Password hashing with SHA-256
- Email OTP verification (5-minute expiry)
- Spam prevention (max 3 emails per hour)
- Session-based authentication
- SQL injection prevention with parameterized queries

### Additional Features
- Responsive web interface
- Email notifications
- Dynamic site content management
- Error handling (404 pages)

## Project Structure

```
flask_app2/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── database.py           # Database connection helpers
├── init_db_scheme.py     # Database initialization script
├── models.py             # Database models and operations
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
├── games/                # Mini-games directory
│   ├── memory_match.py
│   ├── number_guessing.py
│   ├── rock_paper_scissors.py
│   ├── simple_pong.py
│   └── tic_tac_toe.py
├── routes/               # Flask blueprints
│   ├── __init__.py
│   ├── admin.py
│   ├── auth.py
│   └── user.py
├── static/               # Static assets
│   ├── css/
│   │   └── style.css
│   └── games/
│       └── images/
├── templates/            # Jinja2 templates
│   ├── 404.html
│   ├── admin_*.html      # Admin panel templates
│   ├── base.html
│   ├── edit_profile.html
│   ├── games.html
│   ├── index.html
│   ├── login.html
│   ├── profile.html
│   ├── register.html
│   ├── user_*.html       # User panel templates
│   └── verify_otp.html
└── utils/                # Utility functions
    └── email_helper.py
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- MySQL Server
- Git

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd flask_app2
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   Create a `.env` file in the root directory:
   ```env
   db_host=localhost
   db_user=your_mysql_username
   db_password=your_mysql_password
   mail_email=your_email@gmail.com
   mail_password=your_app_password
   ```

5. **Database Setup**
   ```bash
   python init_db_scheme.py
   ```

6. **Run the Application**
   ```bash
   python app.py
   ```

   The application will be available at `http://localhost:5000`

## Database Schema

### Tables

#### users
- `id` (INT, PRIMARY KEY, AUTO_INCREMENT)
- `username` (VARCHAR(50), UNIQUE, NOT NULL)
- `password` (VARCHAR(255), NOT NULL) - SHA-256 hashed
- `email` (VARCHAR(100), UNIQUE, NOT NULL)
- `firstname` (VARCHAR(50), NOT NULL)
- `middlename` (VARCHAR(50))
- `lastname` (VARCHAR(50), NOT NULL)
- `birthday` (DATE, NOT NULL)
- `contact` (VARCHAR(20), NOT NULL)
- `role` (ENUM('user', 'admin'), DEFAULT 'user')
- `is_active` (TINYINT(1), DEFAULT 1)
- `created_at` (DATETIME, DEFAULT CURRENT_TIMESTAMP)

#### otp_codes
- `id` (INT, PRIMARY KEY, AUTO_INCREMENT)
- `email` (VARCHAR(100), NOT NULL)
- `otp_code` (VARCHAR(10), NOT NULL)
- `created_at` (DATETIME, DEFAULT CURRENT_TIMESTAMP)

#### email_log
- `id` (INT, PRIMARY KEY, AUTO_INCREMENT)
- `email` (VARCHAR(100), NOT NULL)
- `sent_at` (DATETIME, DEFAULT CURRENT_TIMESTAMP)

#### pending_registrations
- `id` (INT, PRIMARY KEY, AUTO_INCREMENT)
- `username` (VARCHAR(50), NOT NULL)
- `password` (VARCHAR(255), NOT NULL)
- `email` (VARCHAR(100), NOT NULL)
- `firstname` (VARCHAR(50), NOT NULL)
- `middlename` (VARCHAR(50))
- `lastname` (VARCHAR(50), NOT NULL)
- `birthday` (DATE, NOT NULL)
- `contact` (VARCHAR(20), NOT NULL)
- `created_at` (DATETIME, DEFAULT CURRENT_TIMESTAMP)

#### site_content
- `id` (INT, PRIMARY KEY, AUTO_INCREMENT)
- `content_key` (VARCHAR(50), UNIQUE, NOT NULL)
- `content_value` (TEXT)
- `updated_at` (DATETIME, DEFAULT CURRENT_TIMESTAMP ON UPDATE)

## Key Components

### Core Application (app.py)
- **Flask Application Setup**: Initializes Flask app with secret key
- **Blueprint Registration**: Registers authentication, user, and admin blueprints
- **Error Handling**: Custom 404 error handler
- **Development Server**: Runs on host 0.0.0.0, port 5000 with debug mode

### Database Layer (database.py)
- **`get_db_connection()`**: Establishes MySQL database connection
- **`execute_query(query, params, fetch)`**: Executes SQL queries with optional result fetching
- **`execute_one(query, params)`**: Executes query and returns single result

### Models (models.py)
#### User Operations
- **`create_user()`**: Creates new user with hashed password
- **`verify_login()`**: Authenticates user credentials
- **`get_user_by_*()`**: Various user retrieval functions
- **`update_user()`**: Updates user profile information
- **`admin_update_user()`**: Admin-level user updates

#### OTP Operations
- **`save_otp()`**: Stores OTP codes in database
- **`verify_otp()`**: Validates OTP with 5-minute expiry
- **`check_email_spam()`**: Prevents email spam (max 3 emails/hour)

#### Site Content
- **`get_site_content()`**: Retrieves all site content as dictionary
- **`update_site_content()`**: Updates site content values

### Authentication Routes (routes/auth.py)
- **`/` (index)**: Homepage with dynamic content
- **`/login`**: User login with session management
- **`/register`**: Multi-step registration with OTP
- **`/verify-otp`**: OTP verification endpoint
- **`/logout`**: Session cleanup and logout

### User Routes (routes/user.py)
- **`/dashboard`**: User dashboard
- **`/profile`**: User profile management
- **`/edit-profile`**: Profile editing interface
- **`/games`**: Games page access

### Admin Routes (routes/admin.py)
- **`/admin/dashboard`**: Admin dashboard with statistics
- **`/admin/users`**: User management interface
- **`/admin/edit-user/<id>`**: Individual user editing
- **`/admin/content`**: Site content management

### Email Utilities (utils/email_helper.py)
- **`generate_otp()`**: Generates 6-digit OTP codes
- **`send_otp_email()`**: Sends OTP via SMTP (Gmail)

## API Routes

### Authentication Endpoints
- `GET /` - Homepage
- `GET/POST /login` - User login
- `GET/POST /register` - User registration
- `GET/POST /verify-otp` - OTP verification
- `GET /logout` - User logout

### User Endpoints
- `GET /dashboard` - User dashboard
- `GET /profile` - View profile
- `GET/POST /edit-profile` - Edit profile
- `GET /games` - Access games

### Admin Endpoints
- `GET /admin/dashboard` - Admin dashboard
- `GET /admin/users` - User management
- `GET/POST /admin/edit-user/<id>` - Edit specific user
- `GET/POST /admin/content` - Manage site content
- `POST /admin/update-user-status` - Activate/deactivate users
- `POST /admin/delete-user` - Delete users

## Games

The application includes several mini-games implemented with Tkinter:

### Tic-Tac-Toe (tic_tac_toe.py)
- Two-player turn-based game
- Win condition checking
- Game reset functionality
- Visual feedback with colors

### Rock Paper Scissors (rock_paper_scissors.py)
- Single-player vs computer
- Random computer choice generation
- Score tracking
- Game statistics

### Number Guessing (number_guessing.py)
- Computer generates random number (1-100)
- User input validation
- Hint system (higher/lower)
- Attempt counting

### Memory Match (memory_match.py)
- Card matching game
- Grid-based layout
- Score and timer system
- Difficulty levels

### Simple Pong (simple_pong.py)
- Two-player paddle game
- Ball physics simulation
- Score tracking
- Keyboard controls

## Configuration

### Environment Variables (.env)
```env
# Database Configuration
db_host=localhost
db_user=your_mysql_username
db_password=your_mysql_password

# Email Configuration
mail_email=your_email@gmail.com
mail_password=your_app_password
```

### Application Settings (config.py)
- **SECRET_KEY**: Flask session secret key
- **DB_CONFIG**: MySQL database connection parameters
- **EMAIL_CONFIG**: SMTP email server settings
- **OTP_EXPIRY_MINUTES**: OTP validity duration (5 minutes)
- **Image_EXTENSIONS**: Allowed image file extensions

## Usage

### Default Accounts
After running `init_db_scheme.py`, the following accounts are created:

**Admin Account:**
- Username: `admin`
- Password: `admin123`
- Email: `admin@example.com`

**Test User Account:**
- Username: `testuser`
- Password: `user123`
- Email: `user@example.com`

### User Registration Flow
1. User fills registration form
2. System sends OTP to email
3. User enters OTP for verification
4. Account is activated upon successful OTP verification

### Admin Features
- View all users with their status
- Edit user information
- Activate/deactivate user accounts
- Delete users
- Update site content (title, tagline, about section)

### Games Access
- Available to logged-in users
- Each game runs in separate Tkinter window
- Independent of web interface

## Security Considerations

- Passwords are hashed using SHA-256
- OTP codes expire after 5 minutes
- Email spam prevention (3 emails max per hour)
- Parameterized SQL queries prevent injection
- Session-based authentication
- Role-based access control

## Dependencies

- **Flask 3.1.2**: Web framework
- **mysql-connector-python 9.5.0**: MySQL database connector
- **python-dotenv 1.2.1**: Environment variable management
- **pygame-ce 2.5.6**: Game development (for some games)

## Development Notes

- The application uses Flask blueprints for modular routing
- Database operations are abstracted through helper functions
- Email functionality uses Gmail SMTP (requires app password)
- Games are implemented as separate Python scripts using Tkinter
- Static files are served from the `static/` directory
- Templates use Jinja2 templating with base template inheritance

## Future Enhancements

- Password reset functionality
- User avatar uploads
- Game leaderboards
- Email templates
- API endpoints for mobile app integration
- User activity logging
- Advanced admin analytics</content>
<parameter name="filePath">c:\Users\ASUS\OneDrive\Documents\BASIC WORK\flask_app2\README.md
