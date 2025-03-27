import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'chat_memory.db'))
print("📁 DB Path:", DB_PATH)

try:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat_history (role, content, timestamp) VALUES (?, ?, ?)",
                   ("user", "test message", datetime.now().isoformat()))
    conn.commit()
    print("✅ Inserted successfully.")
except Exception as e:
    print("❌ ERROR:", e)