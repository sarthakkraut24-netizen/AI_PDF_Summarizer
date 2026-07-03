# ==========================================================
# DATABASE.PY
# AI Document Assistant
# Compatible with Python 3.13+
# ==========================================================

import sqlite3
from datetime import datetime

DATABASE_NAME = "ai_document_assistant.db"


# ==========================================================
# CONNECT DATABASE
# ==========================================================

def get_connection():
    return sqlite3.connect(DATABASE_NAME)


# ==========================================================
# CREATE TABLES
# ==========================================================

def create_database():

    conn = get_connection()
    cursor = conn.cursor()

    # Upload History
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS uploads (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        filename TEXT,

        filetype TEXT,

        filesize REAL,

        upload_time TEXT

    )
    """)

    # Summary History
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS summaries (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        filename TEXT,

        summary_type TEXT,

        summary TEXT,

        created_at TEXT

    )
    """)

    # Translation History
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS translations (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        language TEXT,

        translated_text TEXT,

        created_at TEXT

    )
    """)

    # Chat History
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        question TEXT,

        answer TEXT,

        created_at TEXT

    )
    """)

    conn.commit()
    conn.close()


# ==========================================================
# SAVE FILE
# ==========================================================

def save_upload(filename, filetype, filesize):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO uploads

        (filename, filetype, filesize, upload_time)

        VALUES (?, ?, ?, ?)

    """, (

        filename,

        filetype,

        filesize,

        datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    ))

    conn.commit()
    conn.close()


# ==========================================================
# SAVE SUMMARY
# ==========================================================

def save_summary(filename, summary_type, summary):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO summaries

        (filename, summary_type, summary, created_at)

        VALUES (?, ?, ?, ?)

    """, (

        filename,

        summary_type,

        summary,

        datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    ))

    conn.commit()
    conn.close()


# ==========================================================
# SAVE TRANSLATION
# ==========================================================

def save_translation(language, translated_text):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO translations

        (language, translated_text, created_at)

        VALUES (?, ?, ?)

    """, (

        language,

        translated_text,

        datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    ))

    conn.commit()
    conn.close()


# ==========================================================
# SAVE CHAT
# ==========================================================

def save_chat(question, answer):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO chat_history

        (question, answer, created_at)

        VALUES (?, ?, ?)

    """, (

        question,

        answer,

        datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    ))

    conn.commit()
    conn.close()


# ==========================================================
# GET UPLOAD HISTORY
# ==========================================================

def get_uploads():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT * FROM uploads

        ORDER BY id DESC

    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


# ==========================================================
# GET SUMMARY HISTORY
# ==========================================================

def get_summaries():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT * FROM summaries

        ORDER BY id DESC

    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


# ==========================================================
# GET CHAT HISTORY
# ==========================================================

def get_chat_history():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT * FROM chat_history

        ORDER BY id DESC

    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


# ==========================================================
# DELETE ALL DATA
# ==========================================================

def clear_database():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM uploads")
    cursor.execute("DELETE FROM summaries")
    cursor.execute("DELETE FROM translations")
    cursor.execute("DELETE FROM chat_history")

    conn.commit()
    conn.close()


# ==========================================================
# DATABASE STATISTICS
# ==========================================================

def get_statistics():

    conn = get_connection()
    cursor = conn.cursor()

    stats = {}

    cursor.execute("SELECT COUNT(*) FROM uploads")
    stats["uploads"] = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM summaries")
    stats["summaries"] = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM translations")
    stats["translations"] = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM chat_history")
    stats["chat"] = cursor.fetchone()[0]

    conn.close()

    return stats


# ==========================================================
# INITIALIZE DATABASE
# ==========================================================

create_database()


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    create_database()

    print("Database created successfully.")

    print(get_statistics())
