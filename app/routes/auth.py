from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import mysql, bcrypt
from app.models import User
import logging

auth = Blueprint('auth', __name__)

# BOTH routes must accept GET and POST
@auth.route('/', methods=['GET', 'POST'])
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not username or not password:
            flash('Please fill in all fields.', 'danger')
            return render_template('login.html')

        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM users WHERE username = %s",
            (username,)
        )
        user = cur.fetchone()
        cur.close()

        if user and bcrypt.check_password_hash(
            user['password'],
            password
        ):
            user_obj = User(
                user['id'],
                user['username'],
                user['role']
            )

            login_user(user_obj)

            logging.info(
                f"LOGIN | User: {username} | Role: {user['role']}"
            )

            flash(f"Welcome back, {username}!", 'success')

            return redirect(url_for('dashboard.index'))

        flash('Invalid username or password.', 'danger')
        logging.warning(
            f"FAILED LOGIN | Username: {username}"
        )

    return render_template('login.html')


@auth.route('/logout')
@login_required
def logout():
    logging.info(
        f"LOGOUT | User: {current_user.username}"
    )

    logout_user()
    flash('You have been logged out.', 'info')

    return redirect(url_for('auth.login'))