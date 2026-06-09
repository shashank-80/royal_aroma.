import sqlite3
import os
import bcrypt

DB_PATH = "database/royal_aroma.db"
os.makedirs("database", exist_ok=True)

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password_hash TEXT NOT NULL,
                name TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS wishlists (
                username TEXT,
                perfume_id INTEGER,
                PRIMARY KEY (username, perfume_id)
            )
        """)
        conn.commit()

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def register_user(username, password, name):
    try:
        with get_connection() as conn:
            pwd_h = hash_password(password)
            conn.execute("INSERT INTO users VALUES (?, ?, ?)", (username.lower().strip(), pwd_h, name))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False

def authenticate_user(username, password):
    with get_connection() as conn:
        res = conn.execute("SELECT * FROM users WHERE username = ?", (username.lower().strip(),)).fetchone()
        if res and check_password(password, res['password_hash']):
            return {"username": res['username'], "name": res['name']}
    return None

def add_to_wishlist(username, perfume_id):
    try:
        with get_connection() as conn:
            conn.execute("INSERT OR IGNORE INTO wishlists VALUES (?, ?)", (username.lower(), int(perfume_id)))
            conn.commit()
    except Exception as e:
        pass

def remove_from_wishlist(username, perfume_id):
    with get_connection() as conn:
        conn.execute("DELETE FROM wishlists WHERE username = ? AND perfume_id = ?", (username.lower(), int(perfume_id)))
        conn.commit()

def get_user_wishlist(username):
    with get_connection() as conn:
        rows = conn.execute("SELECT perfume_id FROM wishlists WHERE username = ?", (username.lower(),)).fetchall()
        return [r['perfume_id'] for r in rows]

init_db()
