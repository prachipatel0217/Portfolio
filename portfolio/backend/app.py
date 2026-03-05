"""
Prachi Patel — Portfolio Backend
Flask + SQLite
Run: python app.py
API Base: http://localhost:5000/api
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3, os, re
from datetime import datetime
from database import init_db, get_db

app = Flask(__name__)
CORS(app)  # allow the frontend (file:// or localhost) to call the API

# ── DB path ───────────────────────────────────────────────────────────────────
DB_PATH = os.path.join(os.path.dirname(__file__), "portfolio.db")

# ── Init DB on startup ────────────────────────────────────────────────────────
with app.app_context():
    init_db(DB_PATH)

# ─────────────────────────────────────────────────────────────────────────────
# HELPER
# ─────────────────────────────────────────────────────────────────────────────

def valid_email(email: str) -> bool:
    return bool(re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email))


# ─────────────────────────────────────────────────────────────────────────────
# ROUTES — PROJECTS
# ─────────────────────────────────────────────────────────────────────────────

@app.route("/api/projects", methods=["GET"])
def get_projects():
    """Return all projects, optionally filtered by ?cat=web|ml|design|backend"""
    cat = request.args.get("cat", "all")
    with get_db(DB_PATH) as db:
        if cat == "all":
            rows = db.execute(
                "SELECT * FROM projects ORDER BY sort_order ASC"
            ).fetchall()
        else:
            rows = db.execute(
                "SELECT * FROM projects WHERE cat = ? ORDER BY sort_order ASC",
                (cat,)
            ).fetchall()
    return jsonify([dict(r) for r in rows])


@app.route("/api/projects/<int:project_id>", methods=["GET"])
def get_project(project_id):
    """Return a single project by ID (also increments view count)"""
    with get_db(DB_PATH) as db:
        db.execute(
            "UPDATE projects SET views = views + 1 WHERE id = ?", (project_id,)
        )
        row = db.execute(
            "SELECT * FROM projects WHERE id = ?", (project_id,)
        ).fetchone()
    if not row:
        return jsonify({"error": "Project not found"}), 404
    return jsonify(dict(row))


# ─────────────────────────────────────────────────────────────────────────────
# ROUTES — CONTACT MESSAGES
# ─────────────────────────────────────────────────────────────────────────────

@app.route("/api/contact", methods=["POST"])
def submit_contact():
    """Validate and save a contact form submission"""
    data = request.get_json(silent=True) or {}

    name    = data.get("name", "").strip()
    email   = data.get("email", "").strip()
    subject = data.get("subject", "").strip()
    message = data.get("message", "").strip()

    # — Validation —
    errors = {}
    if len(name) < 2:
        errors["name"] = "Name must be at least 2 characters."
    if not valid_email(email):
        errors["email"] = "Please enter a valid email address."
    if len(subject) < 3:
        errors["subject"] = "Subject must be at least 3 characters."
    if len(message) < 6:
        errors["message"] = "Message must be at least 6 characters."

    if errors:
        return jsonify({"success": False, "errors": errors}), 400

    # — Save to DB —
    with get_db(DB_PATH) as db:
        db.execute(
            """INSERT INTO messages (name, email, subject, message, created_at)
               VALUES (?, ?, ?, ?, ?)""",
            (name, email, subject, message, datetime.utcnow().isoformat())
        )

    return jsonify({
        "success": True,
        "message": "Your message has been saved! Prachi will reply within 24 hours. 🌸"
    }), 201


@app.route("/api/messages", methods=["GET"])
def get_messages():
    """Admin: list all contact messages (protect this route in production!)"""
    with get_db(DB_PATH) as db:
        rows = db.execute(
            "SELECT * FROM messages ORDER BY created_at DESC"
        ).fetchall()
    return jsonify([dict(r) for r in rows])


# ─────────────────────────────────────────────────────────────────────────────
# ROUTES — VISITOR STATS
# ─────────────────────────────────────────────────────────────────────────────

@app.route("/api/stats/visit", methods=["POST"])
def record_visit():
    """Called once per page load to increment the visitor counter"""
    page = request.get_json(silent=True, force=True) or {}
    page_name = page.get("page", "home")
    with get_db(DB_PATH) as db:
        db.execute(
            """INSERT INTO visits (page, visited_at) VALUES (?, ?)""",
            (page_name, datetime.utcnow().isoformat())
        )
    return jsonify({"success": True})


@app.route("/api/stats", methods=["GET"])
def get_stats():
    """Return aggregated portfolio stats"""
    with get_db(DB_PATH) as db:
        total_visits   = db.execute("SELECT COUNT(*) FROM visits").fetchone()[0]
        total_messages = db.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
        total_projects = db.execute("SELECT COUNT(*) FROM projects").fetchone()[0]
        top_projects   = db.execute(
            "SELECT id, title, views FROM projects ORDER BY views DESC LIMIT 3"
        ).fetchall()

    return jsonify({
        "total_visits":   total_visits,
        "total_messages": total_messages,
        "total_projects": total_projects,
        "top_projects":   [dict(r) for r in top_projects],
    })


# ─────────────────────────────────────────────────────────────────────────────
# ROUTES — SKILLS
# ─────────────────────────────────────────────────────────────────────────────

@app.route("/api/skills", methods=["GET"])
def get_skills():
    """Return all skills grouped by category"""
    with get_db(DB_PATH) as db:
        rows = db.execute(
            "SELECT * FROM skills ORDER BY category, sort_order"
        ).fetchall()
    # group by category
    grouped = {}
    for r in rows:
        r = dict(r)
        grouped.setdefault(r["category"], []).append(r)
    return jsonify(grouped)


# ─────────────────────────────────────────────────────────────────────────────
# RUN
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)