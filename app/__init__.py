from flask import Flask
from flask_mysqldb import MySQL
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import logging
import os
from dotenv import load_dotenv

load_dotenv()

mysql = MySQL()
login_manager = LoginManager()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv(
        'SECRET_KEY',
        'incident_secret_key_2024'
    )

    app.config['MYSQL_HOST'] = os.getenv(
        'MYSQLHOST',
        'localhost'
    )

    app.config['MYSQL_USER'] = os.getenv(
        'MYSQLUSER',
        'root'
    )

    app.config['MYSQL_PASSWORD'] = os.getenv(
        'MYSQLPASSWORD',
        ''
    )

    app.config['MYSQL_DB'] = os.getenv(
        'MYSQLDATABASE',
        'railway'
    )

    app.config['MYSQL_PORT'] = int(
        os.getenv(
            'MYSQLPORT',
            3306
        )
    )

    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

    mysql.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'warning'

    os.makedirs('logs', exist_ok=True)

    logging.basicConfig(
        filename='logs/audit.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    from app.routes.auth import auth
    from app.routes.tickets import tickets
    from app.routes.dashboard import dashboard

    app.register_blueprint(auth)
    app.register_blueprint(tickets)
    app.register_blueprint(dashboard)

    return app