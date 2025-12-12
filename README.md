# Flask Web App with Games

A simple Flask web application with user authentication and a collection of Tkinter-based games.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. **Clone the repository** (if applicable) or navigate to the project directory:
   ```
   cd flask_app2
   ```

2. **Create a virtual environment** (recommended):
   ```
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

5. **Set up the database**:
   ```
   python init_db_scheme.py
   ```
   This will create the necessary database tables.

## Running the Application

1. **Start the Flask app**:
   ```
   python app.py
   ```

2. **Open your web browser** and go to:
   ```
   http://127.0.0.1:5000
   ```

## Usage

- **Register/Login**: Create an account or log in to access the dashboard and games.
- **Games**: Navigate to the Games section to view and play available games.
  - Games are launched as separate Tkinter windows on your desktop.
  - Available games: Tic-Tac-Toe, Rock Paper Scissors, Number Guessing, Simple Pong, Memory Match.

## Features

- User authentication (register, login, logout)
- User dashboard
- Profile management
- Games section with 5 unique Tkinter games
- Responsive design

## Project Structure

- `app.py`: Main Flask application
- `routes/`: Blueprint routes for different sections
- `models.py`: Database models
- `database.py`: Database connection utilities
- `games/`: Tkinter game files
- `templates/`: HTML templates
- `static/`: CSS, JS, and other static files
- `utils/`: Utility functions (e.g., email helper)

## Notes

- The games are desktop applications that open in separate windows when launched from the web interface.
- Ensure your system allows running Python scripts and Tkinter applications.
- For development, the app runs in debug mode by default.

## Troubleshooting

- If games don't launch, check that Python is in your PATH and Tkinter is installed.
- For database issues, try re-running `python init_db_scheme.py`.
- Ensure port 5000 is not in use by other applications.