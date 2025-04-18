import sqlite3
from datetime import datetime

DB_NAME = "keyflow.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            words INTEGER,
            wpm REAL,
            pauses INTEGER,
            input TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_metrics(metrics):
    # No guardamos si no hay entrada válida
    if not metrics.get("key"):
        return

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO sessions (timestamp, words, wpm, pauses, input)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        datetime.now().isoformat(),
        metrics["words"],
        metrics["wpm"],
        metrics["pauses"],
        metrics["key"]
    ))
    conn.commit()
    conn.close()
