from fasthtml.common import *

class DashboardPage:
    """
    The base layout for all pages in your dashboard.
    Subclass this in dashboard.py to customize your content.
    """
    def __init__(self, title="Manager Dashboard"):
        self.title = title

    def __ft__(self):
        # __ft__ allows FastHTML to render this class as a component
        return Title(self.title), Main(
            Header(H1(self.title), cls="container"),
            Div(cls="container")(self.render_content()),
            cls="container"
        )

    def render_content(self):
        # Placeholder to be overridden by subclasses
        return P("Welcome to the performance monitoring system.")

class Sidebar:
    """
    A reusable navigation component for the left-hand side.
    """
    def __ft__(self):
        return Nav(
            Ul(
                Li(A("🏠 Home", href="/")),
                Li(A("👥 Team View", href="/team")),
                Li(A("👤 Alex Martinez (ID: 1)", href="/employee/1")),
            ),
            cls="sidebar"
        )

class PerformanceChart:
    """
    A visual component that displays employee metrics.
    """
    def __init__(self, df):
        self.df = df

    def __ft__(self):
        # We can use standard HTML elements to represent the chart summary
        score = self.df.net_score.iloc[0]
        return Div(
            H3("Performance Summary"),
            Table(
                Tr(Th("Metric"), Th("Value")),
                Tr(Td("Positive Events"), Td(str(self.df.total_pos.iloc[0]))),
                Tr(Td("Negative Events"), Td(str(self.df.total_neg.iloc[0]))),
                Tr(Td("Net Score"), Td(B(str(score)), cls="text-primary"))
            ),
            cls="card"
        )