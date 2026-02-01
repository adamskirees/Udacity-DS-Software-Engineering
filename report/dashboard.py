import sys
import os
import pandas as pd

# The "Path Bridge" so the dashboard can find your python-package - lets check its working first
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'python-package')))

from employee_events.employee import Employee
from employee_events.team import Team

# Initialize our logic engines
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'python-package', 'employee_events', 'employee_events.db'))
emp_engine = Employee(db_path)
team_engine = Team(db_path)


if __name__ == "__main__":
    print("✅ Starting Dashboard Data Fetch...")
    
    # Get the high-level team risk summary
    risk_summary = team_engine.get_all_teams_risk_summary()
    
    print("\n--- TEAMS WITH HIGHEST RISK FLAGS ---")
    if not risk_summary.empty:
        print(risk_summary)
    else:
        print("No risks flagged! (Or check your 'notes' table data)")


# My Emoji Reference
# 🤔 Thinking Face \U0001F914
# ✅ Check Mark \U0001F504
# ❌ Cross Mark \U0001F534
# ⚠️ Warning Sign \U0001F6A8