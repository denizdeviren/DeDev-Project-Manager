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
from utils.data_handler import load_data, save_data

# Sayfa (View) Importları
from views.dashboard import show_dashboard
from views.projects_view import show_projects
from views.secret_vault import show_secret_vault
from views.kanban_view import show_kanban
from views.timeline import show_timeline
from views.techstack import show_techstack
from views.reports import show_reports
from views.notes import show_notes
from views.team_view import show_team
from views.time_tracking import show_time_tracking
from views.finance_view import show_finance

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
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
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
# VERİ YÜKLEME
# ==========================================
data = load_data()

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="font-size: 24px; font-weight: 900; background: -webkit-linear-gradient(45deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">DeDev AI</h1>
        <p style="font-size: 12px; color: #9ca3af; letter-spacing: 1px;">COMMAND CENTER V2</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🧭 Navigasyon")
    page = st.radio(
        "",
        [
            "🏠 Dashboard", 
            "📁 Projeler", 
            "🔒 Gizli Kasa",
            "📋 Kanban Board", 
            "📅 Timeline", 
            "💻 Tech Stack", 
            "👥 Ekip Yönetimi",
            "📈 Raporlar", 
            "📝 Hızlı Notlar",
            "⏱️ Zaman Takibi",
            "💰 Bütçe & Giderler"
        ],
        label_visibility="collapsed"
    )
    
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
    st.markdown("### 👨‍💻 Geliştirici")

    
    owner = data.get("owner", {})
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
                    <path d="M8 0C5.829 0 5.556.01 4.703.048 3.85.088 3.269.222 2.76.42a3.917 3.917 0 0 0-1.417.923A3.917 3.917 0 0 0 .42 2.76C.222 3.268.087 3.85.048 4.7.01 5.555 0 5.827 0 8.001c0 2.172.01 2.444.048 3.297.04 852.174 1.433.258 1.94.456a3.916 3.916 0 0 0 1.417.923c.5.197 1.079.33 1.933.369.852.037 1.125.047 3.297.047 2.17 0 2.443-.01 3.296-.047.852-.04 1.433-.172 1.94-.369a3.916 3.916 0 0 0 1.417-.923c.5-.4.87-1.18 1.09-1.693.2-.508.33-1.08.369-1.93.038-.853.047-1.125.047-3.297 0-2.17-.01-2.443-.047-3.296-.039-.852-.17-1.433-.369-1.94a3.916 3.916 0 0 0-.923-1.417A3.916 3.916 0 0 0 13.24.42c-.51-.198-1.092-.333-1.943-.372C10.443.01 10.172 0 7.998 0h.003zm-.717 1.442h.718c2.136 0 2.389.007 3.232.046.78.035 1.204.166 1.486.275.373.145.64.319.92.599.28.28.453.546.598.92.11.281.24.705.275 1.485.039.843.047 1.096.047 3.231s-.008 2.389-.047 3.232c-.035.78-.166 1.203-.275 1.485a2.47 2.47 0 0 1-.599.919c-.28.28-.546.453-.92.598-.28.11-.704.24-1.485.276-.843.038-1.096.047-3.232.047s-2.39-.009-3.233-.047c-.78-.036-1.203-.166-1.485-.276a2.478 2.478 0 0 1-.92-.598 2.48 2.48 0 0 1-.6-.92c-.109-.281-.24-.705-.275-1.485-.038-.843-.046-1.096-.046-3.233 0-2.136.008-2.388.046-3.231.036-.78.166-1.204.276-1.486.145-.373.319-.64.599-.92.28-.28.546-.453.92-.598.282-.11.705-.24 1.485-.276.738-.034 1.024-.044 2.515-.045v.002zm4.988 1.328a.96.96 0 1 0 0 1.92.96.96 0 0 0 0-1.92zm-4.27 1.122a4.109 4.109 0 1 0 0 8.217 4.109 4.109 0 0 0 0-8.217zm0 1.441a2.667 2.667 0 1 1 0 5.334 2.667 2.667 0 0 1 0-5.334z"/>
                </svg>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

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
elif page == "🔒 Gizli Kasa":
    show_secret_vault(data)
elif page == "📋 Kanban Board":
    show_kanban(data)
elif page == "📅 Timeline":
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

# Footer
st.markdown("""
<div style="position: fixed; bottom: 0; left: 0; right: 0; background: rgba(15, 15, 35, 0.9); backdrop-filter: blur(10px); border-top: 1px solid rgba(255,255,255,0.1); padding: 12px 24px; text-align: center; z-index: 999;">
    <div style="font-size: 12px; color: #6b7280;">
        🚀 <b>DeDev Project Command Center</b> v2.0 • Modular Edition • Made by Deniz Deviren • 2026
    </div>
</div>
""", unsafe_allow_html=True)
