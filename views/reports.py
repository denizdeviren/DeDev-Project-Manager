import streamlit as st
import plotly.graph_objects as go
from utils.data_handler import get_filtered_elements

def show_reports(data):
    st.markdown('<div class="section-title">📈 Performans Raporları</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Developer üretkenlik metrikleri, proje bazlı ilerlemeler ve analitikler</div>', unsafe_allow_html=True)
    active_owner, active_projects, active_tasks, _, _, _, _ = get_filtered_elements(data)
    active_project_ids = {p["id"] for p in active_projects}

    # -------------------------------------------------------------
    # SECURE VAULT DECRYPTION IN REPORTS
    # -------------------------------------------------------------
    locked_secrets = [p for p in active_projects if p.get("is_secret", False) and p["id"] not in st.session_state.get("unlocked_secrets", {})]
    
    if locked_secrets:
        with st.expander("🔑 Raporlara Gizli Kasa Projelerini Dahil Et (Şifre Çöz)", expanded=False):
            st.markdown("""
            <div style="background: rgba(239, 68, 68, 0.05); border: 1px dashed rgba(239, 68, 68, 0.2); padding: 15px; border-radius: 12px; margin-bottom: 15px;">
                <span style="font-size: 13px; color: #fca5a5;">🔒 Kasadaki şifreli projelerin grafiklerini ve ekip iş yüklerini raporlara dahil etmek için kasa şifrenizi girin.</span>
            </div>
            """, unsafe_allow_html=True)
            col_dec1, col_dec2 = st.columns([3, 1])
            rep_pwd = col_dec1.text_input("Gizli Kasa Şifresi:", type="password", key="reports_pwd_input", placeholder="Şifrenizi yazın...", label_visibility="collapsed")
            dec_btn = col_dec2.button("🔓 Grafik Kilidini Aç", key="reports_dec_btn", use_container_width=True)
            if dec_btn and rep_pwd:
                from utils.encryption import decrypt_text
                unlocked_count = 0
                for proj in locked_secrets:
                    dec_res = decrypt_text(proj.get('description', ''), rep_pwd)
                    if dec_res != "ERROR_WRONG_PASSWORD" and dec_res:
                        if "unlocked_secrets" not in st.session_state:
                            st.session_state.unlocked_secrets = {}
                        st.session_state.unlocked_secrets[proj["id"]] = rep_pwd
                        unlocked_count += 1
                if unlocked_count > 0:
                    st.success(f"🔓 {unlocked_count} Gizli Proje başarıyla deşifre edildi ve grafiklere eklendi!")
                    st.rerun()
                else:
                    st.error("❌ Eşleşen şifre bulunamadı!")
        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-title" style="font-size: 18px;">🔥 Proje İlerleme Durumu</div>', unsafe_allow_html=True)
        
        if active_projects:
            proj_names = []
            proj_progress = []
            marker_colors = []
            
            status_colors = {
                "Production": "#22c55e",
                "In Progress": "#3b82f6",
                "Planning": "#f59e0b"
            }
            
            for p in active_projects:
                is_sec = p.get("is_secret", False)
                is_unlocked = p["id"] in st.session_state.get("unlocked_secrets", {})
                
                if is_sec and not is_unlocked:
                    name_display = "🔒 Şifreli Proje"
                    proj_names.append(name_display)
                    proj_progress.append(0)
                    marker_colors.append('#4b5563') # Gray color for locked
                else:
                    name_display = f"{p['name']} 🔒" if is_sec else p['name']
                    proj_names.append(name_display)
                    proj_progress.append(p.get('progress', 0))
                    marker_colors.append(status_colors.get(p.get('status', 'Planning'), '#6b7280'))

            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=proj_names,
                y=proj_progress,
                marker_color=marker_colors,
                text=[f"%{p}" for p in proj_progress],
                textposition='outside',
                textfont=dict(color='white', size=11)
            ))
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                height=300,
                margin=dict(t=30, b=40, l=20, r=20),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.08)', range=[0, 115])
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("İlerleme grafiği için kayıtlı proje bulunamadı.")

    with col2:
        st.markdown('<div class="section-title" style="font-size: 18px;">👥 Ekip Görev Dağılımı (İş Yükü)</div>', unsafe_allow_html=True)
        
        # We only count tasks if their project is NOT secret OR is unlocked
        unlocked_secrets = st.session_state.get("unlocked_secrets", {})
        valid_project_ids = []
        for p in active_projects:
            is_sec = p.get("is_secret", False)
            if not is_sec or p["id"] in unlocked_secrets:
                valid_project_ids.append(p["id"])
                
        tasks = active_tasks
        filtered_tasks = [t for t in tasks if t.get("project_id") in valid_project_ids]
        
        # Resolve assignee with project owner fallback to prevent "Atanmamış" (unassigned) slice clutter
        resolved_tasks = []
        for t in filtered_tasks:
            t_copy = dict(t)
            asg = t_copy.get("assignee", "").strip()
            if not asg or asg == "Atanmamış":
                proj = next((p for p in active_projects if p["id"] == t_copy.get("project_id")), None)
                t_copy["assignee"] = proj.get("owner_name") if proj else "Atanmamış"
            else:
                t_copy["assignee"] = asg
            resolved_tasks.append(t_copy)
        
        developer_workload = {}
        for t in resolved_tasks:
            assignee = t.get("assignee", "Atanmamış")
            if assignee:
                developer_workload[assignee] = developer_workload.get(assignee, 0) + 1
                
        if developer_workload:
            dev_names = list(developer_workload.keys())
            dev_task_counts = list(developer_workload.values())
            
            fig_pie = go.Figure(data=[go.Pie(
                labels=dev_names,
                values=dev_task_counts,
                hole=.4,
                marker=dict(colors=["#667eea", "#ec4899", "#22c55e", "#f59e0b", "#a7f3d0"]),
                textinfo='value+percent',
                textfont=dict(color='white', size=11)
            )])
            fig_pie.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                height=300,
                margin=dict(t=30, b=40, l=20, r=20),
                legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("İş yükü grafiği için atanmış görev bulunamadı.")

    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

    st.markdown('<div class="section-title" style="font-size: 18px;">📊 Ekip Görev Tamamlama ve Durum Analizi</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Ekip üyelerinin aktif ve tamamlanan görev durumlarının birikmeli dağılımı</div>', unsafe_allow_html=True)
    
    if resolved_tasks:
        assignees = list(set([t.get("assignee", "Atanmamış") for t in resolved_tasks]))
        status_types = ["To Do", "In Progress", "Done"]
        status_colors = {
            "To Do": "#4b5563",
            "In Progress": "#3b82f6",
            "Done": "#22c55e"
        }
        
        fig_tasks_status = go.Figure()
        for status in status_types:
            counts = []
            for assignee in assignees:
                c = sum(1 for t in resolved_tasks if t.get("assignee", "Atanmamış") == assignee and t.get("status") == status)
                counts.append(c)
            
            fig_tasks_status.add_trace(go.Bar(
                name=status,
                x=assignees,
                y=counts,
                marker_color=status_colors[status],
                text=[str(v) if v > 0 else "" for v in counts],
                textposition='inside',
                textfont=dict(color='white', size=11)
            ))
        
        fig_tasks_status.update_layout(
            barmode='stack',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            height=350,
            margin=dict(t=20, b=40, l=20, r=20),
            legend=dict(orientation="h", yanchor="bottom", y=-0.18, xanchor="center", x=0.5),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.08)')
        )
        st.plotly_chart(fig_tasks_status, use_container_width=True, config={'displayModeBar': False})
    else:
        st.info("Görev durum analizi için veri bulunamadı.")

    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

    owner = next((acc for acc in data.get("accounts", []) if acc["name"] == active_owner), data.get("owner", {}))
    st.markdown(f'<div class="section-title" style="font-size: 18px;">🦅 {owner.get("name", "Geliştirici")} Üretkenlik Metrikleri</div>', unsafe_allow_html=True)

    metrics_col = st.columns(4)
    active_count = len([p for p in active_projects if p.get('status') == 'In Progress'])
    
    solo_metrics = [
        ("⏱️", "Ort. Günlük Çalışma", "7.2 saat", "#667eea"),
        ("🎯", "Aktif Sürat", f"{active_count} Proje", "#f59e0b"),
        ("☕", "Enerji Yakıtı", "3 fincan/gün", "#ec4899"),
        ("🔥", "Streak (Hız)", "48 gün", "#22c55e")
    ]

    for col, (icon, label, value, color) in zip(metrics_col, solo_metrics):
        with col:
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.03); border-radius: 16px; padding: 20px; text-align: center; border: 1px solid rgba(255,255,255,0.05); box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                <div style="font-size: 28px; margin-bottom: 8px;">{icon}</div>
                <div style="font-size: 22px; font-weight: 800; color: {color};">{value}</div>
                <div style="font-size: 11px; color: #9ca3af; margin-top: 4px;">{label}</div>
            </div>
            """, unsafe_allow_html=True)
