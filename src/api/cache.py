import sqlite3
import os
import json
import hashlib

DB_FILE = os.path.join(os.path.dirname(__file__), "cache.db")

def get_connection():
    # allow use across threads
    return sqlite3.connect(DB_FILE, check_same_thread=False)

def cache_key(prefix: str, params: dict) -> str:
    """
    Generate a stable cache key based on prefix + params.
    """
    params_str = json.dumps(params, sort_keys=True)
    key_hash = hashlib.sha256(params_str.encode()).hexdigest()
    return f"{prefix}:{key_hash}"

def cache_get(key: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS cache (key TEXT PRIMARY KEY, value TEXT)")
    row = cur.execute("SELECT value FROM cache WHERE key=?", (key,)).fetchone()
    conn.close()
    if row:
        return json.loads(row[0])
    return None

def cache_set(key: str, value: dict):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS cache (key TEXT PRIMARY KEY, value TEXT)")
    cur.execute("REPLACE INTO cache (key, value) VALUES (?, ?)", (key, json.dumps(value)))
    conn.commit()
    conn.close()
