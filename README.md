# ⚙️ Udacity Data Science Software Engineering Project

### Project Status: ✅ COMPLETE & VERIFIED

This repository contains a professional-grade software engineering project focused on HR Analytics, built for the Udacity Data Science Nanodegree. It features a modular Python package, a web-based dashboard, and automated CI/CD testing.

The Engineering Perspective: From a Data Scientist's perspective, the primary highlight of this project was transitioning from exploratory notebooks to production-ready modular Python code. The architecture intentionally utilizes Inheritance, Mixins, and Polymorphism to create a scalable system for database querying and employee data modeling.

---

## 1. 🎯 Project Goal & Business Context

**The Problem:** Managers need a way to quantify employee performance and predict "Flight Risk" without sifting through thousands of raw interaction logs.

**The Solution:** This project implements an Object-Oriented HR engine that:

    * Calculates Performance: Aggregates positive and negative workplace events into a "Net Score".

    * Predicts Turnover Risk: Uses a Machine Learning model to determine the likelihood an employee is looking for a new role based on behavior patterns.

    * Visualizes Insights: Provides a FastHTML dashboard with real-time data visualizations.

---

## 2. 🚀 Setup and Installation

This project is built and managed using Git, Python, and a virtual environment.

Code is run via **python -m report.dashboard**

### Prerequisites

You must have Git and Python installed.

### Installation Steps

1.  **Clone the Repository:**
    ```gitbash
    git clone [https://github.com/adamskirees/Udacity-DS-Software-Engineering.git](https://github.com/adamskirees/Udacity-DS-Software-Engineering.git)
    cd Udacity-DS-Software-Engineering
    ```

2.  **Create and Activate Virtual Environment (Bash):**
    ```gitbash
    python -m venv venv
    source venv/bin/activate
    

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    pip install -e ./python-package
    ```
4.  **Launch the Dashboard:**
    ```bash
    python -m report.dashboard

    OR 
    uvicorn report.dashboard:app --host 127.0.0.1 --port 5001 --reload

    open http://localhost:5000 in your browswer



---

## 3. 📁 Repository Structure (The Engineering View)

The project follows a modular, engineering-first directory structure:

Folder    / FilePurpose.
github/workflows/          CI/CD: Automated tests that run on every push via GitHub Actions.
python-package/            CORE LOGIC: The employee_events library. Includes setup.py and modular OOP classes.
report/                    DASHBOARD: FastHTML application and visualization components.assets/MODELS/DB: Contains the SQLite database and the serialized ML model (.pkl).
requirements.txt           DEPENDENCIES: Exact package versions for environment reproducibility.

---

## 4. 🧬 Engineering Highlights
Object-Oriented Design: Uses Inheritance and Mixins to handle database connections efficiently across Employee and Team classes.

Data Visualizations: Includes custom-built Progress Bar visualizations for Turnover Risk and Performance Balance.

Automated Testing: Integrated with GitHub Actions to verify package imports and logic stability on every commit.


---

## 5. 🔗 Links

* **Is not a live hosted dashboard at present - github link only** 
