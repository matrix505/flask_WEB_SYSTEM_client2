# app.py - Main Flask Application
from flask import Flask, render_template 
from routes import register_blueprints
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

from config import SECRET_KEY
app.secret_key = SECRET_KEY

# Register all blueprints
register_blueprints(app)

# ============ ERROR HANDLERS ============

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# ============ RUN APP ============

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

