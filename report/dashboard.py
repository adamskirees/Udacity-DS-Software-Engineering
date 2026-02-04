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
    def __init__(self, emp_id, emp_name, metrics):
        self.emp_id = emp_id
        self.emp_name = emp_name
        self.metrics = metrics
        
    def __ft__(self):
        return Div(
            H2(f"Performance Profile: {self.emp_name}"),
            P(f"Employee ID: {self.emp_id}"),
            # Displaying the scores we pulled
            Ul(
                Li(f"✅ Positive Events: {self.metrics['total_pos']}"),
                Li(f"❌ Negative Events: {self.metrics['total_neg']}"),
                Li(B(f"📊 Net Productivity: {self.metrics['net_score']}"))
            ),
            cls="container"
        )


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
# --- EMPLOYEE ROUTE ---
@rt("/employee/{id}")
def get(id: int):
    # Fetch the combined dictionary (Name + Scores)
    details = emp_engine.get_employee_details(id)
    
    if details:
        # Pass the real database name and the dictionary to your component
        return EmployeeDashboard(
            emp_id=id, 
            emp_name=details['name'], 
            metrics=details
        )
    return Titled("Error", P(f"Employee {id} not found."))

if __name__ == "__main__":
    serve()

# My Emoji Reference
# 🤔 Thinking Face \U0001F914
# ✅ Check Mark \U0001F504
# ❌ Cross Mark \U0001F534
# ⚠️ Warning Sign \U0001F6A8