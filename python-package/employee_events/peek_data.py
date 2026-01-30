import sqlite3
import pandas as pd
import os

# Let's be 100% sure about the path
# absolute path
db_path = db_path = "employee_events.db"

def inspect_db():
    if not os.path.exists(db_path):
        print(f"❌ Error: The file '{db_path}' does not exist at this location.")
        print(f"Current working directory is: {os.getcwd()}")
        return

    conn = sqlite3.connect(db_path)
    
    # 1. Ask the database what tables it contains
    tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)
    print("--- TABLES FOUND IN DATABASE ---")
    print(tables)
    
    if tables.empty:
        print("\n⚠️ The database is empty. Check if the path is correct!")
    else:
        # 2. Automatically peek at the FIRST table found
        first_table = tables['name'].iloc[0]
        print(f"\n--- PEEKING AT TABLE: {first_table} ---")
        peek = pd.read_sql_query(f"SELECT * FROM {first_table} LIMIT 5;", conn)
        print(peek)

    conn.close()

if __name__ == "__main__":
    inspect_db()