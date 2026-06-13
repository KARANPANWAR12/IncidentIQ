"""
Email Notification Simulation Module
Simulates enterprise alerting system.
Interview talking point: 'This is abstracted so we can plug in 
SendGrid, SES, or internal SMTP without changing business logic.'
"""

import logging

def send_alert(ticket_title: str, priority: str, raised_by: str, ticket_id: int):
    if priority == 'High':
        msg = (
            f"\n{'='*60}\n"
            f"  ⚠️  HIGH PRIORITY ALERT — TICKET #{ticket_id}\n"
            f"{'='*60}\n"
            f"  To      : it-ops-team@company.com, manager@company.com\n"
            f"  Subject : [URGENT] {ticket_title}\n"
            f"  Raised  : {raised_by}\n"
            f"  Priority: {priority}\n"
            f"  Action  : Immediate escalation required.\n"
            f"{'='*60}\n"
        )
        print(msg)
        logging.warning(f"EMAIL ALERT SENT | Ticket #{ticket_id} | {ticket_title} | By: {raised_by}")
    elif priority == 'Medium':
        print(f"[EMAIL] Medium priority ticket #{ticket_id} notification sent to support team.")
        logging.info(f"Email notification | Ticket #{ticket_id} | Medium priority")