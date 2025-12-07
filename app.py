# app.py - Main Flask Application
from flask import Flask, render_template
from config import SECRET_KEY
from routes import register_blueprints

app = Flask(__name__)
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

