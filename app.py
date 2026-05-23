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
    # Inject JavaScript to tag parent document body as active for isolated scoping
    st.markdown("""
    <script>
        try {
            window.parent.document.body.classList.add('login-page-active');
        } catch (e) {
            console.error("Failed to inject login page class", e);
        }
    </script>
    """, unsafe_allow_html=True)

    # Scoped Premium Cyberpunk & 3D CSS Styles
    st.markdown("""
    <style>
    /* =============================================================
       1. GLOBAL VIEWER & BACKGROUND Overrides (Scoped to Login Page)
       ============================================================= */
    .login-page-active .stApp {
        background: radial-gradient(circle at 50% 50%, #0d0d21 0%, #050510 100%) !important;
        overflow: hidden !important;
        position: relative !important;
    }

    /* Cyberpunk Grid Scroll Animation */
    .login-bg-grid {
        position: fixed;
        top: -50%; left: -50%; width: 200vw; height: 200vh;
        background-image: 
            linear-gradient(rgba(99, 102, 241, 0.05) 1.5px, transparent 1.5px),
            linear-gradient(90deg, rgba(99, 102, 241, 0.05) 1.5px, transparent 1.5px);
        background-size: 60px 60px;
        background-position: center;
        pointer-events: none;
        z-index: 1;
        transform: perspective(600px) rotateX(45deg) translateY(-200px) translateZ(-150px);
        opacity: 0.7;
        animation: gridScroll 35s linear infinite;
    }
    
    @keyframes gridScroll {
        0% { background-position: 0 0; }
        100% { background-position: 0 1000px; }
    }

    /* Floating Deep Space Neon Orbs */
    .orb-container {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        pointer-events: none;
        z-index: 2;
        overflow: hidden;
    }
    
    .login-orb {
        position: absolute;
        border-radius: 50%;
        filter: blur(100px);
        opacity: 0.14;
        animation: floatOrb 20s ease-in-out infinite alternate;
    }
    
    .orb-indigo {
        width: 450px; height: 450px;
        background: radial-gradient(circle, #6366f1, #312e81);
        top: 10%; left: 10%;
        animation-duration: 30s;
    }
    
    .orb-pink {
        width: 500px; height: 500px;
        background: radial-gradient(circle, #ec4899, #500724);
        bottom: 10%; right: 10%;
        animation-duration: 25s;
        animation-delay: -5s;
    }
    
    .orb-emerald {
        width: 380px; height: 380px;
        background: radial-gradient(circle, #10b981, #064e3b);
        top: 40%; left: 65%;
        animation-duration: 22s;
        animation-delay: -10s;
    }
    
    @keyframes floatOrb {
        0% { transform: translate(0, 0) scale(1); }
        50% { transform: translate(60px, 50px) scale(1.15); }
        100% { transform: translate(-40px, -60px) scale(0.9); }
    }

    /* Outer Streamlit Layout Configurations */
    .login-page-active .block-container {
        perspective: 1500px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        min-height: 85vh !important;
        padding-top: 2rem !important;
        z-index: 10 !important;
    }

    /* =============================================================
       2. 3D GLASSMORPHIC CARD OVERRIDES (Transforming stTabs)
       ============================================================= */
    .login-page-active div.stTabs {
        background: rgba(10, 10, 26, 0.45) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 28px !important;
        padding: 40px 35px !important;
        backdrop-filter: blur(35px) !important;
        box-shadow: 
            0 35px 70px rgba(0, 0, 0, 0.55), 
            0 0 50px rgba(99, 102, 241, 0.12),
            inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
        transform: perspective(1000px) rotateX(8deg) rotateY(-10deg) translateZ(0);
        transform-style: preserve-3d !important;
        transition: transform 0.12s cubic-bezier(0.25, 1, 0.5, 1), border-color 0.4s ease, box-shadow 0.6s ease !important;
        width: 100% !important;
        max-width: 480px !important;
        margin: 0 auto !important;
        position: relative !important;
        z-index: 100 !important;
    }
    
    .login-page-active div.stTabs:hover {
        border-color: rgba(129, 140, 248, 0.35) !important;
        box-shadow: 
            0 45px 90px rgba(0, 0, 0, 0.65), 
            0 0 65px rgba(99, 102, 241, 0.22),
            inset 0 1px 0 rgba(255, 255, 255, 0.15) !important;
    }

    /* Strip stForm defaults so it integrates seamlessly on the Card */
    .login-page-active [data-testid="stForm"] {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        box-shadow: none !important;
        transform: none !important;
        transform-style: preserve-3d !important;
    }

    /* =============================================================
       3. FLOATING 3D LAYERING & TYPOGRAPHY
       ============================================================= */
    .login-header {
        text-align: center;
        margin-bottom: 25px;
        transform: translateZ(50px) !important;
    }
    
    .float-icon {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
        width: 68px;
        height: 68px;
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 32px;
        color: white;
        margin: 0 auto 16px auto;
        box-shadow: 0 12px 28px rgba(99, 102, 241, 0.38);
        transform: translateZ(75px) rotate(0deg) !important;
        transition: transform 0.6s cubic-bezier(0.165, 0.84, 0.44, 1) !important;
    }
    
    .stTabs:hover .float-icon {
        transform: translateZ(95px) rotate(8deg) !important;
    }
    
    .float-title {
        font-size: 25px;
        font-weight: 800;
        color: white;
        margin: 0 0 6px 0;
        background: linear-gradient(45deg, #c7d2fe, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        transform: translateZ(60px) !important;
        letter-spacing: -0.5px;
    }
    
    .float-subtitle {
        font-size: 13px;
        color: #9ca3af;
        margin: 0;
        transform: translateZ(40px) !important;
        line-height: 1.4;
    }

    /* =============================================================
       4. HIGH-TECH HOLOGRAPHIC CONSOLE TABS
       ============================================================= */
    .login-page-active div.stTabs [data-testid="stTabBar"] {
        background: rgba(0, 0, 0, 0.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 14px !important;
        padding: 5px !important;
        margin-bottom: 30px !important;
        transform: translateZ(35px) !important;
    }
    
    .login-page-active div.stTabs button[data-baseweb="tab"] {
        color: #9ca3af !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        border: none !important;
        border-radius: 9px !important;
        padding: 10px 16px !important;
        background: transparent !important;
        transition: all 0.3s ease !important;
        flex: 1 !important;
        text-align: center !important;
    }
    
    .login-page-active div.stTabs button[aria-selected="true"] {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.18) 0%, rgba(168, 85, 247, 0.18) 100%) !important;
        color: #c7d2fe !important;
        box-shadow: 
            0 4px 12px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.06),
            0 0 10px rgba(99, 102, 241, 0.12) !important;
        border: 1px solid rgba(99, 102, 241, 0.28) !important;
    }
    
    .login-page-active div.stTabs [data-testid="stTabBarHighlight"] {
        display: none !important;
    }

    /* =============================================================
       5. FUTURISTIC INPUT & LABELS CUSTOMIZATION
       ============================================================= */
    .login-page-active .stTextInput > div > div > input {
        background-color: rgba(0, 0, 0, 0.35) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 11px !important;
        color: white !important;
        padding: 12px 16px !important;
        font-size: 14px !important;
        transition: all 0.3s ease !important;
        transform: translateZ(20px) !important;
    }
    
    .login-page-active .stTextInput > div > div > input:focus {
        border-color: #6366f1 !important;
        box-shadow: 
            0 0 15px rgba(99, 102, 241, 0.25),
            inset 0 1px 0 rgba(255, 255, 255, 0.04) !important;
        background-color: rgba(0, 0, 0, 0.5) !important;
    }
    
    .login-page-active .stTextInput label {
        color: #a5b4fc !important;
        font-size: 11px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.8px !important;
        transform: translateZ(25px) !important;
        margin-bottom: 6px !important;
    }
    
    /* Textarea formatting for Registration */
    .login-page-active .stTextArea > div > textarea {
        background-color: rgba(0, 0, 0, 0.35) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 11px !important;
        color: white !important;
        padding: 12px 16px !important;
        font-size: 14px !important;
        transition: all 0.3s ease !important;
        transform: translateZ(20px) !important;
    }
    
    .login-page-active .stTextArea > div > textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 15px rgba(99, 102, 241, 0.25) !important;
        background-color: rgba(0, 0, 0, 0.5) !important;
    }
    
    .login-page-active .stTextArea label {
        color: #a5b4fc !important;
        font-size: 11px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.8px !important;
        transform: translateZ(25px) !important;
        margin-bottom: 6px !important;
    }

    /* =============================================================
       6. SPECTACULAR GRADIENT SUBMIT BUTTONS
       ============================================================= */
    .login-page-active [data-testid="stFormSubmitButton"] button {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 11px !important;
        padding: 13px 24px !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        text-transform: uppercase !important;
        letter-spacing: 1.2px !important;
        box-shadow: 0 8px 24px rgba(99, 102, 241, 0.35) !important;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        transform: translateZ(35px) !important;
        width: 100% !important;
        margin-top: 15px !important;
    }
    
    .login-page-active [data-testid="stFormSubmitButton"] button:hover {
        transform: translateZ(50px) scale(1.025) !important;
        box-shadow: 
            0 12px 32px rgba(99, 102, 241, 0.5),
            0 0 25px rgba(236, 72, 153, 0.3) !important;
        opacity: 1 !important;
    }
    
    .login-page-active [data-testid="stFormSubmitButton"] button:active {
        transform: translateZ(25px) scale(0.97) !important;
    }

    /* =============================================================
       7. CORPORATE FLOATING EXPANDER OVERRIDES
       ============================================================= */
    .login-page-active [data-testid="stExpander"] {
        background: rgba(10, 10, 26, 0.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 18px !important;
        max-width: 480px !important;
        margin: 24px auto 0 auto !important;
        backdrop-filter: blur(20px) !important;
        transform: perspective(1000px) rotateX(4deg) rotateY(-5deg) translateZ(0);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.35) !important;
        transition: all 0.5s ease-out !important;
        z-index: 99 !important;
    }
    
    .login-page-active [data-testid="stExpander"]:hover {
        transform: perspective(1000px) rotateX(0deg) rotateY(0deg) translateZ(8px) !important;
        border-color: rgba(255, 255, 255, 0.1) !important;
        box-shadow: 0 22px 45px rgba(0, 0, 0, 0.45) !important;
    }
    
    .login-page-active [data-testid="stExpander"] details {
        border: none !important;
    }
    
    .login-page-active [data-testid="stExpander"] summary {
        color: #a5b4fc !important;
        font-weight: 600 !important;
        font-size: 13px !important;
    }
    </style>

    <!-- Background Elements Structuring -->
    <div class="login-bg-grid"></div>
    <div class="orb-container">
        <div class="login-orb orb-indigo"></div>
        <div class="login-orb orb-pink"></div>
        <div class="login-orb orb-emerald"></div>
    </div>
    """, unsafe_allow_html=True)
    
    tab_login, tab_register = st.tabs(["🔑 Giriş Yap", "📝 Kayıt Ol"])
    
    with tab_login:
        with st.form("login_form"):
            st.markdown("""
            <div class="login-header">
                <div class="float-icon">🚀</div>
                <h1 class="float-title">DeDev Command Center</h1>
                <p class="float-subtitle">Giriş yapın veya yeni bir simülasyon hesabı oluşturun</p>
            </div>
            """, unsafe_allow_html=True)
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
                        st.toast(f"Hoş geldiniz, {matched_acc['name']}! 👋")
                        st.rerun()
                    else:
                        st.error("Geçersiz kullanıcı adı veya şifre!")
                        
    with tab_register:
        with st.form("register_form"):
            st.markdown("""
            <div class="login-header">
                <div class="float-icon">📝</div>
                <h1 class="float-title">Yeni Kayıt Oluştur</h1>
                <p class="float-subtitle">Kendi izole siber çalışma alanınızı anında başlatın</p>
            </div>
            """, unsafe_allow_html=True)
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
                        import os
                        
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
                        
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
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
        
    # Real-Time 3D Interactive Cursor Tilt Parallax Listener Script
    st.markdown("""
    <script>
        (function() {
            var doc = window.parent.document;
            
            function initTilt() {
                var cards = doc.querySelectorAll('.stTabs');
                var expander = doc.querySelector('[data-testid="stExpander"]');
                
                if (cards.length === 0) return;
                
                doc.addEventListener('mousemove', function(e) {
                    cards.forEach(function(card) {
                        var rect = card.getBoundingClientRect();
                        
                        // Normalized pointer distance from card center (-1 to 1)
                        var cardCenterX = rect.left + rect.width / 2;
                        var cardCenterY = rect.top + rect.height / 2;
                        
                        var dirX = e.clientX - cardCenterX;
                        var dirY = e.clientY - cardCenterY;
                        
                        // Limit angle of tilt to a safe 10 degrees maximum
                        var tiltX = -(dirY / (window.innerHeight / 2)) * 10;
                        var tiltY = (dirX / (window.innerWidth / 2)) * 10;
                        
                        // Update style in 3D perspective space
                        card.style.transform = 'perspective(1000px) rotateX(' + tiltX + 'deg) rotateY(' + tiltY + 'deg) translateZ(0)';
                    });
                    
                    if (expander) {
                        var rectExp = expander.getBoundingClientRect();
                        var expCenterX = rectExp.left + rectExp.width / 2;
                        var expCenterY = rectExp.top + rectExp.height / 2;
                        var dirXExp = e.clientX - expCenterX;
                        var dirYExp = e.clientY - expCenterY;
                        var tiltXExp = -(dirYExp / (window.innerHeight / 2)) * 5;
                        var tiltYExp = (dirXExp / (window.innerWidth / 2)) * 5;
                        expander.style.transform = 'perspective(1000px) rotateX(' + tiltXExp + 'deg) rotateY(' + tiltYExp + 'deg) translateZ(0)';
                    }
                });
            }
            
            // Allow DOM to settle, then initialize
            setTimeout(initTilt, 400);
            
            // Loop checker to catch dynamic React rendering shifts
            var checkInterval = setInterval(function() {
                var cards = doc.querySelectorAll('.stTabs');
                if (cards.length > 0) {
                    initTilt();
                    clearInterval(checkInterval);
                }
            }, 1000);
        })();
    </script>
    """, unsafe_allow_html=True)
    st.stop()

# Inject JavaScript to clean up body tag to ensure no style leakage
st.markdown("""
<script>
    try {
        window.parent.document.body.classList.remove('login-page-active');
    } catch (e) {
        console.error("Failed to remove login page class", e);
    }
</script>
""", unsafe_allow_html=True)

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
    owner_acc = next((acc for acc in data.get("accounts", []) if acc["name"] == active_owner_name), data.get("owner", {}))
    is_demo_user = (current_user == "demo_erpsim")
    
    # Load profile of the actually logged-in user
    current_acc = next((acc for acc in data.get("accounts", []) if acc.get("username") == current_user), None)
    profile_acc = current_acc if current_acc else owner_acc
    profile_name = profile_acc.get("name", "Bilinmiyor")
    profile_role = profile_acc.get("role", "")
    profile_bio = profile_acc.get("bio", "")
    
    # Company is ALWAYS the workspace owner's company!
    workspace_company = owner_acc.get("company", "DeDev" if active_owner_name == "Deniz Deviren" else "Aura Yazılım Teknolojileri")

    if is_demo_user:
        # Demo/simulation account: show a clean corporate profile without personal social links
        owner_company = owner_acc.get('company', 'Aura Yazılım Teknolojileri')
        st.markdown("### 🏢 Aktif Kullanıcı")
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.03);">
            <div style="font-weight: 700; color: white;">{profile_name}</div>
            <div style="font-size: 12px; color: #667eea; margin-bottom: 6px;">{profile_role}</div>
            <div style="font-size: 11px; color: #f59e0b; margin-bottom: 8px; font-weight: 600;">🏢 {owner_company}</div>
            <div style="font-size: 11px; color: #9ca3af; line-height: 1.4;">{profile_bio}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Real users: show full profile of logged-in user with dynamic social links, phone, email
        st.markdown("### 👤 Aktif Kullanıcı")
        
        socials_html = ""
        
        if profile_acc.get("email"):
            socials_html += f"""
            <a href="mailto:{profile_acc['email']}" target="_blank" title="E-posta Gönder" style="text-decoration: none; display: flex; align-items: center; justify-content: center; width: 32px; height: 32px; border-radius: 8px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.08); color: #e5e7eb; transition: all 0.3s ease;">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="currentColor" viewBox="0 0 16 16">
                    <path d="M0 4a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V4zm2-1a1 1 0 0 0-1 1v.217l7 4.2 7-4.2V4a1 1 0 0 0-1-1H2zm13 2.383-4.758 2.855L15 11.114v-5.73zm-.034 6.878L9.271 8.82 8 9.583 6.728 8.82l-5.694 3.44A1 1 0 0 0 2 13h12a1 1 0 0 0 .966-.739zM1 11.114l4.758-2.876L1 5.383v5.73z"/>
                </svg>
            </a>
            """
            
        if profile_acc.get("phone"):
            socials_html += f"""
            <a href="tel:{profile_acc['phone']}" target="_blank" title="Arama Yap" style="text-decoration: none; display: flex; align-items: center; justify-content: center; width: 32px; height: 32px; border-radius: 8px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.08); color: #e5e7eb; transition: all 0.3s ease;">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="currentColor" viewBox="0 0 16 16">
                    <path d="M1.885.511a1.745 1.745 0 0 1 2.61.163L6.29 2.98c.329.423.445.974.315 1.494l-.547 2.19a.678.678 0 0 0 .178.643l2.457 2.457a.678.678 0 0 0 .644.178l2.189-.547a1.745 1.745 0 0 1 1.494.315l2.306 1.794c.829.645.905 1.87.163 2.611l-1.034 1.034c-.74.74-1.846 1.065-2.877.702a18.634 18.634 0 0 1-7.01-4.42 18.634 18.634 0 0 1-4.42-7.009c-.362-1.03-.037-2.137.703-2.877L1.885.511z"/>
                </svg>
            </a>
            """
            
        if profile_acc.get("linkedin"):
            socials_html += f"""
            <a href="{profile_acc['linkedin']}" target="_blank" title="LinkedIn Profili" style="text-decoration: none; display: flex; align-items: center; justify-content: center; width: 32px; height: 32px; border-radius: 8px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.08); color: #e5e7eb; transition: all 0.3s ease;">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="currentColor" viewBox="0 0 16 16">
                    <path d="M0 1.146C0 .513.526 0 1.175 0h13.65C15.474 0 16 .513 16 1.146v13.708c0 .633-.526 1.146-1.175 1.146H1.175C.526 16 0 15.487 0 14.854V1.146zm4.943 12.248V6.169H2.542v7.225h2.401zm-1.2-8.212c.837 0 1.358-.554 1.358-1.248-.015-.709-.52-1.248-1.342-1.248-.822 0-1.359.54-1.359 1.248 0 .694.521 1.248 1.327 1.248h.016zm4.908 8.212V9.359c0-.216.016-.432.08-.586.173-.431.568-.878 1.232-.878.869 0 1.216.662 1.216 1.634v3.865h2.401V9.25c0-2.22-1.184-3.252-2.764-3.252-1.274 0-1.845.7-2.165 1.193v.025h-.016a5.54 5.54 0 0 1 .016-.025V6.169h-2.4c.03.678 0 7.225 0 7.225h2.4z"/>
                </svg>
            </a>
            """
            
        if profile_acc.get("instagram"):
            socials_html += f"""
            <a href="{profile_acc['instagram']}" target="_blank" title="Instagram Profili" style="text-decoration: none; display: flex; align-items: center; justify-content: center; width: 32px; height: 32px; border-radius: 8px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.08); color: #e5e7eb; transition: all 0.3s ease;">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="currentColor" viewBox="0 0 16 16">
                    <path d="M8 0C5.829 0 5.556.01 4.703.048 3.85.088 3.269.222 2.76.42a3.917 3.917 0 0 0-1.417.923A3.917 3.917 0 0 0 .42 2.76C.222 3.268.087 3.85.048 4.7.01 5.555 0 5.827 0 8.001c0 2.172.01 2.444.048 3.297.04.853.174 1.433.372 1.941.198.508.462.94.923 1.417.5.4.87.726 1.417.923.508.198 1.088.333 1.94.372.853.038 1.125.048 3.297.048 2.17 0 2.443-.01 3.296-.048.853-.039 1.433-.174 1.94-.372a3.916 3.916 0 0 0 1.417-.923c.5-.4.87-1.18 1.09-1.693.2-.508.33-1.08.369-1.93.038-.853.047-1.125.047-3.297 0-2.17-.01-2.443-.047-3.296-.039-.852-.17-1.433-.369-1.94a3.916 3.916 0 0 0-.923-1.417A3.916 3.916 0 0 0 13.24.42c-.51-.198-1.092-.333-1.943-.372C10.443.01 10.172 0 7.998 0h.003zm-.717 1.442h.718c2.136 0 2.389.007 3.232.046.78.035 1.204.166 1.486.275.373.145.64.319.92.599.28.28.453.546.598.92.11.281.24.705.275 1.485.039.843.047 1.096.047 3.231s-.008 2.389-.047 3.232c-.035.78-.166 1.203-.275 1.485a2.47 2.47 0 0 1-.599.919c-.28.28-.546.453-.92.598-.28.11-.704.24-1.485.276-.843.038-1.096.047-3.232.047s-2.39-.009-3.233-.047c-.78-.036-1.203-.166-1.485-.276a2.478 2.478 0 0 1-.92-.598 2.48 2.48 0 0 1-.6-.92c-.109-.281-.24-.705-.275-1.485-.038-.843-.046-1.096-.046-3.233 0-2.136.008-2.388.046-3.231.036-.78.166-1.204.276-1.486.145-.373.319-.64.599-.92.28-.28.546-.453.92-.598.282-.11.705-.24 1.485-.276.738-.034 1.024-.044 2.515-.045v.002zm4.988 1.328a.96.96 0 1 0 0 1.92.96.96 0 0 0 0-1.92zm-4.27 1.122a4.109 4.109 0 1 0 0 8.217 4.109 4.109 0 0 0 0-8.217zm0 1.441a2.667 2.667 0 1 1 0 5.334 2.667 2.667 0 0 1 0-5.334z"/>
                </svg>
            </a>
            """
            
        if profile_acc.get("twitter"):
            socials_html += f"""
            <a href="{profile_acc['twitter']}" target="_blank" title="Twitter/X Profili" style="text-decoration: none; display: flex; align-items: center; justify-content: center; width: 32px; height: 32px; border-radius: 8px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.08); color: #e5e7eb; transition: all 0.3s ease;">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="currentColor" viewBox="0 0 16 16">
                    <path d="M12.6.75h2.454l-5.36 6.142L16 15.25h-4.937l-3.867-5.07-4.425 5.07H.316l5.733-6.57L0 .75h5.063l3.495 4.633L12.6.75zm-.86 13.028h1.36L4.323 2.145H2.865z"/>
                </svg>
            </a>
            """
            
        if profile_acc.get("github"):
            socials_html += f"""
            <a href="{profile_acc['github']}" target="_blank" title="GitHub Profili" style="text-decoration: none; display: flex; align-items: center; justify-content: center; width: 32px; height: 32px; border-radius: 8px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.08); color: #e5e7eb; transition: all 0.3s ease;">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="currentColor" viewBox="0 0 16 16">
                    <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"/>
                </svg>
            </a>
            """
            
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.03);">
            <div style="font-weight: 700; color: white;">{profile_name}</div>
            <div style="font-size: 12px; color: #667eea; margin-bottom: 10px;">{profile_role}</div>
            <div style="font-size: 11px; color: #f59e0b; margin-bottom: 8px; font-weight: 600;">🏢 {workspace_company}</div>
            <div style="font-size: 11px; color: #9ca3af; margin-bottom: 15px; line-height: 1.4;">{profile_bio}</div>
            {"<div class='developer-social-links' style='display: flex; gap: 8px; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 12px; margin-top: 10px;'>" + socials_html + "</div>" if socials_html else ""}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    
    # ⚙️ Profil Ayarları (Self-Service)
    with st.expander("⚙️ Profil Ayarları"):
        st.markdown("##### 👤 Kurumsal Profilimi Güncelle")
        current_acc = next((acc for acc in data.get("accounts", []) if acc.get("username") == current_user), None)
        if current_acc:
            with st.form("profile_settings_form"):
                new_uname = st.text_input("Kullanıcı Adı", value=current_acc.get("username", ""))
                new_name = st.text_input("Ad Soyad", value=current_acc.get("name", ""))
                
                col_p1, col_p2 = st.columns(2)
                new_email = col_p1.text_input("E-posta Adresi", value=current_acc.get("email", ""))
                new_phone = col_p2.text_input("Telefon Numarası", value=current_acc.get("phone", ""))
                
                new_address = st.text_area("Fiziksel Adres / Konum", value=current_acc.get("address", ""))
                
                col_p3, col_p4 = st.columns(2)
                new_role = col_p3.text_input("Rol / Ünvan", value=current_acc.get("role", ""))
                new_company = col_p4.text_input("Şirket / Kurum", value=current_acc.get("company", ""))
                
                new_bio = st.text_area("Kısa Biyografi (Maks 300 Karakter)", value=current_acc.get("bio", ""), max_chars=300)
                
                st.markdown("###### 🌐 Sosyal Medya Bağlantıları")
                col_s1, col_s2 = st.columns(2)
                new_linkedin = col_s1.text_input("LinkedIn URL", value=current_acc.get("linkedin", ""))
                new_instagram = col_s2.text_input("Instagram URL", value=current_acc.get("instagram", ""))
                
                col_s3, col_s4 = st.columns(2)
                new_twitter = col_s3.text_input("Twitter / X URL", value=current_acc.get("twitter", ""))
                new_github = col_s4.text_input("GitHub URL", value=current_acc.get("github", ""))
                
                st.markdown("###### 🔒 Giriş Şifresi Güncelleme")
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
                            current_acc["email"] = new_email
                            current_acc["phone"] = new_phone
                            current_acc["address"] = new_address
                            current_acc["role"] = new_role
                            current_acc["company"] = new_company
                            current_acc["bio"] = new_bio
                            current_acc["linkedin"] = new_linkedin
                            current_acc["instagram"] = new_instagram
                            current_acc["twitter"] = new_twitter
                            current_acc["github"] = new_github
                            
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
                            
                            # Also update names, details in team array if names match!
                            for member in data.get("team", []):
                                if member.get("name") == old_name:
                                    member["name"] = new_name
                                    member["email"] = new_email
                                    member["role"] = new_role
                                    member["phone"] = new_phone
                                    member["address"] = new_address
                                    member["bio"] = new_bio
                                    member["linkedin"] = new_linkedin
                                    member["instagram"] = new_instagram
                                    member["twitter"] = new_twitter
                                    member["github"] = new_github
                            
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
    """
    <script>
        function resetScroll() {
            try {
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
                selectors.forEach(function(selector) {
                    var el = doc.querySelector(selector);
                    if (el) {
                        el.scrollTop = 0;
                    }
                });
                // Genel pencere scroll'unu sıfırla
                window.parent.scrollTo(0, 0);
                doc.documentElement.scrollTop = 0;
                doc.body.scrollTop = 0;
            } catch (e) {
                console.error("Scroll reset hatasi:", e);
            }
        }
        
        // Hızlı tetikleyiciler (İlk 300ms içinde tamamlanır, kaydırma hissini bozmaz)
        resetScroll();
        var intervals = [5, 20, 50, 100, 200, 300];
        intervals.forEach(function(t) {
            setTimeout(resetScroll, t);
        });

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
    """.replace("{page}", str(page)),
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
