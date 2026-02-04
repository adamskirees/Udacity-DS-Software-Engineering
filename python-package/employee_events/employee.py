import pandas as pd
from .query_base import QueryBase

class Employee(QueryBase):
    def __init__(self, db_path):
        super().__init__(db_path)
        """ the above calls the parent QueryBase setup, creates 'self.conn'"""

    def get_employee_details(self, employee_id):
        query = """
        SELECT 
            (e.first_name || ' ' || e.last_name) as name, -- Glue first and last name together
            SUM(positive_events) as total_pos,            -- Using actual column names from ERD
            SUM(negative_events) as total_neg,
            (SUM(positive_events) - SUM(negative_events)) as net_score
        FROM employee e 
        LEFT JOIN employee_events ev ON e.employee_id = ev.employee_id 
        WHERE e.employee_id = ? 
        GROUP BY e.employee_id
        """
        df = self.run_query(query, params=(employee_id,))
        return df.iloc[0].to_dict() if not df.empty else None

    def check_flight_risk(self, employee_id):
        """
        Checks for risk keywords in the 'notes' table from the ERD.
        """
        query = """
        SELECT employee_id, note, note_date
        FROM notes
        WHERE employee_id = ? 
        AND (note LIKE '%unhappy%' OR note LIKE '%resignation%' OR note LIKE '%opportunity%')
        """
        return self.run_query(query, params=(employee_id,))