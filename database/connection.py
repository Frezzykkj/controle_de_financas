import sqlite3

def get_connection():
    conn = sqlite3.connect("storage/banco.db")
    return conn