from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import mysql
from app.ai_priority import predict_priority
from app.email_simulation import send_alert
import logging
from datetime import datetime

tickets = Blueprint('tickets', __name__)

@tickets.route('/tickets')
@login_required
def list_tickets():
    cur = mysql.connection.cursor()
    status_filter = request.args.get('status', '')
    priority_filter = request.args.get('priority', '')

    query = """
        SELECT t.*, u.username as raised_by_name 
        FROM tickets t JOIN users u ON t.user_id = u.id
        WHERE 1=1
    """
    params = []

    if current_user.role != 'admin':
        query += " AND t.user_id = %s"
        params.append(current_user.id)

    if status_filter:
        query += " AND t.status = %s"
        params.append(status_filter)

    if priority_filter:
        query += " AND t.priority = %s"
        params.append(priority_filter)

    query += " ORDER BY t.created_at DESC"
    cur.execute(query, params)
    all_tickets = cur.fetchall()
    cur.close()

    return render_template('tickets.html', tickets=all_tickets,
                           status_filter=status_filter, priority_filter=priority_filter)

@tickets.route('/tickets/new', methods=['GET', 'POST'])
@login_required
def new_ticket():
    ai_result = None

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        category = request.form.get('category', 'General')

        if not title or not description:
            flash('Title and description are required.', 'danger')
            return render_template('new_ticket.html')

        # AI Priority Prediction
        ai_result = predict_priority(title, description)
        priority = ai_result['priority']

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO tickets (title, description, priority, category, status, user_id, created_at)
            VALUES (%s, %s, %s, %s, 'Open', %s, %s)
        """, (title, description, priority, category, current_user.id, datetime.now()))
        mysql.connection.commit()
        ticket_id = cur.lastrowid

        # Audit log
        cur.execute("""
            INSERT INTO audit_logs (ticket_id, changed_by, old_status, new_status, note, changed_at)
            VALUES (%s, %s, NULL, 'Open', 'Ticket created', %s)
        """, (ticket_id, current_user.username, datetime.now()))
        mysql.connection.commit()
        cur.close()

        # Email simulation
        send_alert(title, priority, current_user.username, ticket_id)

        logging.info(f"TICKET CREATED | #{ticket_id} | {title} | Priority: {priority} | By: {current_user.username}")
        flash(f'Ticket #{ticket_id} raised! AI predicted priority: {priority}', 'success')
        return redirect(url_for('tickets.list_tickets'))

    return render_template('new_ticket.html', ai_result=ai_result)

@tickets.route('/tickets/<int:ticket_id>')
@login_required
def view_ticket(ticket_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT t.*, u.username as raised_by_name 
        FROM tickets t JOIN users u ON t.user_id = u.id 
        WHERE t.id = %s
    """, (ticket_id,))
    ticket = cur.fetchone()

    if not ticket:
        flash('Ticket not found.', 'danger')
        return redirect(url_for('tickets.list_tickets'))

    if current_user.role != 'admin' and ticket['user_id'] != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('tickets.list_tickets'))

    cur.execute("SELECT * FROM audit_logs WHERE ticket_id = %s ORDER BY changed_at DESC", (ticket_id,))
    logs = cur.fetchall()
    cur.close()

    return render_template('view_ticket.html', ticket=ticket, logs=logs)

@tickets.route('/tickets/<int:ticket_id>/update', methods=['POST'])
@login_required
def update_ticket(ticket_id):
    if current_user.role != 'admin':
        flash('Only admins can update ticket status.', 'danger')
        return redirect(url_for('tickets.view_ticket', ticket_id=ticket_id))

    new_status = request.form.get('status')
    note = request.form.get('note', '').strip() or 'Status updated'
    valid_statuses = ['Open', 'In Progress', 'Resolved', 'Escalated']

    if new_status not in valid_statuses:
        flash('Invalid status.', 'danger')
        return redirect(url_for('tickets.view_ticket', ticket_id=ticket_id))

    cur = mysql.connection.cursor()
    cur.execute("SELECT status FROM tickets WHERE id = %s", (ticket_id,))
    ticket = cur.fetchone()
    old_status = ticket['status']

    cur.execute("UPDATE tickets SET status = %s WHERE id = %s", (new_status, ticket_id))
    cur.execute("""
        INSERT INTO audit_logs (ticket_id, changed_by, old_status, new_status, note, changed_at)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (ticket_id, current_user.username, old_status, new_status, note, datetime.now()))
    mysql.connection.commit()
    cur.close()

    logging.info(f"STATUS UPDATE | Ticket #{ticket_id} | {old_status} → {new_status} | By: {current_user.username}")
    flash(f'Ticket #{ticket_id} updated to {new_status}.', 'success')
    return redirect(url_for('tickets.view_ticket', ticket_id=ticket_id))

@tickets.route('/tickets/predict', methods=['POST'])
@login_required
def predict():
    title = request.form.get('title', '')
    description = request.form.get('description', '')
    result = predict_priority(title, description)
    return {'priority': result['priority'], 'confidence': result['confidence']}