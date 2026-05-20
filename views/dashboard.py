import streamlit as st
import plotly.graph_objects as go
from datetime import datetime

def clean_html(html_str):
    return "\n".join([line.strip() for line in html_str.split("\n")])

def show_dashboard(data):
    st.markdown('<div class="section-title">📊 Komuta Merkezi (Dashboard)</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Tüm projelere ve metriklerine kuşbakışı genel bakış</div>', unsafe_allow_html=True)
    
    # Initialize session state for secret vault
    unlocked_secrets = st.session_state.get("unlocked_secrets", {})
    
    # Üst Metrikler
    public_projects = [p for p in data.get("projects", []) if not p.get("is_secret", False)]
    secret_projects = [p for p in data.get("projects", []) if p.get("is_secret", False)]
    
    total_pub = len(public_projects)
    total_sec = len(secret_projects)
    
    active_projects = sum(1 for p in data.get("projects", []) if p.get('status') == 'In Progress')
    completed_projects = sum(1 for p in data.get("projects", []) if p.get('status') in ['Production', 'Done'])
    
    # Hide tasks of locked secret projects from public task completion count
    visible_tasks = []
    for t in data.get("tasks", []):
        proj_ref = next((p for p in data.get("projects", []) if p["id"] == t.get("project_id")), None)
        if proj_ref and proj_ref.get("is_secret", False):
            if proj_ref["id"] not in unlocked_secrets:
                continue
        visible_tasks.append(t)
        
    total_tasks = len(visible_tasks)
    completed_tasks = sum(1 for t in visible_tasks if t.get('status') == 'Done')
 
    metrics = [
        ("Genel / Gizli Proje", f"{total_pub} / {total_sec}", "💼"),
        ("Aktif Projeler", active_projects, "🔥"),
        ("Tamamlanan", completed_projects, "✅"),
        ("Görev Başarısı", f"%{int((completed_tasks/total_tasks)*100) if total_tasks else 0}", "🎯")
    ]
 
    cols = st.columns(4)
    for col, (label, val, icon) in zip(cols, metrics):
        with col:
            st.markdown(clean_html(f"""
            <div class="metric-card">
                <div style="font-size: 24px; margin-bottom: 5px;">{icon}</div>
                <div style="color: #9ca3af; font-size: 12px; text-transform: uppercase; letter-spacing: 1px;">{label}</div>
                <div style="color: white; font-size: 28px; font-weight: 800; margin-top: 5px;">{val}</div>
            </div>
            """), unsafe_allow_html=True)
 
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
 
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="section-title" style="font-size: 18px;">🔥 Aktif Geliştirme Durumu</div>', unsafe_allow_html=True)
        # Sadece "In Progress" olanları göster
        active_list = [p for p in data.get("projects", []) if p.get('status') == 'In Progress']
        if active_list:
            for proj in active_list:
                progress = proj.get('progress', 0)
                is_sec = proj.get("is_secret", False)
                
                # Premium styling for locked/unlocked indicators
                if is_sec:
                    lock_indicator = " 🔒" if proj['id'] not in unlocked_secrets else " 🔓"
                    color = "#ef4444"  # Red theme for secret projects
                else:
                    lock_indicator = ""
                    color = "#f59e0b" if progress < 50 else "#3b82f6"
                
                proj_name = f"{proj.get('name', 'Bilinmeyen')}{lock_indicator}"
                
                st.markdown(clean_html(f"""
                <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); padding: 20px; border-radius: 12px; margin-bottom: 15px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                        <span style="font-weight: 600; color: white;">{proj_name}</span>
                        <span style="color: {color}; font-weight: bold;">%{progress}</span>
                    </div>
                    <div style="width: 100%; background-color: rgba(255,255,255,0.1); border-radius: 10px; height: 10px;">
                        <div style="width: {progress}%; background-color: {color}; height: 10px; border-radius: 10px;"></div>
                    </div>
                </div>
                """), unsafe_allow_html=True)
        else:
            st.info("Şu an aktif 'In Progress' proje yok.")
 
    with col2:
        st.markdown('<div class="section-title" style="font-size: 18px;">⚡ Son Aktiviteler</div>', unsafe_allow_html=True)
        st.markdown('<div style="background: rgba(255,255,255,0.02); border-radius: 12px; padding: 15px;">', unsafe_allow_html=True)
        
        recent_activities = data.get("activities", [])[:5]
        for act in recent_activities:
            proj_ref = next((p for p in data.get('projects', []) if p['id'] == act.get('project')), None)
            
            if proj_ref:
                is_sec = proj_ref.get("is_secret", False)
                lock_indicator = " 🔒" if is_sec and proj_ref['id'] not in unlocked_secrets else (" 🔓" if is_sec else "")
                p_name = f"{proj_ref.get('name')}{lock_indicator}"
                indicator_color = "#ef4444" if is_sec else "#3b82f6"
            else:
                p_name = "Genel"
                indicator_color = "#10b981"
                
            st.markdown(clean_html(f"""
            <div style="display: flex; gap: 12px; margin-bottom: 15px; border-left: 2px solid {indicator_color}; padding-left: 10px;">
                <div style="font-size: 11px; color: #6b7280; min-width: 40px; padding-top: 2px;">{act.get('date', datetime.now().strftime('%Y-%m-%d'))[-2:]}/{act.get('date', datetime.now().strftime('%Y-%m-%d'))[-5:-3]}</div>
                <div>
                    <div style="font-size: 13px; color: #e5e7eb;">{act.get('action', '')}</div>
                    <div style="font-size: 11px; color: {indicator_color}; margin-top: 2px;">{p_name}</div>
                </div>
            </div>
            """), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    
    # -------------------------------------------------------------
    # ⚡ SMART AUTOMATIONS CONFIGURATION
    # -------------------------------------------------------------
    st.markdown('<div class="section-title" style="font-size: 18px;">⚡ Akıllı İş Otomasyonları (Smart Automations)</div>', unsafe_allow_html=True)
    
    # Initialize automations list if not present
    if "automations" not in data:
        from utils.automations import run_automations
        run_automations(data)
        from utils.data_handler import save_data
        save_data(data)
        
    with st.expander("⚙️ Arka Plan Otomasyon Kurallarını Yönet", expanded=False):
        st.markdown("""
        <div style="font-size: 13px; color: #9ca3af; margin-bottom: 20px;">
            Aşağıdaki kurallar, projeler veya görevler güncellendiğinde otomatik olarak çalıştırılır. İş süreçlerinizi otomatikleştirmek için dilediğinizi aktif veya pasif yapabilirsiniz.
        </div>
        """, unsafe_allow_html=True)
        
        has_changes = False
        for idx, rule in enumerate(data.get("automations", [])):
            enabled = st.toggle(
                label=rule.get("name"),
                value=rule.get("enabled", True),
                key=f"auto_rule_toggle_{rule.get('id')}",
                help=rule.get("description")
            )
            if enabled != rule.get("enabled"):
                data["automations"][idx]["enabled"] = enabled
                has_changes = True
                
        if has_changes:
            from utils.data_handler import save_data
            save_data(data)
            st.toast("⚡ Otomasyon kuralları başarıyla güncellendi!", icon="⚡")
            st.rerun()
