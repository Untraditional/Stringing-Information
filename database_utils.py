# Database Setup
import sqlite3


def setup_database():
    conn = sqlite3.connect("stringing.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS StringingRecords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        racket TEXT NOT NULL,
        string TEXT NOT NULL,
        tension TEXT NOT NULL,
        date_strung TEXT NOT NULL,
        who_strung TEXT NOT NULL
    )""")
    conn.commit()
    conn.close()