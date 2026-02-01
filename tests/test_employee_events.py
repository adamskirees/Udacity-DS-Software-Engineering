import unittest
import sys
import os

# This line tells Python to look one level up and then into 'python-package'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'python-package')))

# NOW you can import it
from employee_events.employee import Employee
from employee_events.team import Team

class TestEmployeeLogic(unittest.TestCase):
    def setUp(self):
        # Path to the real DB for an integration test
        self.db_path = "python-package/employee_events/employee_events.db"
        self.emp = Employee(self.db_path)

    def test_performance_query_runs(self):
        """Test that the performance query returns a DataFrame and not an error."""
        # Testing with Alex Martinez (ID 1)
        result = self.emp.get_employee_performance(1)
        self.assertFalse(result.empty, "The performance result should not be empty")
        self.assertIn('net_score', result.columns)

    def test_flight_risk_logic(self):
        """Test that flight risk returns a DataFrame (even if empty)."""
        result = self.emp.check_flight_risk(1)
        self.assertTrue(hasattr(result, 'columns'), "Result should be a Pandas DataFrame")

if __name__ == '__main__':
    unittest.main()