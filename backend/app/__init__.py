import os
from pathlib import Path
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

# Load .env from the backend/ directory regardless of where the server is started from
_BACKEND_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=_BACKEND_DIR / '.env')


def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_secret_key')
    app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')
    
    frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:5173')
    configured_origins = [origin.strip() for origin in frontend_url.split(',') if origin.strip()]
    allowed_origins = list(dict.fromkeys(configured_origins + [
        "https://fake-news-frontend-iiij.onrender.com",
        "http://localhost:5173", "http://127.0.0.1:5173",
        "http://localhost:5174", "http://127.0.0.1:5174"
    ]))
    CORS(app, resources={r"/api/*": {"origins": allowed_origins, "methods": ["GET", "POST", "OPTIONS"]}})

    # Initialize Database (graceful)
    from app.database.db import init_db
    init_db(app)

    # Register routes blueprint
    from app.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
