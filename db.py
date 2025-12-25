import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("inventory.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sku TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                qty INTEGER NOT NULL DEFAULT 0,
                location TEXT NOT NULL DEFAULT 'N/A',
                updated_at TEXT NOT NULL DEFAULT (datetime('now'))
            );
        """)
        conn.commit()

def add_item(sku, name, qty, location):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO items (sku, name, qty, location) VALUES (?, ?, ?, ?)",
            (sku, name, qty, location)
        )
        conn.commit()

def adjust_qty(sku, delta):
    with get_conn() as conn:
        cur = conn.execute(
            "UPDATE items SET qty = qty + ?, updated_at = datetime('now') WHERE sku = ?",
            (delta, sku)
        )
        conn.commit()
        return cur.rowcount

def search(query):
    q = f"%{query}%"
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM items WHERE sku LIKE ? OR name LIKE ? ORDER BY name",
            (q, q)
        ).fetchall()

def all_items():
    with get_conn() as conn:
        return conn.execute("SELECT * FROM items ORDER BY name").fetchall()
