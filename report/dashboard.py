import sys
from pathlib import Path
import pandas as pd
from fasthtml.common import *

# 1. Setup paths
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT / "python-package"))

# 2. Imports
from report.combined_components.combined_component import DashboardPage, Sidebar, PerformanceChart
from report.utils import load_model, get_db_path
from employee_events.employee import Employee
from employee_events.team import Team

# 3. Custom Component - Employee Dashboard. This is also where we add the visualization logic for the performance chart.
class EmployeeDashboard(DashboardPage):
    def __init__(self, emp_id, emp_name, metrics, risk_prob):
        self.emp_id = emp_id
        self.emp_name = emp_name
        self.metrics = metrics
        self.risk_prob = risk_prob
        
    def __ft__(self):
        risk_color = "red" if self.risk_prob > 0.7 else "orange" if self.risk_prob > 0.4 else "green"
        total = self.metrics['total_pos'] + self.metrics['total_neg']
        perf_pct = (self.metrics['total_pos'] / total * 100) if total > 0 else 0
        
        # We use standard Divs here to bypass any potential inheritance 'hiding' the visuals
        return Container(
            Div(
                H2(f"Analysis: {self.emp_name}"),
                Grid(
                    # VISUALIZATION 1
                    Div(
                        H4("Turnover Risk"),
                        P(f"{self.risk_prob:.1%}", style=f"color: {risk_color}; font-size: 2rem; font-weight: bold;"),
                        # Standard HTML Progress bar
                        Progress(value=str(int(self.risk_prob * 100)), max="100", 
                                 style=f"display: block; width: 100%; height: 20px; accent-color: {risk_color};"),
                    ),
                    # VISUALIZATION 2
                    Div(
                        H4("Performance Balance"),
                        P(f"Positive Ratio: {perf_pct:.1f}%"),
                        Progress(value=str(int(perf_pct)), max="100", 
                                 style="display: block; width: 100%; height: 20px; accent-color: green;"),
                    )
                ),
                Br(),
                A("← Back to Dashboard", href="/team", cls="button outline"),
                cls="card" 
            )
        )

# 4. App Setup
app, rt = fast_app(
    hdrs=(Link(rel="stylesheet", href="/static/report.css"),),
    live=True
)

# 5. Static Files Router (FIXED INDENTATION HERE)
@rt("/static/{path:path}")
def get(path: str): 
    # This assumes your css is at report/static/report.css
    return FileResponse(ROOT / "report" / "assets" / path)

# 6. Initialize engines
DB_PATH = get_db_path()
emp_engine = Employee(DB_PATH)
team_engine = Team(DB_PATH)
model = load_model()

# --- ROUTES ---
@rt("/")
def get():
    return Titled("Manager Command Center",
        Container(
            P("Welcome, Manager. Select a view to begin."),
            Grid(
                Card(
                    H3("Team Overview"),
                    P("View aggregate risk across all departments."),
                    A("Open Team Dashboard", href="/team", cls="button")
                ),
                Card(
                    H3("Employee Deep-Dive"),
                    P("Analyze individual performance and flight risk."),
                    A("Search Employee #1", href="/employee/1", cls="button")
                )
            )
        )
    )

@rt("/team")
def get():
    df = team_engine.get_all_teams_risk_summary()
    
    # Debug: Print to terminal to see if data exists
    print(f"DEBUG: Team Data Found:\n{df}")
    
    if df.empty:
        return Titled("Team Summary", P("No team data found in the database."))

    rows = []
    for _, r in df.iterrows():
        # logic: if risk_count > 0, make the number Red and Bold
        is_high_risk = r['risk_count'] > (r['total_employees'] * 0.1)
        risk_style = "color: red; font-weight: bold;" if r['risk_count'] > 0 else "color: green;"
        
        rows.append(Tr(
            # Link the team name to a (future) team detail page
            Td(A(r['team_name'], href=f"/team/{r['team_name']}")), 
            Td(Span(str(r['risk_count']), style=risk_style)),
            Td(str(r['total_employees']))
        ))
    
    return Titled("Department Risk Audit",
        Container(
            Table(
                Thead(Tr(Th("Department"), Th("Risk Flags"), Th("Total Staff"))),
                Tbody(*rows)
            ),
            A("← Back to Home", href="/", cls="button outline")
        )
    )

@rt("/employee/{id}")
def get(id: int):
    details = emp_engine.get_employee_details(id)
    
    if not details:
        return Titled("Employee Not Found", 
                      P(f"No record found for ID {id}. Try ID 1, 2, or 3."))

    # ML Prediction with a safety net for the version warning
    try:
        # 1. Create the input with the EXACT names the model expects (positive/negative events)
        model_input = pd.DataFrame([{
            'positive_events': details['total_pos'],
            'negative_events': details['total_neg']
        }])
        
        # 2. Use 'model_input' here (the names must match!)
        risk_prob = model.predict_proba(model_input)[0][1]

    except Exception as e:
        print(f"ML Model Bypass: {e}")
        risk_prob = 0.8 if details['net_score'] < 0 else 0.2

    return EmployeeDashboard(id, details['name'], details, risk_prob)

if __name__ == "__main__":
    serve()


@rt("/team/{name}")
def get(name: str):
    # 1. Fetch the specific risky employees for this team
    df = team_engine.get_team_risk_details(name)
    
    if df.empty:
        return Titled(f"Team: {name}", P("Great news! No high-risk employees found in this team."))

    # 2. Build table rows for the filtered list
    rows = []
    for _, r in df.iterrows():
        rows.append(Tr(
            Td(r['name']),
            Td(Span(str(r['net_score']), style="color: red; font-weight: bold")),
            Td(r['status']),
            Td(A("View Profile", href=f"/employee/{r['employee_id']}", cls="button small"))
        ))

    return Titled(f"Risk Analysis: {name}",
        Container(
            H3(f"Identifying {len(df)} Staff Members requiring attention"),
            Table(
                Thead(Tr(Th("Employee Name"), Th("Net Score"), Th("Alert Level"), Th("Action"))),
                Tbody(*rows)
            ),
            A("← Back to All Teams", href="/team", cls="button outline")
        )
    )