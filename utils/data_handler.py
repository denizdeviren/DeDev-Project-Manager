import json
import os
import threading
from utils.gsheets_handler import is_gsheets_configured, push_to_sheets, pull_from_sheets

# Absolute path to data.json in the project root directory
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.normpath(os.path.join(os.path.dirname(CURRENT_DIR), "data.json"))

def load_data():
    # If local file does not exist, try to pull from Google Sheets first (critical for Streamlit Cloud)
    if not os.path.exists(DATA_FILE):
        if is_gsheets_configured():
            data, msg = pull_from_sheets()
            if data:
                try:
                    with open(DATA_FILE, "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    return data
                except Exception:
                    return data
        
        return {"projects": [], "tasks": [], "notes": [], "time_logs": [], "finances": [], "deployments": [], "activities": []}
    
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"projects": [], "tasks": [], "notes": [], "time_logs": [], "finances": [], "deployments": [], "activities": []}

def save_data(data):
    # Run smart automations in-place
    try:
        from utils.automations import run_automations
        run_automations(data)
    except Exception:
        pass

    # Save locally first
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # Save to Google Sheets in background thread if configured
    if is_gsheets_configured():
        threading.Thread(target=push_to_sheets, args=(data,), daemon=True).start()

colors_map = {
    "Washington Emlak AI": "#667eea",
    "ComTerms DeDe AI": "#f59e0b", 
    "DeDev FPS: Shadow Ops": "#ef4444",
    "DeDev Project Manager": "#22c55e"
}

