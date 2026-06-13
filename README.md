# IncidentIQ — AI-Powered Incident Management System

A full-stack enterprise-grade incident management platform built with Flask and MySQL. Features secure role-based authentication, AI-driven ticket priority prediction, real-time analytics dashboard, audit logging, and complete ticket lifecycle management.

> Built as a portfolio project demonstrating full-stack Python development, database design, role-based access control, and AI integration.

---

## Live Demo

| Service | URL |
|---------|-----|
| Live App | _[Add your Render URL after deployment]_ |
| Database | Railway MySQL (managed) |

**Demo Credentials:**

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |
| Employee | `employee` | `emp123` |

---

## Features

**Authentication & Access Control**
- Secure login with bcrypt password hashing
- Role-based access: Admin vs Employee views
- Session management with Flask-Login

**Ticket Management**
- Raise tickets with title, description, and category
- AI automatically predicts priority (High / Medium / Low) from description text
- Full ticket lifecycle: Open → In Progress → Escalated → Resolved
- Employees see only their own tickets; Admins see all

**AI Priority Prediction**
- Keyword-based NLP engine analyzes ticket text
- Returns predicted priority + confidence percentage
- Designed to be swappable with a trained ML classifier
- Live preview before submitting a ticket

**Dashboard & Analytics**
- Real-time stats: Open, In Progress, Resolved ticket counts
- Recent tickets overview
- Filterable ticket list by status and priority

**Audit Logging**
- Every status change is logged with timestamp, actor, old status, new status, and note
- Full audit trail viewable per ticket

---

## Tech Stack

| Layer | Technology | Why |
|-------|------------|-----|
| Backend | Python + Flask | Lightweight, fast development; strong ecosystem |
| Auth | Flask-Login + Flask-Bcrypt | Industry-standard session management and password hashing |
| Database | MySQL | Relational data with foreign key constraints suits ticket/user/log relationships |
| ORM Layer | Flask-MySQLdb | Direct SQL with DictCursor for clean query results |
| Frontend | HTML + Jinja2 + CSS + JavaScript | Server-rendered templates; no frontend build step needed |
| Deployment | Render (app) + Railway (MySQL) | Both have free tiers; Railway MySQL is the easiest managed MySQL option |

---

## How to Run Locally

> Requires: Python 3.10+, MySQL 8.0+

### 1. Clone the repository

```bash
git clone https://github.com/KARANPANWAR12/IncidentIQ.git
cd IncidentIQ
```

### 2. Create virtual environment and install dependencies

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

pip install -r requirements.txt
```

### 3. Set up MySQL database

Open MySQL and run:

```bash
mysql -u root -p < database_setup.sql
```

This creates the `incident_db` database with `users`, `tickets`, and `audit_logs` tables.

### 4. Configure environment variables

```bash
copy .env.example .env       # Windows
# cp .env.example .env       # Mac/Linux
```

Edit `.env`:

```
SECRET_KEY=any_random_string_here
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DB=incident_db
```

### 5. Seed the database with users

```bash
python seed_users.py
```

This creates: `admin / admin123` and `employee / emp123`

### 6. Run the application

```bash
python run.py
```

Open `http://localhost:5000` in your browser.

---

## Project Structure

```
IncidentIQ/
├── run.py                        ← Entry point — starts Flask app
├── seed_users.py                 ← One-time script to create admin + employee accounts
├── database_setup.sql            ← SQL to create all tables
├── requirements.txt              ← Python dependencies
├── Procfile                      ← Render deployment start command
├── render.yaml                   ← Render deployment configuration
├── .env.example                  ← Template for environment variables
├── .gitignore
│
├── app/
│   ├── __init__.py               ← App factory — config, extensions, blueprints
│   ├── models.py                 ← User model for Flask-Login
│   ├── ai_priority.py            ← AI keyword-based priority prediction engine
│   ├── email_simulation.py       ← Simulated email alert on ticket creation
│   │
│   ├── routes/
│   │   ├── auth.py               ← Login, logout routes
│   │   ├── tickets.py            ← Raise, view, list, update tickets + AI predict endpoint
│   │   └── dashboard.py          ← Dashboard stats and recent tickets
│   │
│   ├── templates/
│   │   ├── base.html             ← Base layout with navbar
│   │   ├── login.html            ← Login form
│   │   ├── dashboard.html        ← Stats overview
│   │   ├── tickets.html          ← Ticket list with filters
│   │   ├── new_ticket.html       ← Raise ticket form with AI prediction preview
│   │   └── view_ticket.html      ← Ticket detail + audit log + admin controls
│   │
│   └── static/
│       ├── css/style.css         ← Application styles
│       └── js/main.js            ← AI prediction live preview, form interactions
│
└── logs/
    └── audit.log                 ← Application audit trail
```

---

## API / Route Documentation

| Method | Route | Access | Description |
|--------|-------|--------|-------------|
| GET/POST | `/login` | Public | Login page and authentication |
| GET | `/logout` | Logged in | Logout current user |
| GET | `/dashboard` | Logged in | Stats overview |
| GET | `/tickets` | Logged in | List all tickets (filtered by role) |
| GET/POST | `/tickets/new` | Logged in | Raise a new ticket |
| POST | `/tickets/predict` | Logged in | AJAX: predict priority from title+description |
| GET | `/tickets/<id>` | Logged in | View single ticket + audit log |
| POST | `/tickets/<id>/update` | Admin only | Update ticket status |

---

## What I Would Add Next

- **Email Notifications** — real SMTP integration (currently simulated with print logs) using Flask-Mail
- **Search** — full-text search across ticket titles and descriptions
- **SLA Tracking** — automatic escalation if ticket not resolved within defined time window
- **REST API** — JSON API endpoints so a mobile app or external service could integrate
- **Unit Tests** — pytest tests for AI prediction logic and route authentication
- **Analytics Charts** — Chart.js visualizations for ticket trends over time

---

## AI Tool Usage Disclosure

I built this project independently. I used AI assistants for debugging help and syntax reference. All architectural decisions — database schema design, role-based access logic, the AI prediction pipeline, audit log structure — are my own. I can explain every file and every function in this codebase.

---

*Built by Karan Panwar · IncidentIQ · 2026*
