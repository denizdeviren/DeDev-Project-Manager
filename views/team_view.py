import streamlit as st
import uuid
from utils.data_handler import save_data

def clean_html(html_str):
    return "\n".join([line.strip() for line in html_str.split("\n")])

def show_team(data):
    st.markdown('<div class="section-title">👥 Ekip Yönetimi</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Projelerindeki takım arkadaşların, roller ve iş birlikleri</div>', unsafe_allow_html=True)

    if "team" not in data:
        data["team"] = []

    # Form to add new team member
    with st.form("new_team_member"):
        col1, col2 = st.columns(2)
        m_name = col1.text_input("Ad Soyad", placeholder="Örn: M. Furkan Işık")
        m_role = col2.text_input("Rol / Uzmanlık", placeholder="Örn: Full Stack Developer")
        if st.form_submit_button("Ekip Üyesi Ekle"):
            if m_name:
                data["team"].append({
                    "id": f"USR-{str(uuid.uuid4())[:6].upper()}",
                    "name": m_name,
                    "role": m_role
                })
                save_data(data)
                st.success(f"{m_name} ekibe katıldı!")
                st.rerun()

    st.markdown("---")
    
    # Render Team Grid
    cols = st.columns(4)
    # Himself (Owner)
    with cols[0]:
        st.markdown(clean_html(f"""
        <div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 16px; border: 1px solid rgba(102, 126, 234, 0.5); text-align: center; margin-bottom: 10px;">
            <div style="background: linear-gradient(135deg, #10b981, #047857); width: 60px; height: 60px; border-radius: 50%; margin: 0 auto 10px; display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: bold; color: white; box-shadow: 0 4px 10px rgba(16, 185, 129, 0.3);">
                {data.get('owner', {}).get('name', 'DD')[0].upper()}
            </div>
            <div style="font-weight: 700; color: white; font-size: 16px;">{data.get('owner', {}).get('name', 'Deniz Deviren')} 👑</div>
            <div style="color: #9ca3af; font-size: 12px; margin-top: 5px;">Proje Sahibi</div>
        </div>
        """), unsafe_allow_html=True)
        # Owner cannot be deleted, so we just display placeholder to align button heights
        st.markdown('<div style="height: 38px;"></div>', unsafe_allow_html=True)

    for i, member in enumerate(data.get("team", [])):
        col_idx = (i + 1) % 4
        with cols[col_idx]:
            st.markdown(clean_html(f"""
            <div style="background: rgba(255,255,255,0.03); padding: 20px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.1); text-align: center; margin-bottom: 10px; transition: all 0.3s ease;">
                <div style="background: linear-gradient(135deg, #667eea, #764ba2); width: 60px; height: 60px; border-radius: 50%; margin: 0 auto 10px; display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: bold; color: white; box-shadow: 0 4px 10px rgba(102, 126, 234, 0.3);">
                    {member['name'][0].upper() if member['name'] else '?'}
                </div>
                <div style="font-weight: 700; color: white; font-size: 16px;">{member['name']}</div>
                <div style="color: #9ca3af; font-size: 12px; margin-top: 5px;">{member['role']}</div>
            </div>
            """), unsafe_allow_html=True)
            
            # Delete button for team members
            if st.button("🗑️ Ekipten Çıkar", key=f"del_team_{member['id']}", type="secondary", use_container_width=True):
                data["team"] = [m for m in data["team"] if m["id"] != member["id"]]
                save_data(data)
                st.warning(f"{member['name']} ekipten çıkarıldı!")
                st.rerun()
