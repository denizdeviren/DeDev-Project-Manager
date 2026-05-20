import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.data_handler import colors_map

def clean_html(html_str):
    return "\n".join([line.strip() for line in html_str.split("\n")])

def show_timeline(data):
    st.markdown('<div class="section-title">📅 Proje Zaman Çizelgesi</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Tüm genel ve şifreli projelerin yol haritası ve kilometre taşları zaman akışı</div>', unsafe_allow_html=True)

    # 1. Gather all projects for Gantt data
    gantt_data = []
    for proj in data.get('projects', []):
        is_sec = proj.get("is_secret", False)
        is_unlocked = proj['id'] in st.session_state.get("unlocked_secrets", {})
        
        if is_sec and not is_unlocked:
            proj_display_name = f"{proj['name']} 🔒 (Şifreli)"
            gantt_data.append({
                "Proje": proj_display_name,
                "RealName": proj['name'],
                "Başlangıç": proj.get('start_date', datetime.now().strftime("%Y-%m-%d")),
                "Bitiş": proj.get('end_date', datetime.now().strftime("%Y-%m-%d")),
                "İlerleme": "██",
                "Durum": "Şifreli",
                "is_secret": is_sec,
                "is_locked": True
            })
        else:
            proj_display_name = f"{proj['name']} 🔒" if is_sec else proj['name']
            gantt_data.append({
                "Proje": proj_display_name,
                "RealName": proj['name'],
                "Başlangıç": proj.get('start_date', datetime.now().strftime("%Y-%m-%d")),
                "Bitiş": proj.get('end_date', datetime.now().strftime("%Y-%m-%d")),
                "İlerleme": proj.get('progress', 0),
                "Durum": proj.get('status', 'Planning'),
                "is_secret": is_sec,
                "is_locked": False
            })

    # Premium stable color palette for newly added projects
    extra_colors = ["#7c3aed", "#2563eb", "#db2777", "#ea580c", "#0891b2", "#4f46e5", "#059669"]
    
    # 2. Render Project Gantt Chart
    fig = go.Figure()
    unique_projects = list(set([d["Proje"] for d in gantt_data]))
    
    for idx, p_display in enumerate(unique_projects):
        proj_items = [d for d in gantt_data if d["Proje"] == p_display]
        if not proj_items:
            continue
            
        real_name = proj_items[0]["RealName"]
        is_sec = proj_items[0]["is_secret"]
        is_locked = proj_items[0].get("is_locked", False)
        
        # Color mapping logic
        if is_sec:
            color = "#4b5563" if is_locked else "#ef4444" # Gray if locked, crimson red if unlocked
        else:
            color = colors_map.get(real_name)
            if not color:
                # Dynamically choose stable color from palette
                color = extra_colors[idx % len(extra_colors)]
        
        bases = [d["Başlangıç"] for d in proj_items]
        durations = []
        for d in proj_items:
            try:
                s = datetime.strptime(d["Başlangıç"], "%Y-%m-%d")
                e = datetime.strptime(d["Bitiş"], "%Y-%m-%d")
            except Exception:
                s = datetime.now()
                e = datetime.now()
            # Calculate duration in milliseconds
            durations.append(max(86400000, (e - s).total_seconds() * 1000))
            
        fig.add_trace(go.Bar(
            name=p_display,
            x=durations,
            y=[d["Proje"] for d in proj_items],
            base=bases,
            orientation='h',
            marker_color=color,
            hovertemplate="<b>%{y}</b><br>İlerleme: %{customdata[0]}%<br>Durum: %{customdata[1]}<extra></extra>" if not proj_items[0].get("is_locked", False) else "<b>%{y}</b><br>İlerleme: %{customdata[0]}<br>Durum: %{customdata[1]}<extra></extra>",
            customdata=[[d["İlerleme"], d["Durum"]] for d in proj_items]
        ))

    fig.update_yaxes(autorange="reversed")
    fig.update_layout(
        xaxis_type='date',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        height=320 + (len(unique_projects) * 30),
        showlegend=False,
        margin=dict(l=150, r=20, t=30, b=20),
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.08)'),
        yaxis=dict(showgrid=False)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

    # 3. Tasks Gantt Chart (dynamic fallback color)
    st.markdown('<div class="section-title" style="font-size: 18px;">📋 Görev Zaman Çizelgesi (Yapılacaklar)</div>', unsafe_allow_html=True)
    
    task_gantt_data = []
    for task in data.get('tasks', []):
        end_date_str = task.get('date', datetime.now().strftime("%Y-%m-%d"))
        try:
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        except ValueError:
            end_date = datetime.now()
            end_date_str = end_date.strftime("%Y-%m-%d")
            
        start_date = end_date - timedelta(days=4)
        
        proj_ref = next((p for p in data.get('projects', []) if p['id'] == task['project_id']), None)
        if proj_ref:
            is_sec = proj_ref.get("is_secret", False)
            is_unlocked = proj_ref['id'] in st.session_state.get("unlocked_secrets", {})
            if is_sec and not is_unlocked:
                continue # Hide tasks of locked secret projects
            proj_name = f"{proj_ref['name']} 🔒" if is_sec else proj_ref['name']
        else:
            proj_name = "Bilinmeyen Proje"
        
        task_gantt_data.append({
            "Görev": f"{task.get('title')} ({task.get('status')})",
            "Proje": proj_name,
            "Başlangıç": start_date.strftime("%Y-%m-%d"),
            "Bitiş": end_date_str,
            "Durum": task.get('status', 'To Do')
        })
        
    if task_gantt_data:
        task_gantt_data.sort(key=lambda x: x["Başlangıç"])
        
        fig_tasks = go.Figure()
        unique_projs = list(set([d["Proje"] for d in task_gantt_data]))
        for t_idx, p_name in enumerate(unique_projs):
            t_items = [d for d in task_gantt_data if d["Proje"] == p_name]
            bases = [d["Başlangıç"] for d in t_items]
            durations = []
            for d in t_items:
                s = datetime.strptime(d["Başlangıç"], "%Y-%m-%d")
                e = datetime.strptime(d["Bitiş"], "%Y-%m-%d")
                durations.append(max(86400000, (e - s).total_seconds() * 1000))
                
            # Pick a dynamic task color
            if "🔒" in p_name:
                t_color = "#ef4444"
            else:
                t_color = colors_map.get(p_name)
                if not t_color:
                    t_color = extra_colors[t_idx % len(extra_colors)]
                    
            fig_tasks.add_trace(go.Bar(
                name=p_name,
                x=durations,
                y=[d["Görev"] for d in t_items],
                base=bases,
                orientation='h',
                marker_color=t_color,
                hovertemplate="<b>%{y}</b><br>Durum: %{customdata[0]}<extra></extra>",
                customdata=[[d["Durum"]] for d in t_items]
            ))

        fig_tasks.update_yaxes(autorange="reversed")
        fig_tasks.update_layout(
            xaxis_type='date',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            height=min(600, 300 + (len(task_gantt_data) * 20)),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=10, r=20, t=30, b=20),
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.08)'),
            yaxis=dict(showgrid=False)
        )
        st.plotly_chart(fig_tasks, use_container_width=True)
    else:
        st.info("Çizelgelenecek aktif bir görev bulunamadı.")

    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

    # 4. Premium Milestone roadmap list
    st.markdown('<div class="section-title" style="font-size: 18px;">🎯 Kilometre Taşı Detayları</div>', unsafe_allow_html=True)

    all_projs = data.get('projects', [])
    for proj in all_projs:
        is_sec = proj.get("is_secret", False)
        is_unlocked = proj['id'] in st.session_state.get("unlocked_secrets", {})
        proj_name = f"{proj['name']} 🔒 (Gizli Proje)" if is_sec else proj['name']
        
        milestones = proj.get('milestones', [])
        if not milestones:
            continue
            
        if is_sec and not is_unlocked:
            with st.expander(f"🚀 {proj_name} 🔒 (Şifreli Kilitli)", expanded=False):
                st.markdown(clean_html("""
                <div style="
                    background: linear-gradient(135deg, rgba(239, 68, 68, 0.08) 0%, rgba(153, 27, 27, 0.08) 100%);
                    border: 1px dashed rgba(239, 68, 68, 0.3);
                    border-radius: 12px;
                    padding: 20px;
                    text-align: center;
                    margin-bottom: 15px;
                ">
                    <div style="font-size: 32px; margin-bottom: 10px;">🔒</div>
                    <div style="font-weight: 700; color: #fca5a5; font-size: 14px; margin-bottom: 5px;">
                        Uçtan Uca Şifrelenmiş Yol Haritası
                    </div>
                    <div style="font-size: 12px; color: #9ca3af; line-height: 1.5;">
                        Bu projenin kilometre taşları ve yol haritası güvenlik nedeniyle kriptolanmıştır.<br>
                        Detayları görüntülemek için lütfen <b>🔒 Gizli Kasa</b> sayfasından projeyi deşifre edin.
                    </div>
                </div>
                """), unsafe_allow_html=True)
                
                for ms_idx in range(len(milestones)):
                    st.markdown(clean_html(f"""
                    <div style="
                        background: rgba(255,255,255,0.01);
                        border: 1px solid rgba(255,255,255,0.03);
                        border-left: 4px solid #ef4444;
                        border-radius: 8px;
                        padding: 12px 20px;
                        margin-bottom: 8px;
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        opacity: 0.5;
                    ">
                        <div style="font-weight: 500; color: #6b7280; font-size: 13px; font-family: monospace;">
                            🔒 [Aşama {ms_idx + 1}] Kilitli Kilometre Taşı (XOR/AES-256)
                        </div>
                        <div style="font-size: 11px; color: #ef4444; font-weight: 600; font-family: monospace;">
                            ████-██-██ • Şifreli
                        </div>
                    </div>
                    """), unsafe_allow_html=True)
        else:
            with st.expander(f"🚀 {proj_name}", expanded=(proj['id'] == 'PRJ-003')):
                for ms in milestones:
                    done_icon = "✅" if ms.get('done', False) else "⏳"
                    done_color = "#22c55e" if ms.get('done', False) else "#6b7280"
                    done_text = "Tamamlandı" if ms.get('done', False) else "Bekliyor"

                    st.markdown(clean_html(f"""
                    <div style="
                        background: rgba(255,255,255,0.02);
                        border: 1px solid rgba(255,255,255,0.05);
                        border-left: 4px solid {done_color};
                        border-radius: 8px;
                        padding: 12px 20px;
                        margin-bottom: 8px;
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                    ">
                        <div style="font-weight: 500; color: {'white' if ms.get('done', False) else '#9ca3af'}; font-size: 14px;">
                            {done_icon} {ms['name']}
                        </div>
                        <div style="font-size: 11px; color: {done_color}; font-weight: 600;">
                            {ms.get('date', '')} • {done_text}
                        </div>
                    </div>
                    """), unsafe_allow_html=True)
