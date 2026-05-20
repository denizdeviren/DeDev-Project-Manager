import json
import streamlit as st
import gspread
from datetime import datetime

# Worksheet names
BACKUP_SHEET_NAME = "__json_db__"
READABLE_PROJECTS_SHEET = "Projeler"
READABLE_TASKS_SHEET = "Görevler"

def is_gsheets_configured():
    """Checks if Google Sheets connection is fully configured in secrets."""
    try:
        if "connections" not in st.secrets:
            return False
        if "gsheets" not in st.secrets["connections"]:
            return False
        
        cfg = st.secrets["connections"]["gsheets"]
        required_keys = ["spreadsheet", "type", "project_id", "private_key", "client_email"]
        return all(key in cfg for key in required_keys)
    except Exception:
        return False

def get_gsheets_client():
    """Initializes and returns the gspread client."""
    if not is_gsheets_configured():
        raise ValueError("Google Sheets secrets are not fully configured in .streamlit/secrets.toml")
    
    # Extract credentials from Streamlit secrets
    creds_dict = dict(st.secrets["connections"]["gsheets"])
    
    # Extract spreadsheet URL/ID (it's not part of service account JSON)
    spreadsheet_url = creds_dict.pop("spreadsheet", None)
    
    # Authenticate using the service account dict
    gc = gspread.service_account_from_dict(creds_dict)
    return gc, spreadsheet_url

def get_worksheet(sh, name, default_cols=10, default_rows=100):
    """Gets a worksheet by name, creating it if it doesn't exist."""
    try:
        return sh.worksheet(name)
    except gspread.exceptions.WorksheetNotFound:
        return sh.add_worksheet(title=name, rows=default_rows, cols=default_cols)

def push_to_sheets(data):
    """
    Saves the entire JSON payload to the Google Sheet backup worksheet,
    and updates user-readable tabs for Projects and Tasks.
    """
    try:
        if not is_gsheets_configured():
            return False, "Google Sheets is not configured."
        
        gc, spreadsheet_url = get_gsheets_client()
        sh = gc.open_by_url(spreadsheet_url)
        
        # 1. Update the JSON database backup tab
        json_backup_ws = get_worksheet(sh, BACKUP_SHEET_NAME, default_cols=2, default_rows=10)
        
        # Serialize the entire dictionary
        serialized_data = json.dumps(data, ensure_ascii=False, indent=2)
        
        # Write metadata & JSON payload
        json_backup_ws.update(range_name='A1:B2', values=[
            ["Last Sync Timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            ["JSON_DATA", serialized_data]
        ])
        
        # 2. Update Human-Readable Sheets (Best-effort, don't crash if they fail)
        update_readable_projects(sh, data.get("projects", []))
        update_readable_tasks(sh, data.get("tasks", []))
        
        return True, "Successfully synchronized with Google Sheets."
    except Exception as e:
        return False, f"Google Sheets Sync Error: {str(e)}"

def pull_from_sheets():
    """
    Pulls the entire database dictionary from the Google Sheet backup worksheet.
    """
    try:
        if not is_gsheets_configured():
            return None, "Google Sheets is not configured."
        
        gc, spreadsheet_url = get_gsheets_client()
        sh = gc.open_by_url(spreadsheet_url)
        
        # Access the JSON backup tab
        json_backup_ws = get_worksheet(sh, BACKUP_SHEET_NAME, default_cols=2, default_rows=10)
        
        # Get A2 which contains the JSON_DATA payload
        cell_val = json_backup_ws.acell('B2').value
        if not cell_val:
            return None, "Worksheet is empty or JSON payload cell not found."
            
        data = json.loads(cell_val)
        return data, "Successfully pulled data from Google Sheets."
    except Exception as e:
        return None, f"Failed to pull from Google Sheets: {str(e)}"

def update_readable_projects(sh, projects):
    """Updates a user-friendly 'Projeler' worksheet with flat project details."""
    try:
        ws = get_worksheet(sh, READABLE_PROJECTS_SHEET, default_cols=12, default_rows=len(projects) + 10)
        ws.clear()
        
        headers = [
            "Proje ID", "Proje Adı", "Kategori", "Açıklama", 
            "Durum", "İlerleme (%)", "Öncelik", "Başlangıç Tarihi", 
            "Bitiş Tarihi", "Kod Satırı", "Commit Sayısı", "Gizli Proje mi?"
        ]
        
        rows = [headers]
        for p in projects:
            rows.append([
                p.get("id", ""),
                p.get("name", ""),
                p.get("category", ""),
                p.get("description", "") if not p.get("is_secret") else "🔒 [ŞİFRELİ - GİZLİ KASA]",
                p.get("status", ""),
                p.get("progress", 0),
                p.get("priority", ""),
                p.get("start_date", ""),
                p.get("end_date", ""),
                p.get("lines_of_code", 0),
                p.get("commits", 0),
                "Evet" if p.get("is_secret", False) else "Hayır"
            ])
            
        ws.update(range_name=f'A1:{chr(64 + len(headers))}{len(rows)}', values=rows)
    except Exception as e:
        # Silently log errors for secondary views
        print(f"Error updating readable projects sheet: {e}")

def update_readable_tasks(sh, tasks):
    """Updates a user-friendly 'Görevler' worksheet with flat task details."""
    try:
        ws = get_worksheet(sh, READABLE_TASKS_SHEET, default_cols=8, default_rows=len(tasks) + 10)
        ws.clear()
        
        headers = ["Görev ID", "Başlık", "Proje ID", "Durum", "Öncelik", "Atanan", "Bitiş Tarihi", "Açıklama"]
        
        rows = [headers]
        for t in tasks:
            rows.append([
                t.get("id", ""),
                t.get("title", ""),
                t.get("project", ""),
                t.get("status", ""),
                t.get("priority", ""),
                t.get("assignee", ""),
                t.get("due_date", ""),
                t.get("description", "")
            ])
            
        ws.update(range_name=f'A1:{chr(64 + len(headers))}{len(rows)}', values=rows)
    except Exception as e:
        # Silently log errors for secondary views
        print(f"Error updating readable tasks sheet: {e}")
