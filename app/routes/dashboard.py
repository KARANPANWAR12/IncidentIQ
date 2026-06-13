from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app import mysql

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard')
@login_required
def index():
    cur = mysql.connection.cursor()

    # Aggregated stats
    cur.execute("SELECT COUNT(*) as total FROM tickets")
    total = cur.fetchone()['total']

    cur.execute("SELECT COUNT(*) as cnt FROM tickets WHERE status = 'Resolved'")
    resolved = cur.fetchone()['cnt']

    cur.execute("SELECT COUNT(*) as cnt FROM tickets WHERE status = 'Open'")
    open_count = cur.fetchone()['cnt']

    cur.execute("SELECT COUNT(*) as cnt FROM tickets WHERE status = 'In Progress'")
    in_progress = cur.fetchone()['cnt']

    cur.execute("SELECT COUNT(*) as cnt FROM tickets WHERE status = 'Escalated'")
    escalated = cur.fetchone()['cnt']

    cur.execute("SELECT COUNT(*) as cnt FROM tickets WHERE priority = 'High'")
    high = cur.fetchone()['cnt']

    cur.execute("SELECT COUNT(*) as cnt FROM tickets WHERE priority = 'Medium'")
    medium = cur.fetchone()['cnt']

    cur.execute("SELECT COUNT(*) as cnt FROM tickets WHERE priority = 'Low'")
    low = cur.fetchone()['cnt']

    # Recent tickets
    if current_user.role == 'admin':
        cur.execute("""
            SELECT t.*, u.username as raised_by_name 
            FROM tickets t 
            JOIN users u ON t.user_id = u.id 
            ORDER BY t.created_at DESC LIMIT 8
        """)
    else:
        cur.execute("""
            SELECT t.*, u.username as raised_by_name 
            FROM tickets t 
            JOIN users u ON t.user_id = u.id 
            WHERE t.user_id = %s
            ORDER BY t.created_at DESC LIMIT 8
        """, (current_user.id,))

    recent = cur.fetchall()
    cur.close()

    stats = {
        'total': total, 'resolved': resolved, 'open': open_count,
        'in_progress': in_progress, 'escalated': escalated,
        'high': high, 'medium': medium, 'low': low
    }

    return render_template('dashboard.html', stats=stats, recent=recent)