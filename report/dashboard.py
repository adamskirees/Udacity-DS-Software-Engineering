import sys
from pathlib import Path

# Get the root directory and add the python-package folder to the search path
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT / "python-package"))


from fasthtml.common import *
# Direct import from the sub-module to avoid __init__ confusion
from report.combined_components.combined_component import DashboardPage, Sidebar, PerformanceChart
from report.utils import load_model, get_db_path
from employee_events.employee import Employee
from employee_events.team import Team

# Custom Component Subclassing
class EmployeeDashboard(DashboardPage):
    def __init__(self, emp_data):
        self.emp_data = emp_data
        # This is where you'd use inheritance to build your custom HTML structure

app, rt = fast_app()

# Initialize our engines
DB_PATH = get_db_path()
emp_engine = Employee(DB_PATH)
team_engine = Team(DB_PATH)
model = load_model()

# --- INDEX ROUTE ---
@rt("/")
def get():
    return Titled("Employee Flight Risk Dashboard",
        P("Welcome, Manager. Use the sidebar to navigate between Team and Employee views."),
        A("View Team Stats", href="/team"),
        A("View Employee Stats", href="/employee/1")
    )

# --- TEAM ROUTE ---
@rt("/team")
def get():
    risk_summary = team_engine.get_all_teams_risk_summary()
    # Fixed the typo here: itertuples()
    rows = [Tr(Td(r.team_name), Td(str(r.risk_count))) for r in risk_summary.itertuples()]
    return Titled("Team Risk Summary",
        Table(Thead(Tr(Th("Team Name"), Th("Risk Flags"))),
              Tbody(*rows))
    )

# --- EMPLOYEE ROUTE ---
@rt("/employee/{id}")
def get(id: int):
    perf = emp_engine.get_employee_performance(id)
    return Titled(f"Performance for Employee {id}",
        P(f"Net Productivity Score: {perf.net_score.iloc[0]}"),
        P(f"Positive Events: {perf.total_pos.iloc[0]}"),
        P(f"Negative Events: {perf.total_neg.iloc[0]}")
    )

if __name__ == "__main__":
    serve()

# My Emoji Reference
# 🤔 Thinking Face \U0001F914
# ✅ Check Mark \U0001F504
# ❌ Cross Mark \U0001F534
# ⚠️ Warning Sign \U0001F6A8