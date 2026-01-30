# ⚙️ Udacity Data Science Software Engineering Project

### Project Status: CURRENTLY WORKING

This project is the second practical project in Udacitys new Data science nanodegree. 

---

## 1. 🎯 Project Goal & Business Context

**Goal:** To build and test a robust Python package (`src/`) capable of performing statistical calculations on a dataset, wrapped in a professional project structure. The focus is on **maintainability** and **reproducibility** rather than complex modeling.

We are looking at employee performance, specifically, high-performing employees. The dashboard will show a final measure of employee performance and productivity and help determin if this employee may be a flight risk (AKA - looking for another job). 

**Value Proposition:** This repository showcases the ability to move beyond Jupyter Notebooks by implementing modular, testable, and reusable Python code. This ensures stable data pipelines in production environments.

---

## 2. 🚀 Setup and Installation

This project is built and managed using Git, Python 3.8+, and a virtual environment.

### Prerequisites

You must have Git and Python installed.

### Installation Steps

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/adamskirees/Udacity-DS-Software-Engineering.git](https://github.com/adamskirees/Udacity-DS-Software-Engineering.git)
    cd Udacity-DS-Software-Engineering
    ```

2.  **Create and Activate Virtual Environment (Bash):**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

---

## 3. 📁 Repository Structure (The Engineering View)

The project adheres to a standard, modular structure:

| Folder | Purpose |
| :--- | :--- |
| **`src/`** | **SOURCE CODE:** Contains the production-ready, modular Python functions (e.g., `utils.py`, `calculator.py`). This code is unit tested. |
| **`notebooks/`**| **ANALYSIS:** Contains exploratory data analysis (EDA) and demonstration notebooks (`.ipynb`) used to call the functions in `src/`. |
| **`data/`** | **DATA:** Contains raw and processed data files (under 50MB). Large files are tracked via Git LFS. |
| **`venv/`** | **ENVIRONMENT:** The isolated Python virtual environment (ignored by Git). |
| **`requirements.txt`**| **DEPENDENCIES:** Lists all required Python packages and versions for environment setup. |

---

## 4. 🧪 Testing and CI

* **Testing Framework:** Unit tests are written using Python's built-in `unittest` module.
* **Running Tests:** Execute the following command from the project root:
    ```bash
    python -m unittest discover tests
    ```
* **Continuous Integration (CI):** *(Add this section once you implement a CI tool like GitHub Actions.)*

---

## 5. 🔗 Links

* **Final Report/Demo Notebook:** 
