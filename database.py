# ==========================================================
# DATABASE MODULE
# SQLite Database
# Compatible with Python 3.13+
# ==========================================================

import sqlite3
import os
from datetime import datetime

# ==========================================================
# DATABASE CONFIGURATION
# ==========================================================

DATABASE_FOLDER = "database"
DATABASE_NAME = "ai_document_assistant.db"

os.makedirs(DATABASE_FOLDER, exist_ok=True)

DATABASE_PATH = os.path.join(
    DATABASE_FOLDER,
    DATABASE_NAME
)

# ==========================================================
# CONNECT DATABASE
# ==========================================================

def connect_db():

    return sqlite3.connect(DATABASE_PATH)


# ==========================================================
# CREATE TABLE
# ==========================================================

def init_db():

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS summaries (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            filename TEXT,

            summary_type TEXT,

            language TEXT,

            original_text TEXT,

            summary TEXT,

            created_at TEXT

        )
    """)

    conn.commit()

    conn.close()


# ==========================================================
# SAVE SUMMARY
# ==========================================================

def save_summary_db(
    filename,
    summary_type,
    language,
    original_text,
    summary
):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO summaries(

            filename,
            summary_type,
            language,
            original_text,
            summary,
            created_at

        )

        VALUES(?,?,?,?,?,?)

    """, (

        filename,

        summary_type,

        language,

        original_text,

        summary,

        datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    ))

    conn.commit()

    conn.close()


# ==========================================================
# GET HISTORY
# ==========================================================

def get_history():

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM summaries

        ORDER BY id DESC

    """)

    data = cursor.fetchall()

    conn.close()

    return data


# ==========================================================
# GET SUMMARY BY ID
# ==========================================================

def get_summary(summary_id):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM summaries

        WHERE id=?

    """, (summary_id,))

    data = cursor.fetchone()

    conn.close()

    return data


# ==========================================================
# DELETE SUMMARY
# ==========================================================

def delete_summary(summary_id):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""

        DELETE FROM summaries

        WHERE id=?

    """, (summary_id,))

    conn.commit()

    conn.close()


# ==========================================================
# DELETE ALL HISTORY
# ==========================================================

def clear_database():

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("DELETE FROM summaries")

    conn.commit()

    conn.close()


# ==========================================================
# TOTAL SUMMARIES
# ==========================================================

def total_summaries():

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT COUNT(*)

        FROM summaries

    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total


# ==========================================================
# TOTAL WORDS SUMMARIZED
# ==========================================================

def total_words():

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT summary

        FROM summaries

    """)

    rows = cursor.fetchall()

    conn.close()

    total = 0

    for row in rows:

        total += len(row[0].split())

    return total


# ==========================================================
# DATABASE STATISTICS
# ==========================================================

def database_stats():

    return {

        "Total Summaries": total_summaries(),

        "Total Words": total_words()

    }


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    init_db()

    print("Database Created Successfully")

    print(database_stats())