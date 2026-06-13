from flask import Flask
from flask_mysqldb import MySQL
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

mysql = MySQL()
login_manager = LoginManager()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)

    # --------------------------
    # App Configuration
    # --------------------------
    app.config['SECRET_KEY'] = os.environ.get(
        'SECRET_KEY',
        'incident_secret_key_2024'
    )

    app.config['MYSQL_HOST'] = os.environ.get(
        'MYSQLHOST',
        'localhost'
    )

    app.config['MYSQL_USER'] = os.environ.get(
        'MYSQLUSER',
        'root'
    )

    app.config['MYSQL_PASSWORD'] = os.environ.get(
        'MYSQLPASSWORD',
        ''
    )

    app.config['MYSQL_DB'] = os.environ.get(
        'MYSQLDATABASE',
        'railway'
    )

    app.config['MYSQL_PORT'] = int(
        os.environ.get('MYSQLPORT', 3306)
    )

    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

    # --------------------------
    # Initialize Extensions
    # --------------------------
    mysql.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'warning'

    # --------------------------
    # Test Railway MySQL Connection
    # --------------------------
    with app.app_context():
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT 1")
            result = cur.fetchone()
            print("✅ Railway MySQL Connected!", result)
            cur.close()
        except Exception as e:
            print("❌ Database Error:", e)

    # --------------------------
    # Logging Setup
    # --------------------------
    log_dir = 'logs'

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logging.basicConfig(
        filename=os.path.join(log_dir, 'audit.log'),
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # --------------------------
    # Register Blueprints
    # --------------------------
    from app.routes.auth import auth
    from app.routes.tickets import tickets
    from app.routes.dashboard import dashboard

    app.register_blueprint(auth)
    app.register_blueprint(tickets)
    app.register_blueprint(dashboard)

    return app