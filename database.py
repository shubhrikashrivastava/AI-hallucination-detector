import sqlite3
import hashlib
from datetime import datetime

DB_NAME = "sentinel_cache.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS audit_cache 
                 (input_hash TEXT PRIMARY KEY, 
                  input_text TEXT,
                  full_report TEXT, 
                  trust_score INTEGER, 
                  timestamp DATETIME)''')
    conn.commit()
    conn.close()

def get_cached_audit(input_text):
    # Deterministic SHA256 Hash - will NEVER change for the same input
    input_hash = hashlib.sha256(input_text.encode()).hexdigest()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT full_report, trust_score FROM audit_cache WHERE input_hash=?", (input_hash,))
    result = c.fetchone()
    conn.close()
    return result

def save_audit_to_db(input_text, report, score):
    input_hash = hashlib.sha256(input_text.encode()).hexdigest()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("INSERT OR REPLACE INTO audit_cache VALUES (?, ?, ?, ?, ?)", 
                  (input_hash, input_text, report, score, datetime.now()))
        conn.commit()
    except Exception as e:
        print(f"Database Error: {e}")
    conn.close()

def get_all_history():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT input_text, trust_score, timestamp FROM audit_cache ORDER BY timestamp DESC LIMIT 10")
    history = c.fetchall()
    conn.close()
    return history