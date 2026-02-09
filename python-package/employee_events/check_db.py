import sqlite3
import os

# Updated path logic to find your DB
db_path = 'employee_events.db'

def debug_average():
    if not os.path.exists(db_path):
        print(f"CRITICAL ERROR: {db_path} not found in this folder!")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        # The specific subquery for temporal tables
        query = """
            SELECT AVG(total_net) FROM (
                SELECT SUM(positive_events - negative_events) as total_net 
                FROM employee_events 
                GROUP BY employee_id
            )
        """
        cursor.execute(query)
        result = cursor.fetchone()
        
        print(f"\n--- DATABASE DEBUG ---")
        print(f"Subquery Result: {result}")
        
        if result and result[0] is not None:
            print(f"SUCCESS: Team Average is {result[0]:.2f}")
        else:
            print("FAILURE: Query returned None/Nil. Check table data.")
            
    except Exception as e:
        print(f"SQL ERROR: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    debug_average()