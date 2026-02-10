import pandas as pd
from .query_base import QueryBase


# This is the main class for employee-level queries. It inherits the DB commection and query from QueryBase, 
# so we can focus on writing the SQL and processing the results.
class Employee(QueryBase):
    def __init__(self, db_path):
        super().__init__(db_path)

    def get_employee_details(self, employee_id):
        query = """
        SELECT 
            (e.first_name || ' ' || e.last_name) as name,
            SUM(ev.positive_events) as total_pos, 
            SUM(ev.negative_events) as total_neg,
            (SUM(ev.positive_events) - SUM(ev.negative_events)) as net_score
        FROM employee e 
        LEFT JOIN employee_events ev ON e.employee_id = ev.employee_id 
        WHERE e.employee_id = ? 
        GROUP BY e.employee_id
        """
        df = self.run_query(query, params=(employee_id,))
        
        # Check if we actually got a result and if 'name' isn't NULL
        if df is not None and not df.empty and df.iloc[0]['name'] is not None:
            return df.iloc[0].to_dict()
        return None

    def check_flight_risk(self, employee_id):
        query = """
        SELECT employee_id, note, note_date
        FROM notes
        WHERE employee_id = ? 
        AND (note LIKE '%unhappy%' OR note LIKE '%resignation%' OR note LIKE '%opportunity%')
        """
        return self.run_query(query, params=(employee_id,))