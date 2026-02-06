import sqlite3
import pandas as pd
from report.utils import get_db_path

db_path = get_db_path()
conn = sqlite3.connect(db_path)

print("--- TABLE NAMES ---")
tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)
print(tables)

print("\n--- EMPLOYEE SAMPLE ---")
try:
    emp = pd.read_sql_query("SELECT * FROM employee LIMIT 1;", conn)
    print(emp.columns.tolist())
except Exception as e: print(f"Error reading employee: {e}")

print("\n--- EVENTS SAMPLE ---")
try:
    events = pd.read_sql_query("SELECT * FROM employee_events LIMIT 1;", conn)
    print(events.columns.tolist())
except Exception as e: print(f"Error reading events: {e}")

conn.close()