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
        """
        Identifies which teams have the most 'flagged' notes.
        """
        query = """
        SELECT t.team_name, COUNT(n.note) as risk_count
        FROM team t
        JOIN notes n ON t.team_id = n.team_id
        WHERE n.note LIKE '%unhappy%' OR n.note LIKE '%resignation%'
        GROUP BY t.team_name
        ORDER BY risk_count DESC
        """
        return self.run_query(query)