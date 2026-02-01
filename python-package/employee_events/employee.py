from .query_base import QueryBase

class Employee(QueryBase):
    def get_employee_performance(self, employee_id):
        """
        Calculates score using 'employee_events' table from the ERD.
        """
        query = """
        SELECT 
            employee_id, 
            SUM(positive_events) as total_pos, 
            SUM(negative_events) as total_neg,
            (SUM(positive_events) - SUM(negative_events)) as net_score
        FROM employee_events
        WHERE employee_id = ?
        GROUP BY employee_id
        """
        return self.run_query(query, params=(employee_id,))

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