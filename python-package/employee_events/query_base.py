from .sql_execution import SQLiteMixin



class QueryBase(SQLiteMixin):
    def __init__(self, db_path):
        """
        Initializes the base class with the database location.
        Inheritance passes methods (like run_query) to all subclasses (Employee, Team).
        Parent class above - rememeber ! 
        """
        self.db_path = db_path

    def get_all_teams(self):
        """
        A shared query example: Get all team names and IDs from the database.
        """
        query = "SELECT team_id, team_name FROM team"
        return self.run_query(query)