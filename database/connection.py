import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'storage', 'banco.db')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
