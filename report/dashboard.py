import sys
import os
import pandas as pd
from pathlib import Path
from fasthtml.common import *

# 1. SETUP PATHS & IMPORTS
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT / "python-package"))

from report.combined_components.combined_component import DashboardPage
from report.utils import load_model, get_db_path
from employee_events.employee import Employee
from employee_events.team import Team

# 2. THE UI COMPONENT
class EmployeeDashboard(DashboardPage):
    def __init__(self, emp_id, emp_name, metrics, risk_prob, team_avg, emp_net):
        self.title = f"Performance: {emp_name}" 
        self.emp_id = emp_id
        self.emp_name = emp_name
        self.metrics = metrics
        self.risk_prob = risk_prob
        self.team_avg = team_avg
        self.emp_net = emp_net
        
    def __ft__(self):
        risk_color = "red" if self.risk_prob > 0.7 else "orange" if self.risk_prob > 0.4 else "green"
        total_ev = self.metrics.get('total_pos', 0) + self.metrics.get('total_neg', 0)
        perf_pct = (self.metrics.get('total_pos', 0) / total_ev * 100) if total_ev > 0 else 0

        return Container(
            Div(
                H2(f"Analysis: {self.emp_name}"),
                Grid(
                    # VISUAL 1
                    Div(H4("Turnover Risk"),
                        P(f"{self.risk_prob:.1%}", style=f"color:{risk_color}; font-size:2rem; font-weight:bold;"),
                        Progress(value=str(int(self.risk_prob * 100)), max="100", style=f"accent-color:{risk_color};")),
                    
                    # VISUAL 2
                    Div(H4("Performance Balance"),
                        P(f"Positive Ratio: {perf_pct:.1f}%"),
                        Progress(value=str(int(perf_pct)), max="100", style="accent-color:green;")),
                    
                    # VISUAL 3: Peer Comparison (FIXED SYNTAX HERE)
                    Div(H4("Peer Comparison"),
                        P(f"Total Score: {self.emp_net:.1f} vs Team Avg: {self.team_avg:.1f}"),
                        Progress(value=str(max(0, int(self.emp_net))), max="500", 
                                 style="display: block; width: 100%; height: 20px; accent-color: blue;"),
                        Progress(value=str(max(0, int(self.team_avg))), max="500", 
                                 style="display: block; width: 100%; height: 20px; accent-color: gray;"),
                        Small("Benchmark: Cumulative average across all recorded events."))
                ),
                Br(),
                Card(H5("Logic"), P("Live data from employee_events table.")),
                A("← Back to Dashboard", href="/", cls="button outline"),
                cls="card" 
            )
        )

# 3. INITIALIZATION
app, rt = fast_app(hdrs=(Link(rel="stylesheet", href="/static/report.css"),), live=True)

# Absolute Path Hardening
DB_PATH = ROOT / "python-package" / "employee_events" / "employee_events.db"
print(f"✅ SYSTEM ATTEMPTING DB CONNECTION: {DB_PATH}")

emp_engine = Employee(str(DB_PATH))
team_engine = Team(str(DB_PATH))
model = load_model()

# 4. ROUTES

@rt("/")
def get():
    # 1. Fetch the High-Level Benchmark
    try:
        avg_query = "SELECT AVG(total_net) FROM (SELECT SUM(positive_events - negative_events) as total_net FROM employee_events GROUP BY employee_id)"
        res = emp_engine.run_query(avg_query)
        global_avg = float(res.iloc[0, 0]) if res is not None and not res.empty else 0.0
    except:
        global_avg = 0.0

    # 2. Return the 4-Division Layout
    return Titled("Manager Command Center",
        Container(
            Div( # This Div holds our custom class instead of the Container
                # Row 1: CORE MANAGEMENT DIVISIONS
                Grid(
                    Card(H3("👥 Team Breakdown"),
                        P("View aggregate risk across all departments and identify low scores within teams."),
                        A("Open Team Audit", href="/team", cls="button"),
                        style="border-top: 5px solid #2ecc71;"),
                    Card(H3("👤 Individuals"),
                        P("Analyze specific employee performance, net scores, and turnover risk models."),
                        A("Examine Top Performer", href="/employee/1", cls="button outline"),
                        style="border-top: 5px solid #3498db;")
                ),
                Br(),
                # Row 2: DATA & NOTES DIVISIONS
                Grid(
                    Card(H3("📊 Benchmarks"),
                        P("Current Global Net Average:"),
                        H2(f"{global_avg:.1f}", style="color: #e67e22;"),
                        Progress(value=str(int(global_avg)), max="500", style="accent-color: #e67e22;"),
                        Small("Target performance threshold: 200.0")),
                    Card(H3("📝 Management Notes"),
                        Ul(
                            Li("Review 'Red' risk flags in Sales."),
                            Li("Update Q1 event logs by Friday."),
                            Li("Check individual peer comparisons.")
                        ),
                        style="background-color: #f9f9f9; font-size: 0.9rem;")
                ),
                cls="main-dashboard-wrapper" 
            )
        )
    )

@rt("/employee/{id}")
def get(id: int):
    details = emp_engine.get_employee_details(id)
    if not details: return Titled("Error", P("Employee not found."))
    
    try:
        avg_query = "SELECT AVG(total_net) FROM (SELECT SUM(positive_events - negative_events) as total_net FROM employee_events GROUP BY employee_id)"
        res = emp_engine.run_query(avg_query)
        team_avg = float(res.iloc[0, 0]) if res is not None and not res.empty else 0.0
    except:
        team_avg = 0.0

    emp_net = float(details.get('total_pos', 0) - details.get('total_neg', 0))
    
    try:
        inp = pd.DataFrame([{'positive_events': details.get('total_pos', 0), 'negative_events': details.get('total_neg', 0)}])
        prob = float(model.predict_proba(inp)[0][1])
    except: 
        prob = 0.5
    
    return EmployeeDashboard(id, details['name'], details, prob, team_avg, emp_net)

@rt("/team")
def get():
    # Fetch high-level summary
    df = team_engine.get_all_teams_risk_summary()
    if df.empty:
        return Titled("Team Audit", Container(P("No team data found.")))

    rows = []
    for _, r in df.iterrows():
        # Visual color logic: Red if there are risks, Green if safe
        risk_style = "color: red; font-weight: bold;" if r['risk_count'] > 0 else "color: green;"
        
        rows.append(Tr(
            Td(A(r['team_name'], href=f"/team/{r['team_name']}")), # Link to specific team
            Td(Span(str(r['risk_count']), style=risk_style)),     # Risk stats
            Td(str(r['total_employees'])),                        # Headcount
            Td(A("View Details", href=f"/team/{r['team_name']}", cls="button small outline"))
        ))
    
    return Titled("Department Risk Audit",
        Container(
            H3("Team Performance Summary"),
            Table(
                Thead(Tr(Th("Department"), Th("Risk Flags"), Th("Total Staff"), Th("Action"))),
                Tbody(*rows)
            ),
            A("← Back to Command Center", href="/", cls="button outline")
        )
    )

@rt("/team/{name}")
def get(name: str):
    # Fetch specific employees for this team
    df = team_engine.get_team_risk_details(name)
    
    if df.empty:
        return Titled(f"Team Analysis: {name}", 
                      Container(P("Great news! No high-risk employees found in this team."),
                                A("← Back to Audit", href="/team", cls="button outline")))

    rows = []
    for _, r in df.iterrows():
        rows.append(Tr(
            Td(r['name']),
            Td(Span(str(r['net_score']), style="color: red; font-weight: bold" if r['net_score'] < 100 else "")),
            Td(r['status']), # e.g., 'At Risk' or 'Watchlist'
            Td(A("View Profile", href=f"/employee/{r['employee_id']}", cls="button small"))
        ))

    return Titled(f"Risk Breakdown: {name}",
        Container(
            H3(f"Identifying {len(df)} Staff Members requiring attention"),
            Table(
                Thead(Tr(Th("Employee Name"), Th("Net Score"), Th("Alert Level"), Th("Action"))),
                Tbody(*rows)
            ),
            A("← Back to Team Audit", href="/team", cls="button outline")
        )
    )

if __name__ == "__main__": serve()