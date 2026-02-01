from .sql_execution import SQLiteMixin

class QueryBase(SQLiteMixin):
    def __init__(self, db_path):
        """
        Initializes the base class with the database location.
        Because we inherit from SQLiteMixin, we now have access to self.run_query().
        """
        self.db_path = db_path

    def get_all_teams(self):
        """
        A shared query example: Get all team names and IDs from the database.
        """
        query = "SELECT team_id, team_name FROM team"
        return self.run_query(query)