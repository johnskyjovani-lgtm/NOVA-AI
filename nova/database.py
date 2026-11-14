import sqlite3
from datetime import datetime

def connect(path):
    con = sqlite3.connect(str(path)); con.row_factory = sqlite3.Row; return con

def init_db(path):
    with connect(path) as con:
        con.execute('CREATE TABLE IF NOT EXISTS messages(id INTEGER PRIMARY KEY, role TEXT, content TEXT, created_at TEXT)')

def save_message(path, role, content):
    with connect(path) as con:
        con.execute('INSERT INTO messages(role,content,created_at) VALUES(?,?,?)', (role, content, datetime.now().isoformat(timespec='seconds')))

def recent_messages(path, limit=30):
    with connect(path) as con:
        rows = con.execute('SELECT role,content,created_at FROM messages ORDER BY id DESC LIMIT ?', (limit,)).fetchall()
    return [dict(r) for r in reversed(rows)]
