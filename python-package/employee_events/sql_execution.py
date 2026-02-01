import sqlite3
import pandas as pd

class SQLiteMixin:
    """
    Handles the lifecycle of a database request:
    Connect -> Execute -> Fetch as DataFrame -> Close.
    """
    def run_query(self, query: str, params: tuple = ()):
        # self.db_path will be defined in the class that inherits this
        conn = sqlite3.connect(self.db_path)
        
        try:
            # We use pandas to return data ready for data science tasks
            df = pd.read_sql_query(query, conn, params=params)
            return df
        except Exception as e:
            print(f"Database error: {e}")
            raise e
        finally:
            # Crucial for SQLite: Always close to avoid 'database is locked' errors
            conn.close()