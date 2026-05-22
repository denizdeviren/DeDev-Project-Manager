import streamlit as st
import textwrap

def show_deployments(data):
    st.markdown('<div class="section-title">🔄 CI/CD & Sunucular</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Canlı sistemler, otomatik dağıtımlar ve sunucu durumları</div>', unsafe_allow_html=True)
    
    from utils.data_handler import get_filtered_elements
    active_owner, projects, _, _, _, _, filtered_deps = get_filtered_elements(data)
    project_ids = {p["id"] for p in projects}
    
    if filtered_deps:
        cols = st.columns(2)
        for i, dep in enumerate(filtered_deps):
            proj_name = next((p['name'] for p in projects if p['id'] == dep['project']), dep['project'])
            with cols[i % 2]:
                st.markdown(textwrap.dedent(f"""
                <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 16px; margin-bottom: 16px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                        <span style="font-weight: 700; color: white; font-size: 18px;">☁️ {dep['platform']}</span>
                        <span style="background: #22c55e22; color: #22c55e; padding: 4px 10px; border-radius: 4px; font-size: 12px; font-weight: 600;">{dep['status']}</span>
                    </div>
                    <div style="font-size: 13px; color: #d1d5db;">Proje: <span style="color: white; font-weight: 500;">{proj_name}</span></div>
                    <div style="font-size: 11px; color: #9ca3af; margin-top: 8px;">Son Dağıtım: {dep['last_deploy']}</div>
                    <div style="margin-top: 12px;">
                        <a href="{dep['url']}" target="_blank" style="color: #667eea; text-decoration: none; font-size: 13px;">🔗 Siteye Git</a>
                    </div>
                </div>
                """), unsafe_allow_html=True)
    else:
        st.info("Henüz deployment yapılandırılmamış.")
