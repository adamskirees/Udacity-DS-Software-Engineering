import pickle
from pathlib import Path

# To help with mapping the folder strucutre, so the important files work no matter where we run them from !! 
# 1. Get the path of utils.py (E:\...\Udacity-DS-Software-Engineering\report\utils.py)
# 2. .parent goes to 'report'
# 3. .parent.parent goes to the ROOT 'Udacity-DS-Software-Engineering'
ROOT_DIR = Path(__file__).resolve().parent.parent

# Define the absolute paths to your assets
DB_PATH = ROOT_DIR / "python-package" / "employee_events" / "employee_events.db"
MODEL_PATH = ROOT_DIR / "assets" / "model.pkl"

def load_model():
    """Loads the ML model from the assets folder."""
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Could not find model at {MODEL_PATH}")
        
    with open(MODEL_PATH, 'rb') as file:
        return pickle.load(file)

def get_db_path():
    """Returns the absolute path to the database."""
    return str(DB_PATH)