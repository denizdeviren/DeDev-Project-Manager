import json
import os
import threading
import shutil
import uuid
from utils.gsheets_handler import is_gsheets_configured, push_to_sheets, pull_from_sheets

# Absolute path to data.json in the project root directory
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR)
DATA_FILE = os.path.normpath(os.path.join(ROOT_DIR, "data.json"))


# ---------------------------------------------------------------------------
# Date migration helper
# ---------------------------------------------------------------------------
def migrate_dates_to_2026(data):
    for proj in data.get("projects", []):
        for field in ("start_date", "end_date"):
            if isinstance(proj.get(field), str):
                proj[field] = proj[field].replace("2024-", "2026-").replace("2025-", "2026-")
        for ms in proj.get("milestones", []):
            if isinstance(ms.get("date"), str):
                ms["date"] = ms["date"].replace("2024-", "2026-").replace("2025-", "2026-")
    for task in data.get("tasks", []):
        if isinstance(task.get("date"), str):
            task["date"] = task["date"].replace("2024-", "2026-").replace("2025-", "2026-")
    for log in data.get("time_logs", []):
        if isinstance(log.get("date"), str):
            log["date"] = log["date"].replace("2024-", "2026-").replace("2025-", "2026-")
    for act in data.get("activities", []):
        if isinstance(act.get("date"), str):
            act["date"] = act["date"].replace("2024-", "2026-").replace("2025-", "2026-")
    for dep in data.get("deployments", []):
        if isinstance(dep.get("last_deploy"), str):
            dep["last_deploy"] = dep["last_deploy"].replace("2024-", "2026-").replace("2025-", "2026-")
    return data


# ---------------------------------------------------------------------------
# Production account initialisation (1denizdeviren + furkan)
# ---------------------------------------------------------------------------
def init_defaults(data):
    from utils.encryption import hash_password

    data.setdefault("accounts", [])

    # --- Deniz Deviren ---
    deniz_acc = next(
        (a for a in data["accounts"]
         if a.get("username") == "1denizdeviren" or a.get("name") == "Deniz Deviren"),
        None,
    )
    if deniz_acc:
        deniz_acc["username"] = "1denizdeviren"
        deniz_acc["name"] = "Deniz Deviren"
        deniz_acc.setdefault("role", "Solo Full-Stack Developer & AI Engineer")
        deniz_acc.setdefault("company", "DeDev")
        deniz_acc.setdefault("location", "Remote / Global")
        deniz_acc.setdefault("since", "2023")
        deniz_acc.setdefault("bio", "Tek kişilik ekip. Yapay zeka, web, mobil ve oyun geliştirme projeleri.")
        if "password_hash" not in deniz_acc:
            deniz_acc["password_hash"] = "6a13b67f7ff4538333b55e6800d33ced0b897f9a75612319c3631b9e8ab67b13"
            deniz_acc["password_salt"] = "019769293f90510166382122020ef513"
            deniz_acc.pop("password", None)
    else:
        data["accounts"].append({
            "username": "1denizdeviren",
            "password_hash": "6a13b67f7ff4538333b55e6800d33ced0b897f9a75612319c3631b9e8ab67b13",
            "password_salt": "019769293f90510166382122020ef513",
            "name": "Deniz Deviren",
            "role": "Solo Full-Stack Developer & AI Engineer",
            "company": "DeDev",
            "location": "Remote / Global",
            "since": "2023",
            "bio": "Tek kişilik ekip. Yapay zeka, web, mobil ve oyun geliştirme projeleri.",
            "role_type": "admin",
        })

    # --- M. Furkan Işık ---
    furkan_acc = next(
        (a for a in data["accounts"]
         if a.get("username") == "furkan" or a.get("name") in ["Furkan", "M. Furkan Işık"]),
        None,
    )
    if furkan_acc:
        furkan_acc.setdefault("username", "furkan")
        furkan_acc.setdefault("name", "M. Furkan Işık")
        furkan_acc.setdefault("role", "Co-Founder & Developer")
        furkan_acc.setdefault("company", "DeDev")
        furkan_acc.setdefault("location", "Remote / Global")
        furkan_acc.setdefault("since", "2024")
        furkan_acc.setdefault("bio", "M. Furkan Işık, DeDev ortağı ve yazılım geliştiricisi.")
        if "password_hash" not in furkan_acc:
            h_val, s_val = hash_password("123456")
            furkan_acc["password_hash"] = h_val
            furkan_acc["password_salt"] = s_val
            furkan_acc.pop("password", None)
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
            "bio": "M. Furkan Işık, DeDev ortağı ve yazılım geliştiricisi.",
            "role_type": "admin",
        })

    # Keep all production and team member accounts. Filtering is removed to preserve team logins.

    # Password migration for any plain-text passwords
    for acc in data["accounts"]:
        if "password" in acc and "password_hash" not in acc:
            h_val, s_val = hash_password(str(acc.pop("password")))
            acc["password_hash"] = h_val
            acc["password_salt"] = s_val

    if any(a.get("username") == "1denizdeviren" for a in data.get("accounts", [])):
        data["active_owner"] = "Deniz Deviren"
    else:
        data.setdefault("active_owner", "Deniz Deviren")
    for key in ("projects", "tasks", "notes", "time_logs", "finances",
                "deployments", "activities", "team"):
        data.setdefault(key, [])

    # Scrub any stale mock names that leaked from demo data
    mock_names = {"ahmet yılmaz", "elif demir", "elif aksoy", "ahmet", "elif",
                  "ahmet yilmaz", "elif demır"}
    data["team"] = [
        m for m in data["team"]
        if m.get("name", "").strip().lower() not in mock_names
    ]
    for t in data["tasks"]:
        if t.get("assignee", "").strip().lower() in mock_names:
            t["assignee"] = "Deniz Deviren"
    for p in data["projects"]:
        if p.get("owner_name", "").strip().lower() in mock_names:
            p["owner_name"] = "Deniz Deviren"

    if not data.get("bank_accounts"):
        data["bank_accounts"] = [
            {"id": "ACC-DEFAULT-CASH", "name": "Merkez Kasa", "balance": 0.0, "currency": "TRY"}
        ]
    data.setdefault("accounting_ledger", [])

    if not data.get("departments"):
        data["departments"] = [
            {"id": "DEP-YAZILIM", "name": "Yazılım Geliştirme", "description": "Web, mobil ve backend geliştirme süreçleri.", "color": "#3b82f6", "icon": "💻"},
            {"id": "DEP-AI",      "name": "Yapay Zeka & Veri Bilimi", "description": "Makine öğrenimi modelleri, LLM entegrasyonları.", "color": "#8b5cf6", "icon": "🧠"},
            {"id": "DEP-TASARIM", "name": "Tasarım & UI/UX", "description": "Arayüz tasarımı, grafikler ve marka kimliği.", "color": "#ec4899", "icon": "🎨"},
            {"id": "DEP-PAZARLAMA","name": "Pazarlama & Satış", "description": "Müşteri ilişkileri ve ürün tanıtımları.", "color": "#f59e0b", "icon": "📈"},
            {"id": "DEP-YONETIM", "name": "Yönetim", "description": "Stratejik yönetim ve karar alma süreçleri.", "color": "#ef4444", "icon": "👑"},
        ]

    for member in data["team"]:
        member.setdefault("department", "Yazılım Geliştirme")
        if "id" not in member:
            name = member.get("name", "")
            if name == "Ahmet Yılmaz":
                member["id"] = "USR-AHMET"
            elif name == "Elif Demir":
                member["id"] = "USR-ELIF"
            elif name == "M. Furkan Işık":
                member["id"] = "USR-FURKAN"
            else:
                member["id"] = f"USR-{str(uuid.uuid4())[:6].upper()}"

    # Legacy name migration
    if data.get("active_owner") == "Furkan":
        data["active_owner"] = "M. Furkan Işık"
    for proj in data["projects"]:
        if proj.get("owner_name") == "Furkan":
            proj["owner_name"] = "M. Furkan Işık"
    for task in data["tasks"]:
        if task.get("assignee") == "Furkan":
            task["assignee"] = "M. Furkan Işık"

    return data


# ---------------------------------------------------------------------------
# Demo / simulation account initialisation (first-time only)
# ---------------------------------------------------------------------------
def init_demo_defaults(data):
    from utils.encryption import hash_password

    # 1. Accounts (reset only on true first-run, i.e., when accounts list is empty)
    data.setdefault("accounts", [])
    if not any(a.get("username") == "demo_erpsim" for a in data["accounts"]):
        h_val, s_salt = hash_password("demo123")
        data["accounts"].append({
            "username": "demo_erpsim",
            "password_hash": h_val,
            "password_salt": s_salt,
            "name": "Murat Yıldırım",
            "role": "CEO & Software Architect",
            "company": "Aura Yazılım Teknolojileri",
            "location": "İstanbul, Türkiye",
            "since": "2026",
            "bio": "Aura Yazılım Teknolojileri kurucu ortağı ve baş mimarı. Tüm iş süreçlerini ve projeleri buradan yönetir.",
            "role_type": "admin",
        })

    data["active_owner"] = "Murat Yıldırım"

    # 2. Team (only if empty)
    data.setdefault("team", [])
    if not data["team"]:
        data["team"] = [
            {"id": "USR-AHMET",   "name": "Ahmet Yılmaz",  "role": "Product Manager",   "department": "Yönetim",           "email": "ahmet@auratech.com"},
            {"id": "USR-ELIF",    "name": "Elif Demir",     "role": "Backend Developer",  "department": "Yazılım Geliştirme","email": "elif@auratech.com"},
            {"id": "USR-METEHAN","name": "Metehan Şahin",  "role": "Senior Developer",   "department": "Yazılım Geliştirme","email": "metehan@auratech.com"},
            {"id": "USR-SELIN",   "name": "Selin Kaya",     "role": "UI/UX Tasarımcı",    "department": "Tasarım & UI/UX",   "email": "selin@auratech.com"},
            {"id": "USR-ALPEREN","name": "Alperen Yılmaz", "role": "Mali Müşavir",        "department": "Yönetim",           "email": "alperen@auratech.com"},
        ]

    # 3. Projects (only if empty)
    data.setdefault("projects", [])
    if not data["projects"]:
        data["projects"] = [
            {
                "id": "PROJ-DEMO-1",
                "name": "Aura Kurumsal ERP Uygulaması",
                "category": "Kurumsal Sistem",
                "status": "In Progress",
                "priority": "High",
                "start_date": "2026-05-10",
                "end_date": "2026-08-20",
                "budget": 250000.0,
                "lines_of_code": 34500,
                "description": "Kurumsal süreçlerin, finansal yönetim araçlarının ve proje planlama modüllerinin sergilendiği ana ERP projesi.",
                "tech_stack": ["Python", "Streamlit", "Plotly", "PostgreSQL"],
                "owner_name": "Murat Yıldırım",
                "milestones": [
                    {"id": "MS-DEMO-1", "name": "Veritabanı Şeması Tasarımı",    "date": "2026-05-20", "status": "Completed"},
                    {"id": "MS-DEMO-2", "name": "Muhasebe Modülü Entegrasyonu", "date": "2026-06-15", "status": "Pending"},
                ],
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
                "owner_name": "Murat Yıldırım",
                "milestones": [
                    {"id": "MS-DEMO-3", "name": "Tasarım Onayı", "date": "2026-05-28", "status": "Pending"},
                ],
            },
        ]

    # 4. Tasks (only if empty)
    data.setdefault("tasks", [])
    if not data["tasks"]:
        data["tasks"] = [
            {"id": "TASK-DEMO-1", "title": "Finansal verileri incele ve mizan raporu al",        "status": "Done",        "priority": "High",   "date": "2026-05-15", "project_id": "PROJ-DEMO-1", "assignee": "Alperen Yılmaz", "effort": 2},
            {"id": "TASK-DEMO-2", "title": "Kanban panosunda sürükle-bırak testlerini tamamla", "status": "In Progress", "priority": "Medium", "date": "2026-05-28", "project_id": "PROJ-DEMO-1", "assignee": "Elif Demir",     "effort": 4},
            {"id": "TASK-DEMO-3", "title": "Mobil arayüz login sayfasını tasarla",               "status": "In Progress", "priority": "High",   "date": "2026-05-26", "project_id": "PROJ-DEMO-2", "assignee": "Selin Kaya",     "effort": 5},
            {"id": "TASK-DEMO-4", "title": "Double-entry muhasebe test faturalarını oluştur",    "status": "Done",        "priority": "Medium", "date": "2026-05-22", "project_id": "PROJ-DEMO-1", "assignee": "Ahmet Yılmaz",  "effort": 3},
        ]

    # 5. Time logs (only if empty)
    data.setdefault("time_logs", [])
    if not data["time_logs"]:
        data["time_logs"] = [
            {"date": "2026-05-22", "project_id": "PROJ-DEMO-1", "task_title": "Finansal verileri incele ve mizan raporu al", "duration": 4.0, "effort_level": "Orta",    "description": "Double-entry ledger test edildi ve mizan raporu doğrulandı."},
            {"date": "2026-05-22", "project_id": "PROJ-DEMO-2", "task_title": "Mobil arayüz login sayfasını tasarla",        "duration": 3.5, "effort_level": "Yüksek", "description": "Figma tasarımları Flutter widget'larına dönüştürülüyor."},
        ]

    # 6. Finances (only if empty)
    data.setdefault("finances", [])
    if not data["finances"]:
        data["finances"] = [
            {"id": "FIN-DEMO-1", "project_id": "PROJ-DEMO-1", "type": "Gelir",  "category": "Yazılım Satış",       "amount": 125000.0, "date": "2026-05-12", "description": "Birinci faz hak ediş ödemesi tahsil edildi."},
            {"id": "FIN-DEMO-2", "project_id": "PROJ-DEMO-2", "type": "Gider",  "category": "Pazarlama / Reklam",  "amount": 5000.0,   "date": "2026-05-20", "description": "Sosyal medya lansman bütçesi."},
        ]

    # 7. Bank accounts (only if empty)
    data.setdefault("bank_accounts", [])
    if not data["bank_accounts"]:
        data["bank_accounts"] = [
            {"id": "ACC-DEMO-1", "name": "Akbank Ticari", "balance": 125000.0, "currency": "TRY"},
            {"id": "ACC-DEMO-2", "name": "Nakit Kasa",    "balance": 15000.0,  "currency": "TRY"},
            {"id": "ACC-DEMO-3", "name": "Garanti USD",   "balance": 12000.0,  "currency": "USD"},
        ]

    # 8. Accounting ledger (only if empty)
    data.setdefault("accounting_ledger", [])
    if not data["accounting_ledger"]:
        data["accounting_ledger"] = [
            {"id": "TX-DEMO-INIT-01", "date": "2026-05-10", "voucher_no": "FIŞ-20260510-001", "description": "Akbank Ticari Sermaye Açılışı",        "debit_account": "Akbank Ticari", "credit_account": "Özkaynaklar / Sermaye", "amount": 125000.0, "tax_rate": 0, "tax_amount": 0.0, "grand_total": 125000.0, "type": "Açılış",    "project_id": None, "created_by": "demo_erpsim", "is_correction": False, "corrected_tx_id": None, "is_corrected": False},
            {"id": "TX-DEMO-INIT-02", "date": "2026-05-10", "voucher_no": "FIŞ-20260510-002", "description": "Nakit Kasa Sermaye Açılışı",           "debit_account": "Nakit Kasa",    "credit_account": "Özkaynaklar / Sermaye", "amount": 15000.0,  "tax_rate": 0, "tax_amount": 0.0, "grand_total": 15000.0,  "type": "Açılış",    "project_id": None, "created_by": "demo_erpsim", "is_correction": False, "corrected_tx_id": None, "is_corrected": False},
            {"id": "TX-DEMO-INIT-03", "date": "2026-05-10", "voucher_no": "FIŞ-20260510-003", "description": "Garanti USD Sermaye Açılışı",          "debit_account": "Garanti USD",   "credit_account": "Özkaynaklar / Sermaye", "amount": 12000.0,  "tax_rate": 0, "tax_amount": 0.0, "grand_total": 12000.0,  "type": "Açılış",    "project_id": None, "created_by": "demo_erpsim", "is_correction": False, "corrected_tx_id": None, "is_corrected": False},
            {"id": "TX-DEMO-TX-01",   "date": "2026-05-12", "voucher_no": "FAT-20260512-001", "description": "Aura Kurumsal ERP 1. Faz Fatura Tahsilatı", "debit_account": "Akbank Ticari", "credit_account": "Yurtiçi Satışlar (Gelir)", "amount": 125000.0, "tax_rate": 20, "tax_amount": 25000.0, "grand_total": 150000.0, "type": "Tahsilat", "project_id": "PROJ-DEMO-1", "created_by": "demo_erpsim", "is_correction": False, "corrected_tx_id": None, "is_corrected": False},
        ]

    for key in ("deployments", "activities", "notes"):
        data.setdefault(key, [])

    data.setdefault("departments", [
        {"id": "DEP-YAZILIM",  "name": "Yazılım Geliştirme", "description": "Web, mobil ve backend geliştirme süreçleri.", "color": "#3b82f6", "icon": "💻"},
        {"id": "DEP-AI",       "name": "Yapay Zeka & Veri Bilimi", "description": "Makine öğrenimi modelleri, LLM entegrasyonları.", "color": "#8b5cf6", "icon": "🧠"},
        {"id": "DEP-TASARIM",  "name": "Tasarım & UI/UX", "description": "Arayüz tasarımı, grafikler ve marka kimliği.", "color": "#ec4899", "icon": "🎨"},
        {"id": "DEP-PAZARLAMA","name": "Pazarlama & Satış", "description": "Müşteri ilişkileri ve ürün tanıtımları.", "color": "#f59e0b", "icon": "📈"},
        {"id": "DEP-YONETIM", "name": "Yönetim", "description": "Stratejik yönetim ve karar alma süreçleri.", "color": "#ef4444", "icon": "👑"},
    ])

    return data


# ---------------------------------------------------------------------------
# Per-user isolated file path
# ---------------------------------------------------------------------------
def get_data_file_path(username=None):
    """Return the isolated JSON data file for the given (or session) user."""
    if username is None:
        try:
            import streamlit as st
            username = st.session_state.get("logged_in_user")
        except Exception:
            pass

    if username:
        # Check if the user is a main owner / default database workspace owner
        if username in ("1denizdeviren", "furkan", "demo_erpsim"):
            user_file = os.path.normpath(os.path.join(ROOT_DIR, f"data_user_{username}.json"))

            # One-time migration from legacy single-file layout
            if not os.path.exists(user_file):
                if username == "demo_erpsim":
                    legacy = os.path.normpath(os.path.join(ROOT_DIR, "data_demo.json"))
                    if os.path.exists(legacy):
                        shutil.copy2(legacy, user_file)
                elif username == "1denizdeviren":
                    if os.path.exists(DATA_FILE):
                        shutil.copy2(DATA_FILE, user_file)

            return user_file

        # If it's a team member, search all data_user_*.json files for this username
        try:
            for fname in os.listdir(ROOT_DIR):
                if fname.startswith("data_user_") and fname.endswith(".json"):
                    fpath = os.path.join(ROOT_DIR, fname)
                    try:
                        with open(fpath, "r", encoding="utf-8") as f:
                            accs = json.load(f).get("accounts", [])
                            if any(a.get("username") == username for a in accs):
                                return fpath
                    except Exception:
                        pass
        except Exception:
            pass

        # If not found anywhere, fallback to their own file path
        return os.path.normpath(os.path.join(ROOT_DIR, f"data_user_{username}.json"))

    return DATA_FILE  # fallback (should only happen before login)


# ---------------------------------------------------------------------------
# Account lookup — used by login screen and admin panel
# ---------------------------------------------------------------------------
def get_all_accounts():
    """Return accounts for the current context.

    * When a user IS logged in  → return only their own database accounts
      (no cross-database leakage).
    * When NO user is logged in → scan all databases so the login screen can
      authenticate any registered user.
    """
    accounts = []
    current_user = None
    try:
        import streamlit as st
        current_user = st.session_state.get("logged_in_user")
    except Exception:
        pass

    if current_user:
        # --- Logged-in: read only this user's file ---
        filepath = get_data_file_path(current_user)
        if os.path.exists(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    accounts.extend(json.load(f).get("accounts", []))
            except Exception:
                pass
        else:
            # File not yet created — fall back to legacy paths
            if current_user == "demo_erpsim":
                legacy = os.path.normpath(os.path.join(ROOT_DIR, "data_demo.json"))
                if os.path.exists(legacy):
                    try:
                        with open(legacy, "r", encoding="utf-8") as f:
                            accounts.extend(json.load(f).get("accounts", []))
                    except Exception:
                        pass
            else:
                if os.path.exists(DATA_FILE):
                    try:
                        with open(DATA_FILE, "r", encoding="utf-8") as f:
                            accounts.extend(json.load(f).get("accounts", []))
                    except Exception:
                        pass
    else:
        # --- Not logged in: scan everything so login works ---
        # Legacy data.json
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    accounts.extend(json.load(f).get("accounts", []))
            except Exception:
                pass
        # All per-user files
        try:
            for fname in os.listdir(ROOT_DIR):
                if fname.startswith("data_user_") and fname.endswith(".json"):
                    fpath = os.path.join(ROOT_DIR, fname)
                    try:
                        with open(fpath, "r", encoding="utf-8") as f:
                            accounts.extend(json.load(f).get("accounts", []))
                    except Exception:
                        pass
        except Exception:
            pass
        # Legacy demo file
        legacy_demo = os.path.normpath(os.path.join(ROOT_DIR, "data_demo.json"))
        if os.path.exists(legacy_demo):
            try:
                with open(legacy_demo, "r", encoding="utf-8") as f:
                    accounts.extend(json.load(f).get("accounts", []))
            except Exception:
                pass

    # Deduplicate by username
    seen: set = set()
    dedup = []
    for acc in accounts:
        uname = acc.get("username")
        if uname and uname not in seen:
            seen.add(uname)
            dedup.append(acc)
    return dedup


# ---------------------------------------------------------------------------
# Filtered element view (respects active_owner and member permissions)
# ---------------------------------------------------------------------------
def get_filtered_elements(data):
    import streamlit as st
    active_owner = data.get("active_owner", "Deniz Deviren")

    projects = [p for p in data.get("projects", []) if p.get("owner_name", active_owner) == active_owner]
    project_ids = {p["id"] for p in projects}

    tasks       = [t for t in data.get("tasks",      []) if t.get("project_id") in project_ids]
    time_logs   = [l for l in data.get("time_logs",  []) if l.get("project_id") in project_ids]
    finances    = [f for f in data.get("finances",   []) if not f.get("project_id") or f.get("project_id") in project_ids]
    activities  = [a for a in data.get("activities", []) if not a.get("project")    or a.get("project")    in project_ids]
    deployments = [d for d in data.get("deployments",[]) if d.get("project") in project_ids]

    current_user = st.session_state.get("logged_in_user")
    if current_user:
        current_acc = next((a for a in data.get("accounts", []) if a.get("username") == current_user), None)
        if current_acc and current_acc.get("role_type") == "member":
            member_name = current_acc.get("name")
            tasks = [t for t in tasks if t.get("assignee") == member_name]
            member_proj_ids = {t["project_id"] for t in tasks if "project_id" in t}
            projects = [
                p for p in projects
                if p.get("owner_name") == member_name
                or p["id"] in member_proj_ids
                or member_name in p.get("team", [])
            ]
            project_ids = {p["id"] for p in projects}
            tasks       = [t for t in tasks       if t.get("project_id") in project_ids]
            time_logs   = [l for l in time_logs   if l.get("project_id") in project_ids]
            finances    = [f for f in finances     if f.get("project_id") in project_ids]
            activities  = [a for a in activities   if a.get("project")    in project_ids]
            deployments = [d for d in deployments  if d.get("project")    in project_ids]

    return active_owner, projects, tasks, time_logs, finances, activities, deployments


# ---------------------------------------------------------------------------
# load_data / save_data
# ---------------------------------------------------------------------------
def load_data():
    filepath = get_data_file_path()
    is_demo = "demo_erpsim" in os.path.basename(filepath)

    if not os.path.exists(filepath):
        if is_demo:
            default = {"projects": [], "tasks": [], "notes": [], "time_logs": [],
                       "finances": [], "deployments": [], "activities": []}
            default = init_demo_defaults(default)
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(default, f, ensure_ascii=False, indent=2)
            return default

        if is_gsheets_configured():
            data, _ = pull_from_sheets()
            if data:
                try:
                    data = init_defaults(data)
                    data = migrate_dates_to_2026(data)
                    with open(filepath, "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    return data
                except Exception:
                    return data

        default = {"projects": [], "tasks": [], "notes": [], "time_logs": [],
                   "finances": [], "deployments": [], "activities": []}
        return init_defaults(default)

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        snapshot = json.dumps(data)
        if is_demo:
            data = init_demo_defaults(data)   # safe: only fills missing keys
        else:
            data = init_defaults(data)
        data = migrate_dates_to_2026(data)

        if json.dumps(data) != snapshot:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

        return data
    except Exception:
        default = {"projects": [], "tasks": [], "notes": [], "time_logs": [],
                   "finances": [], "deployments": [], "activities": []}
        return init_demo_defaults(default) if is_demo else init_defaults(default)


def save_data(data):
    filepath = get_data_file_path()
    is_demo = "demo_erpsim" in os.path.basename(filepath)

    try:
        from utils.automations import run_automations
        run_automations(data)
    except Exception:
        pass

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    if not is_demo and is_gsheets_configured():
        threading.Thread(target=push_to_sheets, args=(data,), daemon=True).start()


# ---------------------------------------------------------------------------
# Misc
# ---------------------------------------------------------------------------
colors_map = {
    "Washington Emlak AI":   "#667eea",
    "ComTerms DeDe AI":      "#f59e0b",
    "DeDev FPS: Shadow Ops": "#ef4444",
    "DeDev Project Manager": "#22c55e",
}
