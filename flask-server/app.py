from flask import Flask
from flask_cors import CORS
from flask_session import Session
from models import db  # Import the db object from models.py
from routes.auth import auth_bp
from routes.customer import register_customer_routes
from routes.order import register_order_routes
from routes.report import register_report_routes
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app, 
    supports_credentials=True,
    origins=["https://cs348-backend-a1eh.onrender.com", "http://localhost:3000"],
    allow_headers=["Content-Type"],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
)

# Ensure instance folder exists
os.makedirs(os.path.join(app.root_path, 'instance'), exist_ok=True)

# Configuration settings
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(app.root_path, "instance", "dunder_mifflin.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'connect_args': {
        'timeout': 30,  # Set connection timeout
        'check_same_thread': False,  # Allow multiple threads
        'isolation_level': 'IMMEDIATE'  # SQLite isolation level
    }
}
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = os.path.join(app.root_path, 'instance', 'flask_session')
app.config['SESSION_FILE_THRESHOLD'] = 100
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'None'

# Initialize extensions
db.init_app(app)
Session(app)
