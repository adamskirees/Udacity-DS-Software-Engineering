import sqlite3
import pandas as pd

class SQLMixin:
    def query_to_dataframe(self, query, params=()):
        """Handles the full lifecycle of a database request."""
        # 1. Connect (using the path we'll define in utils)
        conn = sqlite3.connect(self.db_path) 
        
        # 2. Execute & 3. Return (Pandas is great for this)
        try:
            df = pd.read_sql_query(query, conn, params=params)
        finally:
            # 4. Always close the connection
            conn.close()
        return df