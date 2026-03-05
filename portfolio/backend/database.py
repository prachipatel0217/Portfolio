"""
database.py — SQLite setup & seed data for Prachi's portfolio backend
"""

import sqlite3
from contextlib import contextmanager


# ─────────────────────────────────────────────────────────────────────────────
# CONNECTION HELPER
# ─────────────────────────────────────────────────────────────────────────────

@contextmanager
def get_db(db_path: str):
    """Context manager: yields a SQLite connection, auto-commits & closes."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row          # rows behave like dicts
    conn.execute("PRAGMA journal_mode=WAL") # better concurrent read performance
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# ─────────────────────────────────────────────────────────────────────────────
# SCHEMA  +  SEED DATA
# ─────────────────────────────────────────────────────────────────────────────

SCHEMA = """
-- ── Projects ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS projects (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    cat         TEXT    NOT NULL,          -- web | ml | design | backend
    icon        TEXT    NOT NULL,
    bg          TEXT    NOT NULL,          -- CSS gradient string
    title       TEXT    NOT NULL,
    description TEXT    NOT NULL,
    tags        TEXT    NOT NULL,          -- comma-separated list
    github_url  TEXT    DEFAULT '',
    demo_url    TEXT    DEFAULT '',
    views       INTEGER DEFAULT 0,
    sort_order  INTEGER DEFAULT 0
);

-- ── Contact Messages ─────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS messages (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT    NOT NULL,
    email      TEXT    NOT NULL,
    subject    TEXT    NOT NULL,
    message    TEXT    NOT NULL,
    is_read    INTEGER DEFAULT 0,          -- 0 = unread, 1 = read
    created_at TEXT    NOT NULL            -- ISO-8601 UTC
);

-- ── Visitor Tracking ─────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS visits (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    page       TEXT    NOT NULL DEFAULT 'home',
    visited_at TEXT    NOT NULL            -- ISO-8601 UTC
);

-- ── Skills ───────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS skills (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    category   TEXT    NOT NULL,           -- Frontend | Backend | Database | Tools
    badge      TEXT    NOT NULL,           -- short badge label, e.g. "JS"
    name       TEXT    NOT NULL,
    percent    INTEGER NOT NULL,
    sort_order INTEGER DEFAULT 0
);
"""

# ── Seed projects (mirrors the JS PROJS array + extra fields) ────────────────
SEED_PROJECTS = [
    (1, "web",     "🛒", "linear-gradient(135deg,#1a0d20,#7a3560)",
     "E-Commerce Platform",
     "Fully responsive online store with product filtering, cart, wishlist and checkout. "
     "React frontend with Django backend and MySQL database.",
     "React,Django,MySQL,REST API", "https://github.com/prachipatel", "", 1),

    (2, "ml",      "🧠", "linear-gradient(135deg,#150d20,#6a3065)",
     "ML Image Classifier",
     "Deep learning CNN achieving 95% accuracy on CIFAR-10. Packaged as a Flask REST API "
     "with an interactive Streamlit demo dashboard.",
     "Python,TensorFlow,OpenCV,Flask", "https://github.com/prachipatel", "", 2),

    (3, "web",     "📋", "linear-gradient(135deg,#1a0c22,#7a3a7a)",
     "Task Management App",
     "Kanban board with drag & drop, team collaboration, real-time notifications via "
     "WebSockets and a MongoDB backend.",
     "React,Node.js,Socket.io,MongoDB", "https://github.com/prachipatel", "", 3),

    (4, "design",  "🎨", "linear-gradient(135deg,#1c0d18,#8a3560)",
     "Brand Identity System",
     "Complete visual identity — logo, typography, color system, brand guidelines and a "
     "full Figma UI component kit for a tech startup.",
     "Figma,Illustrator,UI Design,Branding", "", "", 4),

    (5, "backend", "⚙️", "linear-gradient(135deg,#120810,#6a3050)",
     "REST API Service",
     "Scalable FastAPI service with JWT authentication, rate limiting, Swagger documentation "
     "and Docker deployment ready for production.",
     "Python,FastAPI,PostgreSQL,Docker", "https://github.com/prachipatel", "", 5),

    (6, "ml",      "💬", "linear-gradient(135deg,#180d22,#6a4075)",
     "Sentiment Analyzer",
     "NLP app using BERT transformers to classify customer reviews and social media "
     "sentiment. Deployed live on Streamlit Cloud.",
     "Python,BERT,NLTK,Streamlit", "https://github.com/prachipatel", "https://streamlit.io", 6),
]

SEED_SKILLS = [
    # Frontend
    ("Frontend", "HTML", "HTML5",       90, 1),
    ("Frontend", "CSS",  "CSS3",        88, 2),
    ("Frontend", "TW",   "Tailwind CSS",82, 3),
    ("Frontend", "JS",   "JavaScript",  85, 4),
    ("Frontend", "Re",   "React",       80, 5),
    # Backend
    ("Backend",  "Py",   "Python",      92, 1),
    ("Backend",  "Dj",   "Django",      85, 2),
    ("Backend",  "Nd",   "Node.js",     78, 3),
    ("Backend",  "Exp",  "Express",     75, 4),
    # Database
    ("Database", "My",   "MySQL",       80, 1),
    ("Database", "SL",   "SQLite",      85, 2),
    ("Database", "Mg",   "MongoDB",     65, 3),
    # Tools
    ("Tools",    "Git",  "Git & GitHub",88, 1),
    ("Tools",    "VS",   "VS Code",     95, 2),
    ("Tools",    "Fg",   "Figma",       72, 3),
]


# ─────────────────────────────────────────────────────────────────────────────
# PUBLIC INIT FUNCTION
# ─────────────────────────────────────────────────────────────────────────────

def init_db(db_path: str) -> None:
    """Create tables and seed data if they don't already exist."""
    with get_db(db_path) as db:
        db.executescript(SCHEMA)

        # Seed projects only if table is empty
        count = db.execute("SELECT COUNT(*) FROM projects").fetchone()[0]
        if count == 0:
            db.executemany(
                """INSERT INTO projects
                   (id, cat, icon, bg, title, description, tags, github_url, demo_url, sort_order)
                   VALUES (?,?,?,?,?,?,?,?,?,?)""",
                SEED_PROJECTS,
            )
            print("✅  Projects seeded.")

        # Seed skills only if table is empty
        count = db.execute("SELECT COUNT(*) FROM skills").fetchone()[0]
        if count == 0:
            db.executemany(
                """INSERT INTO skills (category, badge, name, percent, sort_order)
                   VALUES (?,?,?,?,?)""",
                SEED_SKILLS,
            )
            print("✅  Skills seeded.")

    print("✅  Database ready.")