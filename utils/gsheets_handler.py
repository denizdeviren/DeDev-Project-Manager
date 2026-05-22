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
        # Debug helper: print available keys to help diagnose issues in logs
        print(f"DEBUG: Available keys in st.secrets: {list(st.secrets.keys())}")
        if "connections" in st.secrets:
            print(f"DEBUG: Available keys in connections: {list(st.secrets['connections'].keys())}")
            if "gsheets" in st.secrets["connections"]:
                print(f"DEBUG: Available keys in connections.gsheets: {list(st.secrets['connections']['gsheets'].keys())}")

        required_keys = ["spreadsheet", "type", "project_id", "private_key", "client_email"]

        # Check nested connections.gsheets
        if "connections" in st.secrets and "gsheets" in st.secrets["connections"]:
            cfg = st.secrets["connections"]["gsheets"]
            if all(key in cfg for key in required_keys):
                return True

        # Check flat root-level st.secrets
        if all(key in st.secrets for key in required_keys):
            return True

        # Also support st.secrets["gsheets"] directly
        if "gsheets" in st.secrets:
            cfg = st.secrets["gsheets"]
            if all(key in cfg for key in required_keys):
                return True

        return False
    except Exception as e:
        print(f"DEBUG: Error checking secrets config: {e}")
        return False

def get_gsheets_client():
    """Initializes and returns the gspread client."""
    required_keys = ["spreadsheet", "type", "project_id", "private_key", "client_email"]
    
    # 1. Try nested connections.gsheets
    if "connections" in st.secrets and "gsheets" in st.secrets["connections"]:
        cfg = st.secrets["connections"]["gsheets"]
        if all(key in cfg for key in required_keys):
            creds_dict = dict(cfg)
            spreadsheet_url = creds_dict.pop("spreadsheet", None)
            gc = gspread.service_account_from_dict(creds_dict)
            return gc, spreadsheet_url

    # 2. Try flat root-level st.secrets
    if all(key in st.secrets for key in required_keys):
        creds_dict = {key: st.secrets[key] for key in required_keys}
        # Include optional ones if present
        for key in ["private_key_id", "client_id", "auth_uri", "token_uri", "auth_provider_x509_cert_url", "client_x509_cert_url", "universe_domain"]:
            if key in st.secrets:
                creds_dict[key] = st.secrets[key]
        spreadsheet_url = creds_dict.pop("spreadsheet", None)
        gc = gspread.service_account_from_dict(creds_dict)
        return gc, spreadsheet_url

    # 3. Try st.secrets["gsheets"] directly
    if "gsheets" in st.secrets:
        cfg = st.secrets["gsheets"]
        if all(key in cfg for key in required_keys):
            creds_dict = dict(cfg)
            spreadsheet_url = creds_dict.pop("spreadsheet", None)
            gc = gspread.service_account_from_dict(creds_dict)
            return gc, spreadsheet_url
            
    raise ValueError("Google Sheets secrets are not fully configured in st.secrets")

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
        update_readable_ledger(sh, data.get("accounting_ledger", []))
        update_readable_bank_accounts(sh, data.get("bank_accounts", []))
        
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

def update_readable_ledger(sh, ledger):
    """Updates a user-friendly 'Muhasebe_Defteri' worksheet with general ledger details."""
    try:
        ws = get_worksheet(sh, "Muhasebe_Defteri", default_cols=12, default_rows=len(ledger) + 10)
        ws.clear()
        
        headers = [
            "İşlem ID", "Tarih", "Fiş No", "Açıklama", 
            "Borçlu Hesap (Debit)", "Alacaklı Hesap (Credit)", 
            "Net Tutar", "KDV Oranı (%)", "KDV Tutarı", "Genel Toplam", 
            "Tür", "Kayıt Yapan"
        ]
        
        rows = [headers]
        for tx in ledger:
            rows.append([
                tx.get("id", ""),
                tx.get("date", ""),
                tx.get("voucher_no", ""),
                tx.get("description", ""),
                tx.get("debit_account", ""),
                tx.get("credit_account", ""),
                float(tx.get("amount", 0.0)),
                int(tx.get("tax_rate", 0)),
                float(tx.get("tax_amount", 0.0)),
                float(tx.get("grand_total", 0.0)),
                tx.get("type", ""),
                tx.get("created_by", "")
            ])
            
        ws.update(range_name=f'A1:{chr(64 + len(headers))}{len(rows)}', values=rows)
    except Exception as e:
        print(f"Error updating readable ledger sheet: {e}")

def update_readable_bank_accounts(sh, bank_accounts):
    """Updates a user-friendly 'Hesap_Bakiyeleri' worksheet with bank details."""
    try:
        ws = get_worksheet(sh, "Hesap_Bakiyeleri", default_cols=4, default_rows=len(bank_accounts) + 10)
        ws.clear()
        
        headers = ["Hesap ID", "Hesap Adı", "Mevcut Bakiye", "Para Birimi"]
        
        rows = [headers]
        for acc in bank_accounts:
            rows.append([
                acc.get("id", ""),
                acc.get("name", ""),
                float(acc.get("balance", 0.0)),
                acc.get("currency", "TRY")
            ])
            
        ws.update(range_name=f'A1:{chr(64 + len(headers))}{len(rows)}', values=rows)
    except Exception as e:
        print(f"Error updating readable bank accounts sheet: {e}")
