from flask import Flask
from flask_cors import CORS
from flask-server.routes.auth import auth_bp
from flask-server.routes.customer import register_customer_routes
from flask-server.routes.order import register_order_routes
from flask-server.routes.report import register_report_routes
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app, supports_credentials=True)

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
app.config['SECRET_KEY'] = 'your-secret-key-here'

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
