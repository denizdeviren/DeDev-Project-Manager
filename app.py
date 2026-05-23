import streamlit as st

# ==========================================
# PAGE CONFIGURATION (Zorunlu olarak en üstte)
# ==========================================
st.set_page_config(
    page_title="DeDev | Command Center",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Utils ve Veri Yönetimi
from utils.data_handler import load_data, save_data, get_all_accounts

# Sayfa (View) Importları
from views.dashboard import show_dashboard
from views.projects_view import show_projects
from views.secret_vault import show_secret_vault
from views.kanban_view import show_kanban
from views.timeline import show_timeline
from views.calendar_view import show_calendar
from views.techstack import show_techstack
from views.reports import show_reports
from views.notes import show_notes
from views.team_view import show_team
from views.time_tracking import show_time_tracking
from views.finance_view import show_finance
from views.admin_view import show_admin
from views.archive_view import show_archive
from views.portfolio_rating import show_portfolio_rating
from views.about_view import show_about



# Global CSS
st.markdown("""
<style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Background & Text Colors */
    .stApp {
        background: linear-gradient(145deg, #0f0f23 0%, #171735 100%);
        color: #e5e7eb;
    }
    
    /* Main Content Area */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 5rem !important;
    }
    
    /* Custom Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 15, 35, 0.95);
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    
    /* Hide Streamlit Branding & Footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Make header transparent instead of hiding it entirely (so mobile sidebar toggle button is visible) */
    header {
        background: transparent !important;
    }
    [data-testid="stHeader"] {
        background: transparent !important;
    }
    
    /* Style the sidebar collapse button to look premium and always be visible */
    [data-testid="stSidebarCollapseButton"] {
        visibility: visible !important;
        display: flex !important;
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 8px !important;
        color: white !important;
        z-index: 999999 !important;
    }
    [data-testid="stSidebarCollapseButton"]:hover {
        background-color: rgba(102, 126, 234, 0.2) !important;
        border-color: rgba(102, 126, 234, 0.4) !important;
    }
    
    /* Metric Cards */
    .metric-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 16px;
        padding: 24px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    /* Custom Headings */
    .section-title {
        font-size: 24px;
        font-weight: 800;
        color: white;
        margin-bottom: 5px;
        letter-spacing: -0.5px;
    }
    .section-subtitle {
        font-size: 14px;
        color: #9ca3af;
        margin-bottom: 25px;
    }

    /* Form & Input Styling */
    .stTextInput > div > div > input, .stTextArea > div > textarea, .stSelectbox > div > div {
        background-color: rgba(0,0,0,0.2) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 8px !important;
        color: white !important;
    }
    .stTextInput > div > div > input:focus, .stTextArea > div > textarea:focus, .stSelectbox > div > div:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 1px #667eea !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 600 !important;
        transition: opacity 0.2s !important;
    }
    .stButton > button:hover {
        opacity: 0.9 !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4) !important;
    }

    /* Developer Social Links */
    .developer-social-links a {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    .developer-social-links a:hover {
        transform: translateY(-3px) scale(1.08);
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border-color: transparent !important;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4) !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# GÜVENLİ GİRİŞ KONTROLÜ & EKRANI
# ==========================================
if "logged_in_user" not in st.session_state:
    # Try to restore session from query parameters to prevent logout on refresh
    params = st.query_params
    if "user" in params:
        st.session_state["logged_in_user"] = params["user"]
    else:
        st.session_state["logged_in_user"] = None

# ==========================================
# VERİ YÜKLEME
# ==========================================
data = load_data()

if st.session_state["logged_in_user"] is None:
    st.markdown("""
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 85vh; padding: 20px;">
        <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 24px; padding: 40px; max-width: 480px; width: 100%; backdrop-filter: blur(15px); box-shadow: 0 20px 50px rgba(0,0,0,0.3); text-align: center;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); width: 70px; height: 70px; border-radius: 20px; display: flex; align-items: center; justify-content: center; font-size: 32px; font-weight: bold; color: white; margin: 0 auto 20px auto; box-shadow: 0 8px 25px rgba(102,126,234,0.4);">
                🚀
            </div>
            <h1 style="font-size: 28px; font-weight: 800; color: white; margin-bottom: 5px; background: -webkit-linear-gradient(45deg, #a5b4fc, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">DeDev Command Center</h1>
            <p style="font-size: 13px; color: #9ca3af; margin-bottom: 25px;">Giriş yapın veya yeni bir simülasyon hesabı oluşturun</p>
    """, unsafe_allow_html=True)
    
    tab_login, tab_register = st.tabs(["🔑 Giriş Yap", "📝 Kayıt Ol"])
    
    with tab_login:
        with st.form("login_form"):
            username = st.text_input("👤 Kullanıcı Adı", placeholder="Kullanıcı adınızı girin", key="login_username")
            password = st.text_input("🔑 Şifre", placeholder="Şifrenizi girin", type="password", key="login_password")
            
            login_btn = st.form_submit_button("Sisteme Giriş Yap", use_container_width=True)
            
            if login_btn:
                if not username or not password:
                    st.error("Lütfen kullanıcı adı ve şifrenizi girin.")
                else:
                    matched_acc = None
                    all_accounts = get_all_accounts()
                    for acc in all_accounts:
                        if acc.get("username") == username:
                            if "password_hash" in acc and "password_salt" in acc:
                                from utils.encryption import hash_password
                                h_val, _ = hash_password(password, acc["password_salt"])
                                if h_val == acc["password_hash"]:
                                    matched_acc = acc
                                    break
                            elif acc.get("password") == password:
                                from utils.encryption import hash_password
                                h_val, s_val = hash_password(password)
                                acc["password_hash"] = h_val
                                acc["password_salt"] = s_val
                                del acc["password"]
                                save_data(data)
                                matched_acc = acc
                                break
                    
                    if matched_acc:
                        st.session_state["logged_in_user"] = matched_acc["username"]
                        st.query_params["user"] = matched_acc["username"]
                        # Reload data dynamically from the isolated database
                        data = load_data()
                        data["active_owner"] = matched_acc["name"]
                        save_data(data)
                        st.toast(f"Hoş geldiniz, {matched_acc['name']}! 👋")
                        st.rerun()
                    else:
                        st.error("Geçersiz kullanıcı adı veya şifre!")
                        
    with tab_register:
        with st.form("register_form"):
            r_name = st.text_input("👤 Ad Soyad", placeholder="Örn: Simge Yılmaz", key="reg_name")
            r_role = st.text_input("💼 Rol / Ünvan", placeholder="Örn: Yazılım Geliştirici", key="reg_role")
            r_username = st.text_input("🆔 Kullanıcı Adı", placeholder="Giriş yapmak için kullanılacak", key="reg_username")
            r_password = st.text_input("🔒 Şifre", placeholder="Şifrenizi belirleyin", type="password", key="reg_password")
            r_company = st.text_input("🏢 Şirket", placeholder="Örn: DeDev", key="reg_company")
            r_location = st.text_input("📍 Lokasyon", placeholder="Örn: İstanbul / Türkiye", key="reg_location")
            r_bio = st.text_area("📝 Kısa Biyografi", placeholder="Uzmanlık alanlarınız...", max_chars=300, key="reg_bio")
            
            register_btn = st.form_submit_button("Kayıt Ol ve Giriş Yap", use_container_width=True)
            
            if register_btn:
                if not r_name or not r_username or not r_password:
                    st.error("Lütfen Ad Soyad, Kullanıcı Adı ve Şifre alanlarını doldurun.")
                else:
                    # Check duplication against all database accounts
                    all_accounts = get_all_accounts()
                    name_exists = any(acc.get("name", "").lower() == r_name.lower() for acc in all_accounts)
                    username_exists = any(acc.get("username", "").lower() == r_username.lower() for acc in all_accounts)
                    
                    if name_exists or username_exists:
                        st.error("❌ Bu isimle veya kullanıcı adıyla kayıtlı bir profil zaten mevcut!")
                    else:
                        from utils.encryption import hash_password
                        from utils.data_handler import ROOT_DIR, init_defaults
                        import json
                        
                        h_val, s_val = hash_password(r_password)
                        new_acc = {
                            "username": r_username,
                            "password_hash": h_val,
                            "password_salt": s_val,
                            "name": r_name,
                            "role": r_role if r_role else "Proje Sorumlusu",
                            "company": r_company if r_company else "DeDev",
                            "location": r_location if r_location else "Remote",
                            "since": "2026",
                            "bio": r_bio if r_bio else "Yeni simülasyon kullanıcısı.",
                            "role_type": "admin",
                            "permissions": [
                                "dashboard", "projects", "kanban", "timeline", "calendar", 
                                "time_tracking", "archive", "portfolio_rating", "secret_vault", 
                                "team", "reports", "notes", "finance", "admin"
                            ]
                        }
                        
                        # Initialize their own workspace database file
                        user_file = os.path.normpath(os.path.join(ROOT_DIR, f"data_user_{r_username}.json"))
                        default_data = {
                            "accounts": [new_acc],
                            "active_owner": r_name,
                            "projects": [],
                            "tasks": [],
                            "notes": [],
                            "time_logs": [],
                            "finances": [],
                            "deployments": [],
                            "activities": [],
                            "team": []
                        }
                        
                        default_data = init_defaults(default_data)
                        
                        # Ensure the newly created account remains as admin in accounts list
                        if not any(a.get("username") == r_username for a in default_data["accounts"]):
                            default_data["accounts"].append(new_acc)
                        else:
                            # Update existing if already merged by init_defaults
                            for a in default_data["accounts"]:
                                if a.get("username") == r_username:
                                    a["role_type"] = "admin"
                        
                        with open(user_file, "w", encoding="utf-8") as f:
                            json.dump(default_data, f, ensure_ascii=False, indent=2)
                        
                        # Immediately log in the newly registered user for a seamless premium experience!
                        st.session_state["logged_in_user"] = r_username
                        st.query_params["user"] = r_username
                        
                        st.toast(f"Tebrikler! Hesabınız başarıyla oluşturuldu ve giriş yapıldı. 👋")
                        st.rerun()
                        
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    with st.expander("🏢 Kurumsal Demo Hesabı — Canlı Deneyim"):
        st.markdown("""
        <div style="font-family: 'Inter', sans-serif; font-size: 13px; text-align: left; line-height: 1.8; color: #d1d5db;">
            Sistemi canlı olarak keşfetmek için hazır bir kurumsal çalışma alanına giriş yapabilirsiniz.
            <hr style="border-color: rgba(255,255,255,0.08); margin: 10px 0;">
            <b style="color: #a5b4fc;">🏢 Aura Yazılım Teknolojileri</b><br>
            <span style="color: #9ca3af;">Yetkili:</span> <b style="color: white;">Murat Yıldırım</b> — CEO &amp; Software Architect<br>
            <hr style="border-color: rgba(255,255,255,0.08); margin: 10px 0;">
            <span style="color: #9ca3af;">Kullanıcı Adı:</span> <code style="color: #10b981; font-weight: bold;">demo_erpsim</code><br>
            <span style="color: #9ca3af;">Şifre:</span> <code style="color: #10b981; font-weight: bold;">demo123</code>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="font-size: 24px; font-weight: 900; background: -webkit-linear-gradient(45deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">DeDev</h1>
        <p style="font-size: 12px; color: #9ca3af; letter-spacing: 1px;">COMMAND CENTER V2</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🧭 Navigasyon")
    
    # Permission system mapping
    PAGE_KEYS = {
        "🏠 Dashboard": "dashboard",
        "📁 Projeler": "projects",
        "📚 Arşiv ve Belgeler": "archive",
        "📊 DeDev Findeks Skoru": "portfolio_rating",
        "🔒 Gizli Kasa": "secret_vault",
        "📋 Kanban Board": "kanban",
        "📅 Takvim Görünümü": "calendar",
        "📊 Şemalar ve Gantt": "timeline",
        "💻 Tech Stack": "techstack",
        "👥 Ekip Yönetimi": "team",
        "📈 Raporlar": "reports",
        "📝 Hızlı Notlar": "notes",
        "⏱️ Zaman Takibi": "time_tracking",
        "💰 Bütçe & Giderler": "finance",
        "⚙️ Admin Paneli": "admin",
        "ℹ️ Hakkında & Yasal Uyarı": "about"
    }
    
    all_pages = list(PAGE_KEYS.keys())
    current_user = st.session_state.get("logged_in_user")
    current_acc = next((acc for acc in data.get("accounts", []) if acc.get("username") == current_user), None)
    
    is_admin_user = True
    if current_acc:
        is_admin_user = (current_acc.get("username") in ["1denizdeviren", "furkan"]) or (current_acc.get("role_type", "admin") == "admin")
        
    if current_acc and current_acc.get("username") not in ["1denizdeviren", "furkan"] and current_acc.get("role_type", "admin") == "member":
        allowed_keys = list(current_acc.get("permissions", ["dashboard", "projects", "kanban", "timeline", "calendar", "time_tracking"]))
        # Always allow the About & Disclaimer page for legal transparency
        if "about" not in allowed_keys:
            allowed_keys.append("about")
        available_pages = [p for p in all_pages if PAGE_KEYS.get(p) in allowed_keys]
        if not available_pages:
            available_pages = ["🏠 Dashboard"]
    else:
        available_pages = all_pages
        
    # Restore selected page from query parameters if present, preventing reset to home on page refresh
    stored_page_key = st.query_params.get("page")
    default_idx = 0
    if stored_page_key:
        for idx, p_name in enumerate(available_pages):
            if PAGE_KEYS.get(p_name) == stored_page_key:
                default_idx = idx
                break
                
    page = st.radio(
        "",
        available_pages,
        index=default_idx,
        label_visibility="collapsed"
    )
    # Sync selected page back to query parameters
    st.query_params["page"] = PAGE_KEYS.get(page)
    
    if is_admin_user:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.markdown("### ☁️ Bulut Yedekleme")
        from utils.gsheets_handler import is_gsheets_configured, push_to_sheets, pull_from_sheets
        if is_gsheets_configured():
            st.markdown("""
            <div style="background: rgba(16, 185, 129, 0.05); padding: 10px; border-radius: 8px; border: 1px solid rgba(16, 185, 129, 0.15); margin-bottom: 10px;">
                <div style="font-size: 11px; color: #10b981; font-weight: bold; text-align: center;">☁️ GOOGLE SHEETS AKTİF</div>
            </div>
            """, unsafe_allow_html=True)
            
            col_sync1, col_sync2 = st.columns(2)
            with col_sync1:
                if st.button("📤 Yedekle", use_container_width=True, help="Mevcut yerel verileri anında Google Sheets'e yedekler."):
                    success, msg = push_to_sheets(data)
                    if success:
                        st.toast("Veriler buluta başarıyla yedeklendi!", icon="☁️")
                    else:
                        st.error("Yedekleme Hatası")
                        st.toast(msg, icon="❌")
            with col_sync2:
                if st.button("📥 Geri Yükle", use_container_width=True, help="Google Sheets'teki son yedek veriyi çekerek yerel verilerin üzerine yazar."):
                    cloud_data, msg = pull_from_sheets()
                    if cloud_data:
                        from utils.data_handler import save_data
                        save_data(cloud_data)
                        st.toast("Veriler buluttan geri yüklendi!", icon="✅")
                        st.rerun()
                    else:
                        st.error("Geri Yükleme Hatası")
                        st.toast(msg, icon="❌")
        else:
            st.markdown("""
            <div style="background: rgba(239, 68, 68, 0.05); padding: 10px; border-radius: 8px; border: 1px solid rgba(239, 68, 68, 0.15); margin-bottom: 10px;">
                <div style="font-size: 11px; color: #ef4444; font-weight: bold; text-align: center;">⚠️ BAĞLANTI BULUNAMADI</div>
            </div>
            """, unsafe_allow_html=True)
        
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

    active_owner_name = data.get("active_owner", "Deniz Deviren")
    owner = next((acc for acc in data.get("accounts", []) if acc["name"] == active_owner_name), data.get("owner", {}))
    is_demo_user = (current_user == "demo_erpsim")

    if is_demo_user:
        # Demo/simulation account: show a clean corporate profile without personal social links
        owner_company = owner.get('company', 'Aura Yazılım Teknolojileri')
        st.markdown("### 🏢 Aktif Kullanıcı")
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.03);">
            <div style="font-weight: 700; color: white;">{owner.get('name', 'Bilinmiyor')}</div>
            <div style="font-size: 12px; color: #667eea; margin-bottom: 6px;">{owner.get('role', '')}</div>
            <div style="font-size: 11px; color: #f59e0b; margin-bottom: 8px; font-weight: 600;">🏢 {owner_company}</div>
            <div style="font-size: 11px; color: #9ca3af; line-height: 1.4;">{owner.get('bio', '')}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Real users: show full profile with social links
        st.markdown("### 👨‍💻 Geliştirici")
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.03);">
            <div style="font-weight: 700; color: white;">{owner.get('name', 'Bilinmiyor')}</div>
            <div style="font-size: 12px; color: #667eea; margin-bottom: 10px;">{owner.get('role', '')}</div>
            <div style="font-size: 11px; color: #9ca3af; margin-bottom: 15px; line-height: 1.4;">{owner.get('bio', '')}</div>
            <div class="developer-social-links" style="display: flex; gap: 10px; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 12px;">
                <a href="mailto:devirendeniz21@gmail.com" target="_blank" title="E-posta Gönder" style="text-decoration: none; display: flex; align-items: center; justify-content: center; width: 34px; height: 34px; border-radius: 8px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.08); color: #e5e7eb; transition: all 0.3s ease;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                        <path d="M0 4a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V4zm2-1a1 1 0 0 0-1 1v.217l7 4.2 7-4.2V4a1 1 0 0 0-1-1H2zm13 2.383-4.758 2.855L15 11.114v-5.73zm-.034 6.878L9.271 8.82 8 9.583 6.728 8.82l-5.694 3.44A1 1 0 0 0 2 13h12a1 1 0 0 0 .966-.739zM1 11.114l4.758-2.876L1 5.383v5.73z"/>
                    </svg>
                </a>
                <a href="https://www.linkedin.com/in/deniz-deviren-160b74297?utm_source=share_via&utm_content=profile&utm_medium=member_android" target="_blank" title="LinkedIn Profili" style="text-decoration: none; display: flex; align-items: center; justify-content: center; width: 34px; height: 34px; border-radius: 8px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.08); color: #e5e7eb; transition: all 0.3s ease;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                        <path d="M0 1.146C0 .513.526 0 1.175 0h13.65C15.474 0 16 .513 16 1.146v13.708c0 .633-.526 1.146-1.175 1.146H1.175C.526 16 0 15.487 0 14.854V1.146zm4.943 12.248V6.169H2.542v7.225h2.401zm-1.2-8.212c.837 0 1.358-.554 1.358-1.248-.015-.709-.52-1.248-1.342-1.248-.822 0-1.359.54-1.359 1.248 0 .694.521 1.248 1.327 1.248h.016zm4.908 8.212V9.359c0-.216.016-.432.08-.586.173-.431.568-.878 1.232-.878.869 0 1.216.662 1.216 1.634v3.865h2.401V9.25c0-2.22-1.184-3.252-2.764-3.252-1.274 0-1.845.7-2.165 1.193v.025h-.016a5.54 5.54 0 0 1 .016-.025V6.169h-2.4c.03.678 0 7.225 0 7.225h2.4z"/>
                    </svg>
                </a>
                <a href="https://www.instagram.com/1denizdeviren" target="_blank" title="Instagram Profili" style="text-decoration: none; display: flex; align-items: center; justify-content: center; width: 34px; height: 34px; border-radius: 8px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.08); color: #e5e7eb; transition: all 0.3s ease;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                        <path d="M8 0C5.829 0 5.556.01 4.703.048 3.85.088 3.269.222 2.76.42a3.917 3.917 0 0 0-1.417.923A3.917 3.917 0 0 0 .42 2.76C.222 3.268.087 3.85.048 4.7.01 5.555 0 5.827 0 8.001c0 2.172.01 2.444.048 3.297.04.853.174 1.433.372 1.941.198.508.462.94.923 1.417.5.4.87.726 1.417.923.508.198 1.088.333 1.94.372.853.038 1.125.048 3.297.048 2.17 0 2.443-.01 3.296-.048.853-.039 1.433-.174 1.94-.372a3.916 3.916 0 0 0 1.417-.923c.5-.4.87-1.18 1.09-1.693.2-.508.33-1.08.369-1.93.038-.853.047-1.125.047-3.297 0-2.17-.01-2.443-.047-3.296-.039-.852-.17-1.433-.369-1.94a3.916 3.916 0 0 0-.923-1.417A3.916 3.916 0 0 0 13.24.42c-.51-.198-1.092-.333-1.943-.372C10.443.01 10.172 0 7.998 0h.003zm-.717 1.442h.718c2.136 0 2.389.007 3.232.046.78.035 1.204.166 1.486.275.373.145.64.319.92.599.28.28.453.546.598.92.11.281.24.705.275 1.485.039.843.047 1.096.047 3.231s-.008 2.389-.047 3.232c-.035.78-.166 1.203-.275 1.485a2.47 2.47 0 0 1-.599.919c-.28.28-.546.453-.92.598-.28.11-.704.24-1.485.276-.843.038-1.096.047-3.232.047s-2.39-.009-3.233-.047c-.78-.036-1.203-.166-1.485-.276a2.478 2.478 0 0 1-.92-.598 2.48 2.48 0 0 1-.6-.92c-.109-.281-.24-.705-.275-1.485-.038-.843-.046-1.096-.046-3.233 0-2.136.008-2.388.046-3.231.036-.78.166-1.204.276-1.486.145-.373.319-.64.599-.92.28-.28.546-.453.92-.598.282-.11.705-.24 1.485-.276.738-.034 1.024-.044 2.515-.045v.002zm4.988 1.328a.96.96 0 1 0 0 1.92.96.96 0 0 0 0-1.92zm-4.27 1.122a4.109 4.109 0 1 0 0 8.217 4.109 4.109 0 0 0 0-8.217zm0 1.441a2.667 2.667 0 1 1 0 5.334 2.667 2.667 0 0 1 0-5.334z"/>
                    </svg>
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    
    # ⚙️ Profil Ayarları (Self-Service)
    with st.expander("⚙️ Profil Ayarları"):
        st.markdown("##### 👤 Bilgilerimi Güncelle")
        current_acc = next((acc for acc in data.get("accounts", []) if acc.get("username") == current_user), None)
        if current_acc:
            with st.form("profile_settings_form"):
                new_uname = st.text_input("Kullanıcı Adı", value=current_acc.get("username", ""))
                new_name = st.text_input("Ad Soyad", value=current_acc.get("name", ""))
                new_pwd = st.text_input("Yeni Şifre", type="password", placeholder="Değiştirmek istemiyorsanız boş bırakın")
                new_pwd_confirm = st.text_input("Şifre Doğrulama", type="password", placeholder="Yeni şifrenizi doğrulayın")
                
                profile_save_btn = st.form_submit_button("💾 Profilimi Güncelle")
                if profile_save_btn:
                    if not new_uname or not new_name:
                        st.error("Kullanıcı Adı ve Ad Soyad alanları boş bırakılamaz.")
                    elif new_pwd and new_pwd != new_pwd_confirm:
                        st.error("Girdiğiniz şifreler uyuşmuyor.")
                    else:
                        # Check unique username, excluding the current account
                        other_exists = any(acc.get("username", "").lower() == new_uname.lower() and acc != current_acc for acc in data.get("accounts", []))
                        if other_exists:
                            st.error("Bu kullanıcı adı başka bir hesap tarafından kullanılıyor.")
                        else:
                            # Update account info
                            old_name = current_acc.get("name")
                            current_acc["username"] = new_uname
                            current_acc["name"] = new_name
                            
                            # If password changed
                            if new_pwd:
                                from utils.encryption import hash_password
                                h_val, s_val = hash_password(new_pwd)
                                current_acc["password_hash"] = h_val
                                current_acc["password_salt"] = s_val
                                if "password" in current_acc:
                                    del current_acc["password"]
                            
                            # Update active owner name in data
                            if data.get("active_owner") == old_name:
                                data["active_owner"] = new_name
                            
                            # Also update names of team members in team array if names match!
                            for member in data.get("team", []):
                                if member.get("name") == old_name:
                                    member["name"] = new_name
                            
                            # Also update owner of projects/tasks/logs if names match
                            for p in data.get("projects", []):
                                if p.get("owner_name") == old_name:
                                    p["owner_name"] = new_name
                                if p.get("team") and old_name in p["team"]:
                                    p["team"] = [new_name if t == old_name else t for t in p["team"]]
                            
                            for t in data.get("tasks", []):
                                if t.get("assignee") == old_name:
                                    t["assignee"] = new_name
                                if t.get("owner_name") == old_name:
                                    t["owner_name"] = new_name
                                    
                            for fl in data.get("finance", {}).get("transactions", []):
                                if fl.get("spent_by") == old_name:
                                    fl["spent_by"] = new_name
                                    
                            for act in data.get("activities", []):
                                if act.get("spent_by") == old_name:
                                    act["spent_by"] = new_name
                                    
                            save_data(data)
                            st.session_state["logged_in_user"] = new_uname
                            st.query_params["user"] = new_uname
                            st.success("Profiliniz başarıyla güncellendi!")
                            st.rerun()

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    if st.button("🔒 Oturumu Kapat", use_container_width=True, type="secondary"):
        st.session_state["logged_in_user"] = None
        st.query_params.pop("user", None)
        st.toast("Oturum güvenli bir şekilde kapatıldı.", icon="🔒")
        st.rerun()

# ==========================================
# ANA AKIŞ (ROUTING)
# ==========================================

# Her sayfa değişiminde pencereyi en yukarı kaydır (Streamlit Scroll Bug Fix - Kesin Çözüm)
# Akıllı Kontrol: Iframe her zaman DOM'da kalır (böylece layout shift / yukarı atma bug'ı yaşanmaz).
# Yalnızca sayfa değiştiğinde HTML içeriği değiştiği için Streamlit iframe'i baştan yaratır ve scroll sıfırlanır.
import streamlit.components.v1 as components

components.html(
    f"""
    <script>
        function resetScroll() {{
            try {{
                var doc = window.parent.document;
                // Ana scroll container'ları
                var selectors = [
                    '.main',
                    '.block-container',
                    '[data-testid="stMainViewContainer"]',
                    '[data-testid="stAppViewContainer"]',
                    '[data-testid="stMain"]',
                    'section.main'
                ];
                selectors.forEach(function(selector) {{
                    var el = doc.querySelector(selector);
                    if (el) {{
                        el.scrollTop = 0;
                    }}
                }});
                // Genel pencere scroll'unu sıfırla
                window.parent.scrollTo(0, 0);
                doc.documentElement.scrollTop = 0;
                doc.body.scrollTop = 0;
            }} catch (e) {{
                console.error("Scroll reset hatasi:", e);
            }}
        }}
        
        // Hızlı tetikleyiciler (İlk 300ms içinde tamamlanır, kaydırma hissini bozmaz)
        resetScroll();
        var intervals = [5, 20, 50, 100, 200, 300];
        intervals.forEach(function(t) {{
            setTimeout(resetScroll, t);
        }});

        // -------------------------------------------------------------
        // Global Keyboard Shortcut: Ctrl + S (or Cmd + S on Mac)
        // -------------------------------------------------------------
        window.parent.document.addEventListener('keydown', function(e) {
            if ((window.navigator.platform.match("Mac") ? e.metaKey : e.ctrlKey) && e.key === 's') {
                e.preventDefault();
                
                // Show a premium toast on the parent document
                showToast("💾 DeDev Veritabanı ve Bulut Senkronizasyonu Kaydedildi!");
                
                // Find and click the form submit button if inside an active form
                var submitButtons = window.parent.document.querySelectorAll('button[data-testid="stFormSubmitButton"]');
                if (submitButtons.length > 0) {
                    submitButtons[submitButtons.length - 1].click();
                }
            }
        });

        // -------------------------------------------------------------
        // Auto-Save / Auto-Sync Timer (10 Seconds)
        // -------------------------------------------------------------
        if (!window.dedevAutosaveInitialized) {
            window.dedevAutosaveInitialized = true;
            setInterval(function() {
                var submitButtons = window.parent.document.querySelectorAll('button[data-testid="stFormSubmitButton"]');
                if (submitButtons.length > 0) {
                    submitButtons[submitButtons.length - 1].click();
                    showToast("🔄 Otomatik Kaydedildi (Autosave)");
                } else {
                    showHeartbeat();
                }
            }, 10000);
        }

        function showToast(text) {
            var doc = window.parent.document;
            var toast = doc.getElementById('dedev-toast');
            if (!toast) {
                toast = doc.createElement('div');
                toast.id = 'dedev-toast';
                toast.style.position = 'fixed';
                toast.style.top = '20px';
                toast.style.right = '20px';
                toast.style.background = 'rgba(16, 185, 129, 0.95)';
                toast.style.color = 'white';
                toast.style.padding = '12px 24px';
                toast.style.borderRadius = '10px';
                toast.style.fontFamily = "'Inter', sans-serif";
                toast.style.fontSize = '13px';
                toast.style.fontWeight = 'bold';
                toast.style.zIndex = '999999';
                toast.style.boxShadow = '0 10px 25px rgba(16, 185, 129, 0.4)';
                toast.style.border = '1px solid rgba(255,255,255,0.1)';
                toast.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
                doc.body.appendChild(toast);
            }
            toast.innerText = text;
            toast.style.opacity = '1';
            toast.style.transform = 'translateY(0)';
            
            setTimeout(function() {
                toast.style.opacity = '0';
                toast.style.transform = 'translateY(-10px)';
            }, 2500);
        }

        function showHeartbeat() {
            var doc = window.parent.document;
            var pulse = doc.getElementById('dedev-pulse');
            if (!pulse) {
                pulse = doc.createElement('div');
                pulse.id = 'dedev-pulse';
                pulse.style.position = 'fixed';
                pulse.style.bottom = '15px';
                pulse.style.right = '20px';
                pulse.style.background = 'rgba(15, 15, 35, 0.8)';
                pulse.style.border = '1px solid rgba(16, 185, 129, 0.3)';
                pulse.style.color = '#10b981';
                pulse.style.padding = '4px 10px';
                pulse.style.borderRadius = '20px';
                pulse.style.fontFamily = "'Inter', sans-serif";
                pulse.style.fontSize = '10px';
                pulse.style.fontWeight = 'bold';
                pulse.style.zIndex = '9999';
                pulse.style.transition = 'opacity 0.5s ease';
                doc.body.appendChild(pulse);
            }
            pulse.innerHTML = '🟢 Otomatik Kaydedildi (Autosaved)';
            pulse.style.opacity = '1';
            setTimeout(function() {
                pulse.style.opacity = '0';
            }, 2000);
        }
    </script>
    <!-- Streamlit Scroll Key: {page} -->
    """,
    height=0,
    width=0
)



if page == "🏠 Dashboard":
    show_dashboard(data)
elif page == "📁 Projeler":
    show_projects(data)
elif page == "📚 Arşiv ve Belgeler":
    show_archive(data)
elif page == "📊 DeDev Findeks Skoru":
    show_portfolio_rating(data)
elif page == "🔒 Gizli Kasa":
    show_secret_vault(data)
elif page == "📋 Kanban Board":
    show_kanban(data)
elif page == "📅 Takvim Görünümü":
    show_calendar(data)
elif page == "📊 Şemalar ve Gantt":
    show_timeline(data)
elif page == "💻 Tech Stack":
    show_techstack(data)
elif page == "👥 Ekip Yönetimi":
    show_team(data)
elif page == "📈 Raporlar":
    show_reports(data)
elif page == "📝 Hızlı Notlar":
    show_notes(data)
elif page == "⏱️ Zaman Takibi":
    show_time_tracking(data)
elif page == "💰 Bütçe & Giderler":
    show_finance(data)
elif page == "⚙️ Admin Paneli":
    show_admin(data)
elif page == "ℹ️ Hakkında & Yasal Uyarı":
    show_about(data)

# Footer
_footer_demo = st.session_state.get("logged_in_user") == "demo_erpsim"
_footer_brand = "Aura Yazılım Teknolojileri" if _footer_demo else "DeDev"
_footer_app = "Aura ERP Yönetim Sistemi" if _footer_demo else "DeDev Project Command Center"
st.markdown(f"""
<div style="position: fixed; bottom: 0; left: 0; right: 0; background: rgba(15, 15, 35, 0.9); backdrop-filter: blur(10px); border-top: 1px solid rgba(255,255,255,0.1); padding: 12px 24px; text-align: center; z-index: 999;">
    <div style="font-size: 12px; color: #6b7280;">
        🚀 <b>{_footer_app}</b> v2.0 • Modular Edition • {_footer_brand} • 2026
    </div>
</div>
""", unsafe_allow_html=True)
