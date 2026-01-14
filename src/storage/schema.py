from storage.db import get_connection

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        event_type TEXT NOT NULL,
        path TEXT NOT NULL,
        is_directory INTEGER NOT NULL,
        process_name TEXT,
        pid INTEGER
    );
    """)

    conn.commit()
    conn.close()
