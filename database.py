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
# CREATE DATABASE
# ==========================================================

def create_database():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS uploads(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        filetype TEXT,
        filesize REAL,
        upload_time TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS summaries(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        summary_type TEXT,
        summary TEXT,
        created_at TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS translations(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        language TEXT,
        translated_text TEXT,
        created_at TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history(
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
        (filename,filetype,filesize,upload_time)

        VALUES(?,?,?,?)

    """,(

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
        (filename,summary_type,summary,created_at)

        VALUES(?,?,?,?)

    """,(

        filename,
        summary_type,
        summary,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    ))

    conn.commit()
    conn.close()


# ==========================================================
# SAVE HISTORY
# Used by app.py
# ==========================================================

def save_history(filename, summary):

    save_summary(

        filename,

        "Generated",

        summary

    )


# ==========================================================
# LOAD HISTORY
# Used by app.py
# ==========================================================

def load_history():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT filename,
               summary,
               created_at

        FROM summaries

        ORDER BY id DESC

    """)

    rows = cursor.fetchall()

    conn.close()

    history = []

    for row in rows:

        history.append({

            "filename": row[0],

            "summary": row[1],

            "created_at": row[2]

        })

    return history


# ==========================================================
# SAVE TRANSLATION
# ==========================================================

def save_translation(language, translated_text):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO translations
        (language,translated_text,created_at)

        VALUES(?,?,?)

    """,(

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
        (question,answer,created_at)

        VALUES(?,?,?)

    """,(

        question,
        answer,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    ))

    conn.commit()
    conn.close()


# ==========================================================
# GET STATISTICS
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
# CLEAR DATABASE
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
# INITIALIZE DATABASE
# ==========================================================

create_database()


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    print("Database Ready")

    print(get_statistics())