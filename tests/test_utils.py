from report.utils import load_model, get_db_path
import os

def test_setup():
    print("--- 🔍 STARTING UTILS TEST ---")
    
    # 1. Test Database Path
    db_path = get_db_path()
    print(f"📂 DB Path calculated as: {db_path}")
    if os.path.exists(db_path):
        print("✅ Success: Database file found!")
    else:
        print("❌ Error: Database file NOT found at that path.")

    # 2. Test Model Loading
    try:
        model = load_model()
        print(f"🧠 Model loaded successfully! Type: {type(model)}")
        print("✅ Success: model.pkl is valid.")
    except Exception as e:
        print(f"❌ Error: Could not load model. Details: {e}")

if __name__ == "__main__":
    test_setup()