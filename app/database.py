from pathlib import Path
import sqlite3

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "alhuda.db"

def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)

def initialize():
    with get_connection() as con:
        con.executescript("""
        CREATE TABLE IF NOT EXISTS bookmarks(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          type TEXT NOT NULL, reference TEXT NOT NULL,
          title TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS history(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          type TEXT NOT NULL, reference TEXT NOT NULL,
          title TEXT, opened_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS notes(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          type TEXT NOT NULL, reference TEXT NOT NULL,
          note TEXT NOT NULL, created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS settings(
          key TEXT PRIMARY KEY, value TEXT NOT NULL
        );
        """)
