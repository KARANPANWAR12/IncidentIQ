"""Run this ONCE to create admin and employee accounts."""
from app import create_app, mysql, bcrypt

app = create_app()

with app.app_context():
    cur = mysql.connection.cursor()

    admin_pass = bcrypt.generate_password_hash('admin123').decode('utf-8')
    emp_pass = bcrypt.generate_password_hash('emp123').decode('utf-8')

    cur.execute("INSERT IGNORE INTO users (username, password, role) VALUES (%s, %s, 'admin')",
                ('admin', admin_pass))
    cur.execute("INSERT IGNORE INTO users (username, password, role) VALUES (%s, %s, 'employee')",
                ('employee', emp_pass))
    mysql.connection.commit()
    cur.close()
    print("✅ Users created: admin/admin123 and employee/emp123")