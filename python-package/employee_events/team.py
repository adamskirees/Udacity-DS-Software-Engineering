from .query_base import QueryBase

class Team(QueryBase):
    """
    Handles database logic for Team and Manager level analytics.
    """
    
    def get_team_stats(self, team_id):
        """
        Aggregates performance across a whole team to find the average net_score.
        """
        query = """
        SELECT 
            t.team_name,
            COUNT(e.employee_id) as member_count,
            SUM(ev.positive_events - ev.negative_events) as team_net_score
        FROM team t
        JOIN employee e ON t.team_id = e.team_id
        JOIN employee_events ev ON e.employee_id = ev.employee_id
        WHERE t.team_id = ?
        GROUP BY t.team_id
        """
        return self.run_query(query, params=(team_id,))

    def get_all_teams_risk_summary(self):
        query = """
        SELECT 
        t.team_name,
        COUNT(DISTINCT e.employee_id) as total_employees,
        -- ONly flag the most negative, if an employee has a net_score < -10, they are a risk
        SUM(CASE WHEN (ev.positive_events - ev.negative_events) < -10 THEN 1 ELSE 0 END) as risk_count
        FROM team t
        LEFT JOIN employee e ON t.team_id = e.team_id
        LEFT JOIN employee_events ev ON e.employee_id = ev.employee_id
        GROUP BY t.team_name
        """
        # Use your self.run_query helper
        df = self.run_query(query)
        return df
    
    def get_team_risk_details(self, team_name):
        query = """
        SELECT 
            e.employee_id,
            (e.first_name || ' ' || e.last_name) as name,
            (SUM(ev.positive_events) - SUM(ev.negative_events)) as net_score,
            CASE 
                WHEN (SUM(ev.positive_events) - SUM(ev.negative_events)) < -10 THEN 'High Risk'
                WHEN (SUM(ev.positive_events) - SUM(ev.negative_events)) < 0 THEN 'At Risk'
                ELSE 'Stable'
            END as status
        FROM team t
        JOIN employee e ON t.team_id = e.team_id
        JOIN employee_events ev ON e.employee_id = ev.employee_id
        WHERE t.team_name = ?
        GROUP BY e.employee_id
        HAVING net_score < 0  -- Only return those with negative scores
        ORDER BY net_score ASC
        """
        return self.run_query(query, params=(team_name,))