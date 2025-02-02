"""
Module for printing row counts of database tables.

This script connects to an SQLite database, retrieves all table names,
and prints the count of records in each table.
"""

import sqlite3

def print_table_counts(db_path="data/social_media.db"):
    """
    Prints the number of records in each table of the specified SQLite database.
    
    :param db_path: Path to the SQLite database file (default: "data/social_media.db").
    """
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Retrieve all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("📌 Tables in the database:", tables)

    # Count and print the number of records in each table
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        count = cursor.fetchone()[0]
        print(f"📌 Total records in table '{table_name}': {count}")
    
    # Close the database connection
    conn.close()

if __name__ == "__main__":
    print_table_counts()
