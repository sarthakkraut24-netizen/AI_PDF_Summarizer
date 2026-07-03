# ==========================================================
# TABLE_READER.PY
# AI Document Assistant
# Compatible with Python 3.13+
# ==========================================================

import pdfplumber


# ==========================================================
# EXTRACT TABLES
# ==========================================================

def extract_tables(pdf_file):
    """
    Extract all tables from a PDF.
    Returns a list of tables.
    """

    tables = []

    pdf_file.seek(0)

    with pdfplumber.open(pdf_file) as pdf:

        for page in pdf.pages:

            page_tables = page.extract_tables()

            if page_tables:

                tables.extend(page_tables)

    return tables


# ==========================================================
# CONVERT TABLES TO TEXT
# ==========================================================

def tables_to_text(tables):
    """
    Convert extracted tables into readable text.
    """

    if not tables:
        return ""

    final_text = ""

    table_number = 1

    for table in tables:

        final_text += f"\n========== TABLE {table_number} ==========\n"

        for row in table:

            row = [str(cell).strip() if cell else "" for cell in row]

            final_text += " | ".join(row)

            final_text += "\n"

        final_text += "\n"

        table_number += 1

    return final_text.strip()


# ==========================================================
# TABLE SUMMARY
# ==========================================================

def table_statistics(tables):
    """
    Returns simple statistics.
    """

    total_tables = len(tables)

    total_rows = 0

    total_columns = 0

    for table in tables:

        total_rows += len(table)

        if table:

            total_columns += len(table[0])

    return {

        "tables": total_tables,

        "rows": total_rows,

        "columns": total_columns

    }


# ==========================================================
# MAIN FUNCTION
# ==========================================================

def read_tables(pdf_file):

    tables = extract_tables(pdf_file)

    text = tables_to_text(tables)

    stats = table_statistics(tables)

    return {

        "text": text,

        "tables": tables,

        "statistics": stats

    }


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    print("Table Reader Loaded Successfully.")