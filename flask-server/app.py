from flask import Flask
from flask_cors import CORS
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
    origins=["https://new-cs348-frontend.onrender.com", "http://localhost:3000"],
    allow_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
)

# Ensure instance folder exists
os.makedirs(os.path.join(app.root_path, 'instance'), exist_ok=True)

# Configuration settings
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
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
app.config['SESSION_COOKIE_NAME'] = 'dunder_mifflin_session'
app.config['SESSION_COOKIE_SECURE'] = False  # Set to False for localhost
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Changed to Lax for localhost
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour

# Bind the database to this app
db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return "Welcome to the Order Management System API!"

# Import and register routes
register_customer_routes(app)
register_order_routes(app)
register_report_routes(app)
app.register_blueprint(auth_bp, url_prefix='/auth')

if __name__ == "__main__":
    app.run()
