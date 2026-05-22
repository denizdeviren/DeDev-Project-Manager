import json
import os
import threading
from utils.gsheets_handler import is_gsheets_configured, push_to_sheets, pull_from_sheets

# Absolute path to data.json in the project root directory
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.normpath(os.path.join(os.path.dirname(CURRENT_DIR), "data.json"))

def migrate_dates_to_2026(data):
    # Migrate project dates
    for proj in data.get("projects", []):
        if "start_date" in proj and isinstance(proj["start_date"], str):
            proj["start_date"] = proj["start_date"].replace("2024-", "2026-").replace("2025-", "2026-")
        if "end_date" in proj and isinstance(proj["end_date"], str):
            proj["end_date"] = proj["end_date"].replace("2024-", "2026-").replace("2025-", "2026-")
        for ms in proj.get("milestones", []):
            if "date" in ms and isinstance(ms["date"], str):
                ms["date"] = ms["date"].replace("2024-", "2026-").replace("2025-", "2026-")
    
    # Migrate task dates
    for task in data.get("tasks", []):
        if "date" in task and isinstance(task["date"], str):
            task["date"] = task["date"].replace("2024-", "2026-").replace("2025-", "2026-")
            
    # Migrate time logs
    for log in data.get("time_logs", []):
        if "date" in log and isinstance(log["date"], str):
            log["date"] = log["date"].replace("2024-", "2026-").replace("2025-", "2026-")
            
    # Migrate activities
    for act in data.get("activities", []):
        if "date" in act and isinstance(act["date"], str):
            act["date"] = act["date"].replace("2024-", "2026-").replace("2025-", "2026-")
            
    # Migrate deployments
    for dep in data.get("deployments", []):
        if "last_deploy" in dep and isinstance(dep["last_deploy"], str):
            dep["last_deploy"] = dep["last_deploy"].replace("2024-", "2026-").replace("2025-", "2026-")
            
    return data

def init_defaults(data):
    from utils.encryption import hash_password
    
    if "accounts" not in data or not data["accounts"]:
        data["accounts"] = []
        
    # Find or update Deniz's account
    deniz_acc = next((acc for acc in data["accounts"] if acc.get("username") == "1denizdeviren" or acc.get("name") == "Deniz Deviren"), None)
    if deniz_acc:
        deniz_acc["username"] = "1denizdeviren"
        deniz_acc["name"] = "Deniz Deviren"
        deniz_acc.setdefault("role", "Solo Full-Stack Developer & AI Engineer")
        deniz_acc.setdefault("company", "DeDev")
        deniz_acc.setdefault("location", "Remote / Global")
        deniz_acc.setdefault("since", "2023")
        deniz_acc.setdefault("bio", "Tek kişilik ekip. Yapay zeka, web, mobil ve oyun geliştirme projeleri.")
        if "password_hash" not in deniz_acc:
            # Pre-hashed PBKDF2 credentials for safety
            deniz_acc["password_hash"] = "6a13b67f7ff4538333b55e6800d33ced0b897f9a75612319c3631b9e8ab67b13"
            deniz_acc["password_salt"] = "019769293f90510166382122020ef513"
            if "password" in deniz_acc:
                del deniz_acc["password"]
    else:
        # Pre-hashed PBKDF2 credentials for safety
        data["accounts"].append({
            "username": "1denizdeviren",
            "password_hash": "6a13b67f7ff4538333b55e6800d33ced0b897f9a75612319c3631b9e8ab67b13",
            "password_salt": "019769293f90510166382122020ef513",
            "name": "Deniz Deviren",
            "role": "Solo Full-Stack Developer & AI Engineer",
            "company": "DeDev",
            "location": "Remote / Global",
            "since": "2023",
            "bio": "Tek kişilik ekip. Yapay zeka, web, mobil ve oyun geliştirme projeleri."
        })

    # Find or update Furkan's account (M. Furkan Işık - Real Partner Account)
    furkan_acc = next((acc for acc in data["accounts"] if acc.get("username") == "furkan" or acc.get("name") in ["Furkan", "M. Furkan Işık"]), None)
    if furkan_acc:
        furkan_acc["username"] = "furkan"
        furkan_acc["name"] = "M. Furkan Işık"
        furkan_acc["role"] = "Co-Founder & Developer"
        furkan_acc["company"] = "DeDev"
        furkan_acc["location"] = "Remote / Global"
        furkan_acc["since"] = "2024"
        furkan_acc["bio"] = "M. Furkan Işık, DeDev ortağı ve yazılım geliştiricisi."
        if "password_hash" not in furkan_acc:
            h_val, s_val = hash_password("123456")
            furkan_acc["password_hash"] = h_val
            furkan_acc["password_salt"] = s_val
            if "password" in furkan_acc:
                del furkan_acc["password"]
    else:
        h_val, s_val = hash_password("123456")
        data["accounts"].append({
            "username": "furkan",
            "password_hash": h_val,
            "password_salt": s_val,
            "name": "M. Furkan Işık",
            "role": "Co-Founder & Developer",
            "company": "DeDev",
            "location": "Remote / Global",
            "since": "2024",
            "bio": "M. Furkan Işık, DeDev ortağı ve yazılım geliştiricisi."
        })

    # Keep only primary accounts, completely removing demo_erpsim or others from the production database
    data["accounts"] = [acc for acc in data["accounts"] if acc.get("username") in ["1denizdeviren", "furkan"]]
        
    # Auto-migrate any other legacy accounts loaded from database
    for acc in data.get("accounts", []):
        if "password" in acc and "password_hash" not in acc:
            h_val, s_val = hash_password(str(acc["password"]))
            acc["password_hash"] = h_val
            acc["password_salt"] = s_val
            del acc["password"]
        
    if "active_owner" not in data:
        data["active_owner"] = "Deniz Deviren"
        
    # Initialize basic keys
    data.setdefault("projects", [])
    data.setdefault("tasks", [])
    data.setdefault("notes", [])
    data.setdefault("time_logs", [])
    data.setdefault("finances", [])
    data.setdefault("deployments", [])
    data.setdefault("activities", [])
    data.setdefault("team", [])
    # Filter out mock team members from Deniz's production database
    data["team"] = [m for m in data["team"] if m.get("name") not in ["Ahmet Yılmaz", "Elif Demir"]]
    
    # Initialize empty lists for bank accounts and ledger to let user define them
    data.setdefault("bank_accounts", [])
    data.setdefault("accounting_ledger", [])
        
    # Initialize departments
    if "departments" not in data or not data["departments"]:
        data["departments"] = [
            {"id": "DEP-YAZILIM", "name": "Yazılım Geliştirme", "description": "Web, mobil ve backend geliştirme süreçleri.", "color": "#3b82f6", "icon": "💻"},
            {"id": "DEP-AI", "name": "Yapay Zeka & Veri Bilimi", "description": "Makine öğrenimi modelleri, LLM entegrasyonları.", "color": "#8b5cf6", "icon": "🧠"},
            {"id": "DEP-TASARIM", "name": "Tasarım & UI/UX", "description": "Arayüz tasarımı, grafikler ve marka kimliği.", "color": "#ec4899", "icon": "🎨"},
            {"id": "DEP-PAZARLAMA", "name": "Pazarlama & Satış", "description": "Müşteri ilişkileri ve ürün tanıtımları.", "color": "#f59e0b", "icon": "📈"},
            {"id": "DEP-YONETIM", "name": "Yönetim", "description": "Stratejik yönetim ve karar alma süreçleri.", "color": "#ef4444", "icon": "👑"}
        ]
        
    # Set default department and unique ID for existing team members if not present
    import uuid
    for member in data.setdefault("team", []):
        if "department" not in member:
            member["department"] = "Yazılım Geliştirme"
        if "id" not in member:
            if member.get("name") == "Ahmet Yılmaz":
                member["id"] = "USR-AHMET"
            elif member.get("name") == "Elif Demir":
                member["id"] = "USR-ELIF"
            elif member.get("name") == "M. Furkan Işık":
                member["id"] = "USR-FURKAN"
            else:
                member["id"] = f"USR-{str(uuid.uuid4())[:6].upper()}"
            
    # Migrate legacy "Furkan" owner_name / assignee to "M. Furkan Işık"
    if data.get("active_owner") == "Furkan":
        data["active_owner"] = "M. Furkan Işık"
    for proj in data.setdefault("projects", []):
        if proj.get("owner_name") == "Furkan":
            proj["owner_name"] = "M. Furkan Işık"
    for task in data.setdefault("tasks", []):
        if task.get("assignee") == "Furkan":
            task["assignee"] = "M. Furkan Işık"

    return data

def init_demo_defaults(data):
    from utils.encryption import hash_password
    
    # 1. Accounts
    data["accounts"] = []
    h_val, s_salt = hash_password("demo123")
    data["accounts"].append({
        "username": "demo_erpsim",
        "password_hash": h_val,
        "password_salt": s_salt,
        "name": "Örnek Simülasyon",
        "role": "Kurumsal Admin & Test Sorumlusu",
        "company": "DeDev Kurumsal",
        "location": "İstanbul, Türkiye",
        "since": "2026",
        "bio": "ERP Sistemi test ve simülasyon yönetici hesabı. Tam yetkilidir.",
        "role_type": "admin"
    })
    
    data["active_owner"] = "Örnek Simülasyon"
    
    # 2. Team
    data["team"] = [
        {"id": "USR-METEHAN", "name": "Metehan Şahin", "role": "Senior Developer", "department": "Yazılım Geliştirme", "email": "metehan@dedev.com"},
        {"id": "USR-SELIN", "name": "Selin Kaya", "role": "UI/UX Tasarımcı", "department": "Tasarım & UI/UX", "email": "selin@dedev.com"},
        {"id": "USR-ALPEREN", "name": "Alperen Yılmaz", "role": "Mali Müşavir", "department": "Yönetim", "email": "alperen@dedev.com"}
    ]
    
    # 3. Projects
    data["projects"] = [
        {
            "id": "PROJ-DEMO-1",
            "name": "DeDev Kurumsal ERP Uygulaması",
            "category": "Kurumsal Sistem",
            "status": "In Progress",
            "priority": "High",
            "start_date": "2026-05-10",
            "end_date": "2026-08-20",
            "budget": 250000.0,
            "lines_of_code": 34500,
            "description": "Örnek simülasyon kullanıcısı için geniş kapsamlı modüllerin, Kanban panosunun ve maliyet analizlerinin sergilendiği ana proje.",
            "tech_stack": ["Python", "Streamlit", "Plotly", "PostgreSQL"],
            "owner_name": "Örnek Simülasyon",
            "milestones": [
                {"id": "MS-DEMO-1", "name": "Veritabanı Şeması Tasarımı", "date": "2026-05-20", "status": "Completed"},
                {"id": "MS-DEMO-2", "name": "Muhasebe Modülü Entegrasyonu", "date": "2026-06-15", "status": "Pending"}
            ]
        },
        {
            "id": "PROJ-DEMO-2",
            "name": "Müşteri Portalı Mobil Uygulaması",
            "category": "Mobil Uygulama",
            "status": "In Progress",
            "priority": "Medium",
            "start_date": "2026-05-15",
            "end_date": "2026-07-30",
            "budget": 95000.0,
            "lines_of_code": 18200,
            "description": "Müşterilerin siparişlerini takip edip faturalarını görüntüleyebileceği mobil ara yüz geliştirme süreci.",
            "tech_stack": ["Flutter", "Dart", "Firebase"],
            "owner_name": "Örnek Simülasyon",
            "milestones": [
                {"id": "MS-DEMO-3", "name": "Tasarım Onayı", "date": "2026-05-28", "status": "Pending"}
            ]
        }
    ]
    
    # 4. Tasks
    data["tasks"] = [
        {
            "id": "TASK-DEMO-1",
            "title": "Finansal verileri incele ve mizan raporu al",
            "status": "Done",
            "priority": "High",
            "date": "2026-05-15",
            "project_id": "PROJ-DEMO-1",
            "assignee": "Alperen Yılmaz",
            "effort": 2
        },
        {
            "id": "TASK-DEMO-2",
            "title": "Kanban panosunda sürükle-bırak testlerini tamamla",
            "status": "In Progress",
            "priority": "Medium",
            "date": "2026-05-28",
            "project_id": "PROJ-DEMO-1",
            "assignee": "Metehan Şahin",
            "effort": 4
        },
        {
            "id": "TASK-DEMO-3",
            "title": "Mobil arayüz login sayfasını tasarla",
            "status": "In Progress",
            "priority": "High",
            "date": "2026-05-26",
            "project_id": "PROJ-DEMO-2",
            "assignee": "Selin Kaya",
            "effort": 5
        },
        {
            "id": "TASK-DEMO-4",
            "title": "Double-entry muhasebe test faturalarını oluştur",
            "status": "Done",
            "priority": "Medium",
            "date": "2026-05-22",
            "project_id": "PROJ-DEMO-1",
            "assignee": "Örnek Simülasyon",
            "effort": 3
        }
    ]
    
    # 5. Time Logs
    data["time_logs"] = [
        {
            "date": "2026-05-22",
            "project_id": "PROJ-DEMO-1",
            "task_title": "Finansal verileri incele ve mizan raporu al",
            "duration": 4.0,
            "effort_level": "Orta",
            "description": "Double-entry ledger test edildi ve mizan raporu doğrulandı."
        },
        {
            "date": "2026-05-22",
            "project_id": "PROJ-DEMO-2",
            "task_title": "Mobil arayüz login sayfasını tasarla",
            "duration": 3.5,
            "effort_level": "Yüksek",
            "description": "Figma tasarımları Flutter widget'larına dönüştürülüyor."
        }
    ]
    
    # 6. Finances
    data["finances"] = [
        {
            "id": "FIN-DEMO-1",
            "project_id": "PROJ-DEMO-1",
            "type": "Gelir",
            "category": "Yazılım Satış",
            "amount": 125000.0,
            "date": "2026-05-12",
            "description": "Birinci faz hak ediş ödemesi tahsil edildi."
        },
        {
            "id": "FIN-DEMO-2",
            "project_id": "PROJ-DEMO-2",
            "type": "Gider",
            "category": "Pazarlama / Reklam",
            "amount": 5000.0,
            "date": "2026-05-20",
            "description": "Sosyal medya lansman bütçesi."
        }
    ]
    
    # 7. Bank Accounts
    data["bank_accounts"] = [
        {"id": "ACC-DEMO-1", "name": "Akbank Ticari", "balance": 125000.0, "currency": "TRY"},
        {"id": "ACC-DEMO-2", "name": "Nakit Kasa", "balance": 15000.0, "currency": "TRY"},
        {"id": "ACC-DEMO-3", "name": "Garanti USD", "balance": 12000.0, "currency": "USD"}
    ]
    
    # 8. Accounting Ledger
    data["accounting_ledger"] = [
        {
            "id": "TX-DEMO-INIT-01",
            "date": "2026-05-10",
            "voucher_no": "FIŞ-20260510-001",
            "description": "Akbank Ticari Sermaye Açılışı",
            "debit_account": "Akbank Ticari",
            "credit_account": "Özkaynaklar / Sermaye",
            "amount": 125000.0,
            "tax_rate": 0,
            "tax_amount": 0.0,
            "grand_total": 125000.0,
            "type": "Açılış",
            "project_id": None,
            "created_by": "demo_erpsim",
            "is_correction": False,
            "corrected_tx_id": None,
            "is_corrected": False
        },
        {
            "id": "TX-DEMO-INIT-02",
            "date": "2026-05-10",
            "voucher_no": "FIŞ-20260510-002",
            "description": "Nakit Kasa Sermaye Açılışı",
            "debit_account": "Nakit Kasa",
            "credit_account": "Özkaynaklar / Sermaye",
            "amount": 15000.0,
            "tax_rate": 0,
            "tax_amount": 0.0,
            "grand_total": 15000.0,
            "type": "Açılış",
            "project_id": None,
            "created_by": "demo_erpsim",
            "is_correction": False,
            "corrected_tx_id": None,
            "is_corrected": False
        },
        {
            "id": "TX-DEMO-INIT-03",
            "date": "2026-05-10",
            "voucher_no": "FIŞ-20260510-003",
            "description": "Garanti USD Sermaye Açılışı",
            "debit_account": "Garanti USD",
            "credit_account": "Özkaynaklar / Sermaye",
            "amount": 12000.0,
            "tax_rate": 0,
            "tax_amount": 0.0,
            "grand_total": 12000.0,
            "type": "Açılış",
            "project_id": None,
            "created_by": "demo_erpsim",
            "is_correction": False,
            "corrected_tx_id": None,
            "is_corrected": False
        },
        {
            "id": "TX-DEMO-TX-01",
            "date": "2026-05-12",
            "voucher_no": "FAT-20260512-001",
            "description": "DeDev Kurumsal ERP 1. Faz Fatura Tahsilatı",
            "debit_account": "Akbank Ticari",
            "credit_account": "Yurtiçi Satışlar (Gelir)",
            "amount": 125000.0,
            "tax_rate": 20,
            "tax_amount": 25000.0,
            "grand_total": 150000.0,
            "type": "Tahsilat",
            "project_id": "PROJ-DEMO-1",
            "created_by": "demo_erpsim",
            "is_correction": False,
            "corrected_tx_id": None,
            "is_corrected": False
        }
    ]
    
    data.setdefault("deployments", [])
    data.setdefault("activities", [])
    data.setdefault("notes", [])
    
    data["departments"] = [
        {"id": "DEP-YAZILIM", "name": "Yazılım Geliştirme", "description": "Web, mobil ve backend geliştirme süreçleri.", "color": "#3b82f6", "icon": "💻"},
        {"id": "DEP-AI", "name": "Yapay Zeka & Veri Bilimi", "description": "Makine öğrenimi modelleri, LLM entegrasyonları.", "color": "#8b5cf6", "icon": "🧠"},
        {"id": "DEP-TASARIM", "name": "Tasarım & UI/UX", "description": "Arayüz tasarımı, grafikler ve marka kimliği.", "color": "#ec4899", "icon": "🎨"},
        {"id": "DEP-PAZARLAMA", "name": "Pazarlama & Satış", "description": "Müşteri ilişkileri ve ürün tanıtımları.", "color": "#f59e0b", "icon": "📈"},
        {"id": "DEP-YONETIM", "name": "Yönetim", "description": "Stratejik yönetim ve karar alma süreçleri.", "color": "#ef4444", "icon": "👑"}
    ]
    
    return data

def get_data_file_path():
    try:
        import streamlit as st
        if st.session_state.get("logged_in_user") == "demo_erpsim":
            return os.path.normpath(os.path.join(os.path.dirname(CURRENT_DIR), "data_demo.json"))
    except Exception:
        pass
    return DATA_FILE

def get_all_accounts():
    accounts = []
    # Read production data.json accounts
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            prod_data = json.load(f)
            accounts.extend(prod_data.get("accounts", []))
    except Exception:
        pass
        
    # Read/Initialize demo data_demo.json accounts
    demo_path = os.path.normpath(os.path.join(os.path.dirname(CURRENT_DIR), "data_demo.json"))
    if not os.path.exists(demo_path):
        try:
            demo_data = {"projects": [], "tasks": [], "notes": [], "time_logs": [], "finances": [], "deployments": [], "activities": []}
            demo_data = init_demo_defaults(demo_data)
            with open(demo_path, "w", encoding="utf-8") as f:
                json.dump(demo_data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
            
    try:
        with open(demo_path, "r", encoding="utf-8") as f:
            demo_data = json.load(f)
            accounts.extend(demo_data.get("accounts", []))
    except Exception:
        pass
        
    seen = set()
    dedup_accounts = []
    for acc in accounts:
        uname = acc.get("username")
        if uname and uname not in seen:
            seen.add(uname)
            dedup_accounts.append(acc)
            
    return dedup_accounts

def get_filtered_elements(data):
    active_owner = data.get("active_owner", "Deniz Deviren")
    
    projects = [p for p in data.get("projects", []) if p.get("owner_name", "Deniz Deviren") == active_owner]
    project_ids = {p["id"] for p in projects}
    
    tasks = [t for t in data.get("tasks", []) if t.get("project_id") in project_ids]
    time_logs = [log for log in data.get("time_logs", []) if log.get("project_id") in project_ids]
    finances = [f for f in data.get("finances", []) if not f.get("project_id") or f.get("project_id") in project_ids]
    activities = [a for a in data.get("activities", []) if not a.get("project") or a.get("project") in project_ids]
    deployments = [d for d in data.get("deployments", []) if d.get("project") in project_ids]
    
    return active_owner, projects, tasks, time_logs, finances, activities, deployments

def load_data():
    filepath = get_data_file_path()
    is_demo = (os.path.basename(filepath) == "data_demo.json")
    
    if not os.path.exists(filepath):
        if is_demo:
            default_data = {"projects": [], "tasks": [], "notes": [], "time_logs": [], "finances": [], "deployments": [], "activities": []}
            default_data = init_demo_defaults(default_data)
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(default_data, f, ensure_ascii=False, indent=2)
            return default_data
            
        if is_gsheets_configured():
            data, msg = pull_from_sheets()
            if data:
                try:
                    data = init_defaults(data)
                    data = migrate_dates_to_2026(data)
                    with open(filepath, "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    return data
                except Exception:
                    return data
        
        default_data = {"projects": [], "tasks": [], "notes": [], "time_logs": [], "finances": [], "deployments": [], "activities": []}
        default_data = init_defaults(default_data)
        return default_data
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        initial_data_str = json.dumps(data)
        if is_demo:
            data = init_demo_defaults(data)
        else:
            data = init_defaults(data)
        data = migrate_dates_to_2026(data)
        
        if json.dumps(data) != initial_data_str:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
        return data
    except Exception:
        default_data = {"projects": [], "tasks": [], "notes": [], "time_logs": [], "finances": [], "deployments": [], "activities": []}
        if is_demo:
            default_data = init_demo_defaults(default_data)
        else:
            default_data = init_defaults(default_data)
        return default_data

def save_data(data):
    filepath = get_data_file_path()
    is_demo = (os.path.basename(filepath) == "data_demo.json")
    
    try:
        from utils.automations import run_automations
        run_automations(data)
    except Exception:
        pass

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    if not is_demo and is_gsheets_configured():
        threading.Thread(target=push_to_sheets, args=(data,), daemon=True).start()

colors_map = {
    "Washington Emlak AI": "#667eea",
    "ComTerms DeDe AI": "#f59e0b", 
    "DeDev FPS: Shadow Ops": "#ef4444",
    "DeDev Project Manager": "#22c55e"
}


