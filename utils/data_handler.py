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
            h_val, s_val = hash_password("104691")
            deniz_acc["password_hash"] = h_val
            deniz_acc["password_salt"] = s_val
            if "password" in deniz_acc:
                del deniz_acc["password"]
    else:
        h_val, s_val = hash_password("104691")
        data["accounts"].append({
            "username": "1denizdeviren",
            "password_hash": h_val,
            "password_salt": s_val,
            "name": "Deniz Deviren",
            "role": "Solo Full-Stack Developer & AI Engineer",
            "company": "DeDev",
            "location": "Remote / Global",
            "since": "2023",
            "bio": "Tek kişilik ekip. Yapay zeka, web, mobil ve oyun geliştirme projeleri."
        })

    # Find or update Furkan's account
    furkan_acc = next((acc for acc in data["accounts"] if acc.get("username") == "furkan" or acc.get("name") == "Furkan"), None)
    if furkan_acc:
        furkan_acc["username"] = "furkan"
        furkan_acc["name"] = "Furkan"
        furkan_acc.setdefault("role", "Co-Founder & Product Manager")
        furkan_acc.setdefault("company", "DeDev")
        furkan_acc.setdefault("location", "Remote / Global")
        furkan_acc.setdefault("since", "2024")
        furkan_acc.setdefault("bio", "Furkan, DeDev ortağı ve ürün yöneticisi.")
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
            "name": "Furkan",
            "role": "Co-Founder & Product Manager",
            "company": "DeDev",
            "location": "Remote / Global",
            "since": "2024",
            "bio": "Furkan, DeDev ortağı ve ürün yöneticisi."
        })
        
    # Auto-migrate any other legacy accounts loaded from database
    for acc in data.get("accounts", []):
        if "password" in acc and "password_hash" not in acc:
            h_val, s_val = hash_password(str(acc["password"]))
            acc["password_hash"] = h_val
            acc["password_salt"] = s_val
            del acc["password"]
        
    if "active_owner" not in data:
        data["active_owner"] = "Deniz Deviren"
        
    # Initialize departments
    if "departments" not in data or not data["departments"]:
        data["departments"] = [
            {"id": "DEP-YAZILIM", "name": "Yazılım Geliştirme", "description": "Web, mobil ve backend geliştirme süreçleri.", "color": "#3b82f6", "icon": "💻"},
            {"id": "DEP-AI", "name": "Yapay Zeka & Veri Bilimi", "description": "Makine öğrenimi modelleri, LLM entegrasyonları.", "color": "#8b5cf6", "icon": "🧠"},
            {"id": "DEP-TASARIM", "name": "Tasarım & UI/UX", "description": "Arayüz tasarımı, grafikler ve marka kimliği.", "color": "#ec4899", "icon": "🎨"},
            {"id": "DEP-PAZARLAMA", "name": "Pazarlama & Satış", "description": "Müşteri ilişkileri ve ürün tanıtımları.", "color": "#f59e0b", "icon": "📈"},
            {"id": "DEP-YONETIM", "name": "Yönetim", "description": "Stratejik yönetim ve karar alma süreçleri.", "color": "#ef4444", "icon": "👑"}
        ]
        
    # Set default department for existing team members if not present
    for member in data.setdefault("team", []):
        if "department" not in member:
            member["department"] = "Yazılım Geliştirme"
            
    # Check if Furkan has any projects. If not, add mock projects and tasks for simulation
    furkan_projects = [p for p in data.setdefault("projects", []) if p.get("owner_name") == "Furkan"]
    if not furkan_projects:
        # Create mock project
        mock_proj = {
            "id": "PROJ-SIM-1",
            "name": "DeDev Mobil Cüzdan",
            "category": "Mobil Uygulama",
            "status": "In Progress",
            "priority": "High",
            "start_date": "2026-05-01",
            "end_date": "2026-07-15",
            "budget": 15000.0,
            "lines_of_code": 12500,
            "description": "Ekip içi ödemeleri ve cüzdan hareketlerini izleyen mobil uygulama geliştirme süreci.",
            "tech_stack": ["Dart", "Flutter", "Firebase"],
            "owner_name": "Furkan",
            "milestones": [
                {"id": "MS-SIM-1", "name": "UI/UX Tasarımları", "date": "2026-05-15", "status": "Completed"},
                {"id": "MS-SIM-2", "name": "Firebase Entegrasyonu", "date": "2026-06-10", "status": "Pending"}
            ]
        }
        data["projects"].append(mock_proj)
        
        # Create mock tasks
        mock_tasks = [
            {
                "id": "TASK-SIM-1",
                "title": "Giriş ekranı ve login tasarımı",
                "status": "Done",
                "priority": "Medium",
                "date": "2026-05-12",
                "project_id": "PROJ-SIM-1",
                "assignee": "Furkan",
                "effort": 3
            },
            {
                "id": "TASK-SIM-2",
                "title": "State Management kurulumu (Provider)",
                "status": "In Progress",
                "priority": "High",
                "date": "2026-05-24",
                "project_id": "PROJ-SIM-1",
                "assignee": "Furkan",
                "effort": 5
            },
            {
                "id": "TASK-SIM-3",
                "title": "API bağlantıları ve servis katmanı",
                "status": "To Do",
                "priority": "High",
                "date": "2026-06-05",
                "project_id": "PROJ-SIM-1",
                "assignee": "Ahmet Yılmaz",
                "effort": 8
            }
        ]
        data.setdefault("tasks", []).extend(mock_tasks)
        
        # Create mock time logs
        mock_logs = [
            {
                "date": "2026-05-22",
                "project_id": "PROJ-SIM-1",
                "task_title": "State Management kurulumu (Provider)",
                "duration": 2.5,
                "effort_level": "Yüksek",
                "description": "Provider mimarisi kuruldu ve entegre edildi."
            },
            {
                "date": "2026-05-22",
                "project_id": "PROJ-SIM-1",
                "task_title": "UI/UX Tasarımları",
                "duration": 1.5,
                "effort_level": "Orta",
                "description": "Arayüz revizyonları yapıldı."
            }
        ]
        data.setdefault("time_logs", []).extend(mock_logs)
        
        # Create mock finances
        mock_finances = [
            {
                "id": "FIN-SIM-1",
                "project_id": "PROJ-SIM-1",
                "type": "Gelir",
                "category": "Yazılım Satış",
                "amount": 25000.0,
                "date": "2026-05-02",
                "description": "Proje avansı alındı."
            },
            {
                "id": "FIN-SIM-2",
                "project_id": "PROJ-SIM-1",
                "type": "Gider",
                "category": "Sunucu / Altyapı",
                "amount": 350.0,
                "date": "2026-05-18",
                "description": "Firebase Blaze plan ödemesi."
            }
        ]
        data.setdefault("finances", []).extend(mock_finances)
        
        # Create mock team members if not already there
        data.setdefault("team", [])
        if not any(t["name"] == "Ahmet Yılmaz" for t in data["team"]):
            data["team"].append({"name": "Ahmet Yılmaz", "role": "Mobil Geliştirici", "department": "Yazılım Geliştirme", "email": "ahmet@dedev.com"})
        if not any(t["name"] == "Elif Demir" for t in data["team"]):
            data["team"].append({"name": "Elif Demir", "role": "UI/UX Tasarımcı", "department": "Tasarım & UI/UX", "email": "elif@dedev.com"})

    return data

def get_filtered_elements(data):
    active_owner = data.get("active_owner", "Deniz Deviren")
    
    # Filter projects belonging to active owner
    projects = [p for p in data.get("projects", []) if p.get("owner_name", "Deniz Deviren") == active_owner]
    project_ids = {p["id"] for p in projects}
    
    # Filter tasks
    tasks = [t for t in data.get("tasks", []) if t.get("project_id") in project_ids]
    
    # Filter time logs
    time_logs = [log for log in data.get("time_logs", []) if log.get("project_id") in project_ids]
    
    # Filter finances
    finances = [f for f in data.get("finances", []) if not f.get("project_id") or f.get("project_id") in project_ids]
    
    # Filter activities
    activities = [a for a in data.get("activities", []) if not a.get("project") or a.get("project") in project_ids]
    
    # Filter deployments
    deployments = [d for d in data.get("deployments", []) if d.get("project") in project_ids]
    
    return active_owner, projects, tasks, time_logs, finances, activities, deployments

def load_data():
    # If local file does not exist, try to pull from Google Sheets first (critical for Streamlit Cloud)
    if not os.path.exists(DATA_FILE):
        if is_gsheets_configured():
            data, msg = pull_from_sheets()
            if data:
                try:
                    data = init_defaults(data)
                    data = migrate_dates_to_2026(data)
                    with open(DATA_FILE, "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    return data
                except Exception:
                    return data
        
        default_data = {"projects": [], "tasks": [], "notes": [], "time_logs": [], "finances": [], "deployments": [], "activities": []}
        default_data = init_defaults(default_data)
        return default_data
    
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        # Apply migrations and defaults in-place
        initial_data_str = json.dumps(data)
        data = init_defaults(data)
        data = migrate_dates_to_2026(data)
        
        # Save back if there are any changes (like year migration or key initialization)
        if json.dumps(data) != initial_data_str:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
        return data
    except Exception:
        default_data = {"projects": [], "tasks": [], "notes": [], "time_logs": [], "finances": [], "deployments": [], "activities": []}
        default_data = init_defaults(default_data)
        return default_data

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


