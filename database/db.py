"""
SQLite Database Handler for Scan Logging, Forensics History, and User Feedback.
"""

import sqlite3
import json
import os
from datetime import datetime

if os.environ.get("VERCEL"):
    DB_PATH = "/tmp/scam_detector.db"
else:
    DB_PATH = os.path.join(os.path.dirname(__file__), "scam_detector.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        input_type TEXT NOT NULL,
        content_preview TEXT NOT NULL,
        risk_score INTEGER NOT NULL,
        verdict TEXT NOT NULL,
        verdict_badge TEXT NOT NULL,
        model_name TEXT NOT NULL,
        signals_json TEXT,
        recommendations_json TEXT,
        token_weights_json TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        scan_id INTEGER,
        feedback_type TEXT NOT NULL,
        comment TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (scan_id) REFERENCES scans(id)
    )
    """)

    conn.commit()
    conn.close()

def log_scan(input_type, preview, risk_score, verdict, verdict_badge, model_name, signals, recs, tokens):
    conn = get_connection()
    cursor = conn.cursor()

    # Truncate preview if too long
    preview_clean = (preview[:180] + '...') if len(preview) > 180 else preview

    cursor.execute("""
    INSERT INTO scans (
        input_type, content_preview, risk_score, verdict, verdict_badge,
        model_name, signals_json, recommendations_json, token_weights_json
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        input_type,
        preview_clean,
        risk_score,
        verdict,
        verdict_badge,
        model_name,
        json.dumps(signals),
        json.dumps(recs),
        json.dumps(tokens)
    ))

    scan_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return scan_id

def get_recent_scans(limit=25):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, timestamp, input_type, content_preview, risk_score, verdict, verdict_badge, model_name
    FROM scans
    ORDER BY id DESC
    LIMIT ?
    """, (limit,))
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def get_scan_by_id(scan_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM scans WHERE id = ?", (scan_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        d = dict(row)
        d['signals'] = json.loads(d['signals_json']) if d['signals_json'] else []
        d['recommendations'] = json.loads(d['recommendations_json']) if d['recommendations_json'] else []
        d['token_weights'] = json.loads(d['token_weights_json']) if d['token_weights_json'] else []
        return d
    return None

def submit_feedback(scan_id, feedback_type, comment=""):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO feedback (scan_id, feedback_type, comment)
    VALUES (?, ?, ?)
    """, (scan_id, feedback_type, comment))
    conn.commit()
    conn.close()
    return True

def get_statistics():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM scans")
    total_scans = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scans WHERE risk_score >= 65")
    scam_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scans WHERE risk_score < 30")
    legit_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scans WHERE risk_score >= 30 AND risk_score < 65")
    suspicious_count = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(risk_score) FROM scans")
    avg_risk = cursor.fetchone()[0] or 0.0

    cursor.execute("""
    SELECT input_type, COUNT(*) as cnt FROM scans GROUP BY input_type
    """)
    type_distribution = {row['input_type']: row['cnt'] for row in cursor.fetchall()}

    conn.close()
    return {
        "total_scans": total_scans,
        "scam_count": scam_count,
        "suspicious_count": suspicious_count,
        "legit_count": legit_count,
        "avg_risk": round(float(avg_risk), 1),
        "type_distribution": type_distribution
    }

# Initialize tables immediately upon import
init_db()
