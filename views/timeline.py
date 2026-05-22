import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from utils.data_handler import colors_map, get_filtered_elements

def clean_html(html_str):
    return "\n".join([line.strip() for line in html_str.split("\n")])

def show_timeline(data):
    st.markdown('<div class="section-title">📊 Şemalar ve Gantt Analiz Paneli</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Proje yol haritaları, kilometre taşları, iş yükü, bütçe ve zaman efor takibi grafik merkezi</div>', unsafe_allow_html=True)

    # -------------------------------------------------------------
    # GEREKLİ ORTAK VERİ YAPILARININ HAZIRLANMASI & FİLTRELENMESİ
    # -------------------------------------------------------------
    # Filter projects and tasks by the active account profile!
    active_owner, projects, tasks, time_logs, finances, activities, deployments = get_filtered_elements(data)
    
    # 1. Proje Filtreleme & Şifreli Kilitleme Mantığı
    unlocked_secrets = st.session_state.get("unlocked_secrets", {})
    
    visible_projects = []
    locked_project_ids = []
    
    for p in projects:
        is_sec = p.get("is_secret", False)
        is_unlocked = p["id"] in unlocked_secrets
        
        if is_sec and not is_unlocked:
            locked_project_ids.append(p["id"])
            visible_projects.append({
                "id": p["id"],
                "name": f"{p['name']} 🔒 (Şifreli)",
                "start_date": p.get("start_date", datetime.now().strftime("%Y-%m-%d")),
                "end_date": p.get("end_date", datetime.now().strftime("%Y-%m-%d")),
                "progress": 0,
                "status": "Şifreli",
                "is_locked": True,
                "color": "#4b5563"
            })
        else:
            color = colors_map.get(p["name"], "#7c3aed")
            visible_projects.append({
                "id": p["id"],
                "name": f"{p['name']} 🔒" if is_sec else p["name"],
                "start_date": p.get("start_date", datetime.now().strftime("%Y-%m-%d")),
                "end_date": p.get("end_date", datetime.now().strftime("%Y-%m-%d")),
                "progress": p.get("progress", 0),
                "status": p.get("status", "Planning"),
                "category": p.get("category", "Genel"),
                "lines_of_code": p.get("lines_of_code", 0),
                "team": p.get("team", []),
                "is_locked": False,
                "color": color
            })
            
    # Proje ID -> İsim Eşleştirmesi (Grafiklerde kullanmak için)
    proj_id_to_name = {p["id"]: p["name"] for p in visible_projects}

    # 2. Görev Filtreleme (Şifreli projelerin görevleri filtrelenir)
    visible_tasks = [t for t in tasks if t["project_id"] not in locked_project_ids]

    # -------------------------------------------------------------
    # STREAMLIT TABS İLE ORGANİZE GÖRÜNÜM
    # -------------------------------------------------------------
    tab_gantt, tab_progress, tab_financials = st.tabs([
        "📅 Yol Haritaları (Gantt)", 
        "📈 İlerleme & Ekip İş Yükü", 
        "💰 Bütçe, Maliyet & Zaman Eforu"
    ])

    # =============================================================
    # SEKME 1: YOL HARİTALARI (GANTT ŞEMALARI)
    # =============================================================
    with tab_gantt:
        st.markdown('### 🗺️ Proje Gantt Çizelgesi')
        if visible_projects:
            fig_proj_gantt = go.Figure()
            
            # Gantt bar çizimi
            for idx, p in enumerate(visible_projects):
                try:
                    s_dt = datetime.strptime(p["start_date"], "%Y-%m-%d")
                    e_dt = datetime.strptime(p["end_date"], "%Y-%m-%d")
                except Exception:
                    s_dt = datetime.now()
                    e_dt = datetime.now()
                
                # Duration in milliseconds
                duration_ms = max(86400000, (e_dt - s_dt).total_seconds() * 1000)
                
                team_list = ", ".join(p.get("team", [])) if p.get("team") else "Atanmadı"
                fig_proj_gantt.add_trace(go.Bar(
                    name=p["name"],
                    x=[duration_ms],
                    y=[p["name"]],
                    base=[p["start_date"]],
                    orientation='h',
                    marker_color=p["color"],
                    hovertemplate=(
                        f"<b>{p['name']}</b><br>"
                        f"Kategori: {p.get('category', 'Genel')}<br>"
                        f"Zaman Aralığı: {p['start_date']} / {p['end_date']}<br>"
                        f"Kod Boyutu: {p.get('lines_of_code', 0):,} LOC<br>"
                        f"Sorumlu Ekip: {team_list}<br>"
                        f"İlerleme: {p['progress']}%<br>"
                        f"Durum: {p['status']}<extra></extra>"
                    ),
                    showlegend=False
                ))
            
            fig_proj_gantt.update_yaxes(autorange="reversed")
            fig_proj_gantt.update_layout(
                xaxis_type='date',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                height=260 + (len(visible_projects) * 35),
                margin=dict(l=150, r=20, t=30, b=20),
                xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)', zeroline=False),
                yaxis=dict(showgrid=False)
            )
            st.plotly_chart(fig_proj_gantt, use_container_width=True)
        else:
            st.info("Çizelgelenecek herhangi bir proje bulunamadı.")
            
        st.markdown("<hr style='border-color: rgba(255,255,255,0.05); margin: 30px 0;'>", unsafe_allow_html=True)
        
        # -------------------------------------------------------------
        # DİNAMİK VE GELİŞMİŞ GÖREV ZAMAN ÇİZELGESİ (ZAMAN ÖLÇEKLİ)
        # -------------------------------------------------------------
        st.markdown('### 📋 Görev Detaylı Zaman Çizelgesi')
        
        # Timeline Controls
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 12px; margin-bottom: 20px;">
            <div style="font-size: 13px; font-weight: bold; color: #a5b4fc; margin-bottom: 10px;">⏳ Görev Çizelgesi Zaman Filtreleri ve Ölçekleme</div>
        </div>
        """, unsafe_allow_html=True)
        
        col_ctrl1, col_ctrl2 = st.columns([2, 1])
        time_scale = col_ctrl1.radio(
            "Zaman Ölçeği Seçimi:",
            ["Günlük (Gantt)", "Aylık (Yol Haritası)", "Saatlik (Günlük Plan)"],
            horizontal=True,
            key="timeline_scale_select"
        )
        
        # Dynamic project filter
        project_options = ["Tüm Projeler"] + [p["name"] for p in visible_projects if not p.get("is_locked", False)]
        selected_gantt_proj = col_ctrl2.selectbox("Filtrelenecek Proje", project_options, key="timeline_proj_select")
        
        # Apply project filter to tasks
        gantt_tasks = visible_tasks
        if selected_gantt_proj != "Tüm Projeler":
            gantt_proj_id = next((p["id"] for p in projects if p["name"] == selected_gantt_proj), None)
            gantt_tasks = [t for t in gantt_tasks if t["project_id"] == gantt_proj_id]
            
        if time_scale == "Saatlik (Günlük Plan)":
            # ---------------------------------------------------------
            # SAATLİK ZAMAN PLANI (POMODORO & SAATLİK GÜNLÜK AKIŞ)
            # ---------------------------------------------------------
            st.markdown("#### ⏱️ Günlük Çalışma & Saatlik Görev Akışı")
            
            # Fetch dates from time logs, if empty default to today
            log_dates = sorted(list(set(log.get("date", datetime.now().strftime("%Y-%m-%d")) for log in time_logs)), reverse=True)
            if not log_dates:
                log_dates = [datetime.now().strftime("%Y-%m-%d")]
                
            selected_log_date = st.selectbox("Çalışma Tarihi Seçin:", log_dates, key="timeline_log_date_select")
            
            # Filter logs for selected date
            day_logs = [log for log in time_logs if log.get("date") == selected_log_date]
            
            if day_logs:
                fig_hourly = go.Figure()
                
                # We group logs by task name or assignee to draw a horizontal timeline.
                # In each log, we assign a start time. Pomodoro logs do not have explicit start times.
                # We will programmatically structure them starting at 09:00 and cascading forward.
                user_times = {} # Keeps track of active end time for each developer
                
                for log_idx, log in enumerate(day_logs):
                    p_name = proj_id_to_name.get(log.get("project_id"), "Genel")
                    task_name = log.get("task", "Çalışma Seansı")
                    duration_mins = int(log.get("duration", 25))
                    
                    # Since logs might not have an assignee, we assign the active owner
                    dev_name = log.get("assignee", active_owner)
                    if not dev_name:
                        dev_name = active_owner
                        
                    # Calculate start/end time for this block of work
                    if dev_name not in user_times:
                        user_times[dev_name] = datetime.strptime(f"{selected_log_date} 09:00", "%Y-%m-%d %H:%M")
                        
                    s_time = user_times[dev_name]
                    e_time = s_time + timedelta(minutes=duration_mins)
                    
                    # Store end time for next log
                    # Add 10 mins break after each block automatically for realism
                    user_times[dev_name] = e_time + timedelta(minutes=10)
                    
                    s_str = s_time.strftime("%Y-%m-%d %H:%M:%S")
                    e_str = e_time.strftime("%Y-%m-%d %H:%M:%S")
                    dur_ms = duration_mins * 60 * 1000
                    
                    hover_txt = f"<b>{task_name}</b><br>Ekip Üyesi: {dev_name}<br>Proje: {p_name}<br>Süre: {duration_mins} Dakika<br>Zaman: {s_time.strftime('%H:%M')} - {e_time.strftime('%H:%M')}"
                    
                    fig_hourly.add_trace(go.Bar(
                        name=dev_name,
                        x=[dur_ms],
                        y=[dev_name],
                        base=[s_str],
                        orientation='h',
                        marker_color="#3b82f6" if log_idx % 2 == 0 else "#8b5cf6",
                        hovertemplate=f"{hover_txt}<extra></extra>",
                        showlegend=False
                    ))
                    
                fig_hourly.update_yaxes(autorange="reversed")
                fig_hourly.update_layout(
                    xaxis_type='date',
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    height=200 + (len(user_times) * 45),
                    margin=dict(l=150, r=20, t=30, b=20),
                    xaxis=dict(
                        showgrid=True, 
                        gridcolor='rgba(255,255,255,0.06)', 
                        zeroline=False,
                        tickformat="%H:%M",
                        title="Günlük Çalışma Saatleri (09:00'dan İtibaren Kümülatif Akış)"
                    ),
                    yaxis=dict(showgrid=False)
                )
                st.plotly_chart(fig_hourly, use_container_width=True)
            else:
                st.info(f"📅 {selected_log_date} tarihinde kaydedilmiş herhangi bir Pomodoro/Zaman günlük çalışması bulunamadı.")
                
        else:
            # Aylık veya Günlük Görünüm
            if gantt_tasks:
                fig_task_gantt = go.Figure()
                
                # Görevleri bitiş tarihlerine göre sıralayalım
                sorted_tasks = sorted(gantt_tasks, key=lambda x: x.get("date", ""))
                
                # Statüye göre stabil renkler
                status_colors = {
                    "Done": "#10b981",       # Emerald
                    "In Progress": "#f59e0b", # Amber
                    "To Do": "#3b82f6",       # Blue
                    "Testing": "#8b5cf6"      # Purple
                }
                
                for t_idx, t in enumerate(sorted_tasks):
                    p_name = proj_id_to_name.get(t["project_id"], "Bilinmeyen Proje")
                    asg = t.get("assignee", "").strip()
                    if not asg or asg in ["Atanmadı", "Atanmamış", "Atanmış Değil"]:
                        proj = next((p for p in projects if p["id"] == t.get("project_id")), None)
                        assignee_name = proj.get("owner_name") if proj else "Atanmamış"
                    else:
                        assignee_name = asg
                    
                    # Görevin bitiş tarihi task['date']'dir. Başlangıç tarihini 4 gün öncesi varsayıyoruz
                    end_str = t.get("date", datetime.now().strftime("%Y-%m-%d"))
                    try:
                        e_dt = datetime.strptime(end_str, "%Y-%m-%d")
                    except ValueError:
                        e_dt = datetime.now()
                        end_str = e_dt.strftime("%Y-%m-%d")
                        
                    s_dt = e_dt - timedelta(days=4)
                    start_str = s_dt.strftime("%Y-%m-%d")
                    
                    duration_ms = 4 * 86400 * 1000 # 4 gün milisaniye
                    
                    color = status_colors.get(t.get("status", "To Do"), "#6b7280")
                    
                    # Dynamic label showing who is doing the work!
                    task_label = f"{t.get('title')} | 👤 {assignee_name}"
                    
                    task_desc = t.get('description') or "Detaylı açıklama belirtilmemiş."
                    task_priority = t.get('priority', 'Medium')
                    task_effort = t.get('effort') or "Belirtilmedi"
                    
                    fig_task_gantt.add_trace(go.Bar(
                        name=t.get("status", "To Do"),
                        x=[duration_ms],
                        y=[task_label],
                        base=[start_str],
                        orientation='h',
                        marker_color=color,
                        hovertemplate=(
                            f"<b>{t.get('title')}</b><br>"
                            f"Proje: {p_name}<br>"
                            f"Atanan: {assignee_name}<br>"
                            f"Durum: {t.get('status')}<br>"
                            f"Öncelik: {task_priority}<br>"
                            f"Efor Seviyesi: {task_effort} Puan<br>"
                            f"Hedef Tarih: {end_str}<br>"
                            f"Açıklama: {task_desc}<extra></extra>"
                        ),
                        showlegend=False
                    ))
                    
                fig_task_gantt.update_yaxes(autorange="reversed")
                
                # Format X-axis according to monthly or daily scale
                x_axis_config = dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)', zeroline=False)
                if time_scale == "Aylık (Yol Haritası)":
                    x_axis_config["dtick"] = "M1"
                    x_axis_config["tickformat"] = "%B %Y"
                else:
                    x_axis_config["tickformat"] = "%d %b"
                    
                fig_task_gantt.update_layout(
                    xaxis_type='date',
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    height=min(600, 300 + (len(gantt_tasks) * 22)),
                    margin=dict(l=250, r=20, t=30, b=20),
                    xaxis=x_axis_config,
                    yaxis=dict(showgrid=False)
                )
                st.plotly_chart(fig_task_gantt, use_container_width=True)
                
                # Statü lejantı
                st.markdown(clean_html("""
                <div style="display: flex; gap: 20px; justify-content: center; font-size: 12px; margin-top: 10px;">
                    <div><span style="color: #10b981; font-weight: bold;">●</span> Done (Tamamlandı)</div>
                    <div><span style="color: #f59e0b; font-weight: bold;">●</span> In Progress (Devam Ediyor)</div>
                    <div><span style="color: #3b82f6; font-weight: bold;">●</span> To Do (Yapılacak)</div>
                    <div><span style="color: #8b5cf6; font-weight: bold;">●</span> Testing (Test Aşamasında)</div>
                </div>
                """), unsafe_allow_html=True)
            else:
                st.info("Çizelgelenecek aktif bir görev bulunamadı.")

        st.markdown("<hr style='border-color: rgba(255,255,255,0.05); margin: 30px 0;'>", unsafe_allow_html=True)

        # Kilometre Taşları Kartları
        st.markdown('### 🎯 Kilometre Taşı Yol Haritaları')
        for proj in projects:
            is_sec = proj.get("is_secret", False)
            is_unlocked = proj['id'] in unlocked_secrets
            proj_name = f"{proj['name']} 🔒 (Gizli Proje)" if is_sec else proj['name']
            
            milestones = proj.get('milestones', [])
            if not milestones:
                continue
                
            if is_sec and not is_unlocked:
                with st.expander(f"🚀 {proj_name} 🔒 (Şifreli / Kilitli)", expanded=False):
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
            else:
                with st.expander(f"🚀 {proj_name}", expanded=False):
                    for ms in milestones:
                        ms_is_done = ms.get('done', False) or ms.get('status') == 'Completed'
                        done_icon = "✅" if ms_is_done else "⏳"
                        done_color = "#22c55e" if ms_is_done else "#6b7280"
                        done_text = "Tamamlandı" if ms_is_done else "Bekliyor"

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
                            <div style="font-weight: 500; color: {'white' if ms_is_done else '#9ca3af'}; font-size: 14px;">
                                {done_icon} {ms['name']}
                            </div>
                            <div style="font-size: 11px; color: {done_color}; font-weight: 600;">
                                {ms.get('date', '')} • {done_text}
                            </div>
                        </div>
                        """), unsafe_allow_html=True)

    # =============================================================
    # SEKME 2: İLERLEME & EKİP GÖREV DAĞILIMI
    # =============================================================
    with tab_progress:
        col_prog_left, col_prog_right = st.columns(2)
        
        with col_prog_left:
            st.markdown('### 📈 Proje İlerleme Durumları')
            non_locked_projs = [p for p in visible_projects if not p.get("is_locked", False)]
            if non_locked_projs:
                fig_prog_bar = go.Figure()
                
                # Proje isimleri ve yüzdeleri
                names = [p["name"] for p in non_locked_projs]
                progresses = [p["progress"] for p in non_locked_projs]
                colors = [p["color"] for p in non_locked_projs]
                
                fig_prog_bar.add_trace(go.Bar(
                    x=progresses,
                    y=names,
                    orientation='h',
                    marker=dict(
                        color=colors,
                        line=dict(color='rgba(255,255,255,0.1)', width=1)
                    ),
                    text=[f"{prg}%" for prg in progresses],
                    textposition='inside',
                    insidetextanchor='middle',
                    textfont=dict(color='white', size=12, family='Inter'),
                    hovertemplate="<b>%{y}</b><br>İlerleme: %{x}%<extra></extra>"
                ))
                
                fig_prog_bar.update_xaxes(range=[0, 100])
                fig_prog_bar.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    height=280 + (len(non_locked_projs) * 20),
                    margin=dict(l=150, r=20, t=20, b=20),
                    xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)', title="İlerleme Oranı (%)"),
                    yaxis=dict(showgrid=False)
                )
                st.plotly_chart(fig_prog_bar, use_container_width=True)
            else:
                st.info("İlerlemesi çizelgelenecek açık proje bulunamadı.")
                
        with col_prog_right:
            st.markdown('### 👥 Ekip Görev Dağılımı')
            if visible_tasks:
                # Resolve assignee with project owner fallback to prevent "Atanmamış" (unassigned) slice clutter
                resolved_visible_tasks = []
                for t in visible_tasks:
                    t_copy = dict(t)
                    asg = t_copy.get("assignee", "").strip()
                    if not asg or asg == "Atanmamış":
                        proj = next((p for p in projects if p["id"] == t_copy.get("project_id")), None)
                        t_copy["assignee"] = proj.get("owner_name") if proj else "Atanmamış"
                    else:
                        t_copy["assignee"] = asg
                    resolved_visible_tasks.append(t_copy)
                
                # Görevlileri (assignee) çıkarıp sayalım
                assignee_counts = {}
                for t in resolved_visible_tasks:
                    asg = t.get("assignee", "Atanmamış").strip()
                    if not asg:
                        asg = "Atanmamış"
                    assignee_counts[asg] = assignee_counts.get(asg, 0) + 1
                    
                labels = list(assignee_counts.keys())
                values = list(assignee_counts.values())
                
                fig_team_donut = go.Figure(data=[go.Pie(
                    labels=labels,
                    values=values,
                    hole=.4,
                    marker=dict(colors=["#667eea", "#f59e0b", "#10b981", "#ef4444", "#8b5cf6"]),
                    textinfo='value+percent',
                    textfont=dict(size=12, color='white'),
                    hovertemplate="<b>%{label}</b><br>Görev Sayısı: %{value} (%{percent})<extra></extra>"
                )])
                
                fig_team_donut.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    height=300,
                    margin=dict(l=10, r=10, t=10, b=10),
                    legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
                )
                st.plotly_chart(fig_team_donut, use_container_width=True)
            else:
                st.info("Ekip dağılımı için görev bulunamadı.")
 
        st.markdown("<hr style='border-color: rgba(255,255,255,0.05); margin: 30px 0;'>", unsafe_allow_html=True)
        
        st.markdown('### 📊 Proje Bazlı Görev Statü Dağılımı (Stacked)')
        if visible_tasks and non_locked_projs:
            # Proje bazında statü sayılarını çıkaralım
            status_types = ["To Do", "In Progress", "Done"]
            status_colors_map = {
                "To Do": "#3b82f6",
                "In Progress": "#f59e0b",
                "Done": "#10b981"
            }
            
            proj_statuses = {p["name"]: {st: 0 for st in status_types} for p in non_locked_projs}
            
            for t in visible_tasks:
                p_name = proj_id_to_name.get(t["project_id"])
                if p_name in proj_statuses:
                    stt = t.get("status", "To Do")
                    if stt in proj_statuses[p_name]:
                        proj_statuses[p_name][stt] += 1
                        
            fig_stacked = go.Figure()
            
            for stt in status_types:
                y_data = []
                for p in non_locked_projs:
                    y_data.append(proj_statuses[p["name"]][stt])
                    
                fig_stacked.add_trace(go.Bar(
                    name=stt,
                    x=[p["name"] for p in non_locked_projs],
                    y=y_data,
                    marker_color=status_colors_map[stt],
                    hovertemplate=f"Statü: {stt}<br>Görev Sayısı: %{{y}}<extra></extra>"
                ))
                
            fig_stacked.update_layout(
                barmode='stack',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                height=350,
                margin=dict(l=40, r=20, t=30, b=40),
                xaxis=dict(showgrid=False, title="Projeler"),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)', title="Görev Sayısı"),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_stacked, use_container_width=True)
        else:
            st.info("Statü dağılım analizi için yeterli veri bulunamadı.")

    # =============================================================
    # SEKME 3: BÜTÇE, MALİYET & ZAMAN EFORU
    # =============================================================
    with tab_financials:
        col_fin_left, col_fin_right = st.columns(2)
        
        with col_fin_left:
            st.markdown('### 💰 Proje Gider ve Maliyet Analizi')
            if finances:
                # Giderleri projelere göre gruplayalım
                proj_expenses = {}
                for exp in finances:
                    pid = exp.get("project_id")
                    pname = proj_id_to_name.get(pid, "Genel (Tüm Projeler)") if pid else "Genel (Tüm Projeler)"
                    proj_expenses[pname] = proj_expenses.get(pname, 0.0) + float(exp.get("amount", 0.0))
                    
                labels = list(proj_expenses.keys())
                values = list(proj_expenses.values())
                
                fig_fin_pie = go.Figure(data=[go.Pie(
                    labels=labels,
                    values=values,
                    hole=.4,
                    marker=dict(colors=["#ef4444", "#ec4899", "#f43f5e", "#6366f1", "#14b8a6"]),
                    textinfo='value+percent',
                    textfont=dict(size=12, color='white'),
                    hovertemplate="<b>%{label}</b><br>Harcama Tutarı: $%{value:.2f} (%{percent})<extra></extra>"
                )])
                
                fig_fin_pie.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    height=300,
                    margin=dict(l=10, r=10, t=10, b=10),
                    legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
                )
                st.plotly_chart(fig_fin_pie, use_container_width=True)
            else:
                st.markdown(clean_html("""
                <div style="background: rgba(255,255,255,0.02); border: 1px dashed rgba(255,255,255,0.1); border-radius: 12px; padding: 40px 20px; text-align: center; height: 260px; display: flex; flex-direction: column; justify-content: center;">
                    <div style="font-size: 32px; margin-bottom: 10px;">💸</div>
                    <div style="color: #9ca3af; font-size: 13px; font-weight: 500;">Henüz kaydedilmiş harcama maliyeti bulunmuyor.</div>
                    <div style="color: #6b7280; font-size: 11px; margin-top: 5px;">Harcamalarınızı kaydettikten sonra grafik otomatik olarak burada belirecektir.</div>
                </div>
                """), unsafe_allow_html=True)
                
        with col_fin_right:
            st.markdown('### ⏱️ Zaman Takibi ve Efor Gelişimi')
            if time_logs:
                # Eforları tarihe göre sıralayıp kümülatif toplayalım
                logs_by_date = {}
                for log in time_logs:
                    ldt = log.get("date", "")
                    if ldt:
                        logs_by_date[ldt] = logs_by_date.get(ldt, 0) + int(log.get("duration", 25))
                        
                sorted_dates = sorted(list(logs_by_date.keys()))
                
                # Kümülatif toplam hesaplama
                cumulative_effort = []
                running_total = 0
                for d in sorted_dates:
                    running_total += logs_by_date[d]
                    cumulative_effort.append(running_total)
                    
                fig_effort_line = go.Figure()
                
                # Çizgi grafik çizimi
                fig_effort_line.add_trace(go.Scatter(
                    x=sorted_dates,
                    y=cumulative_effort,
                    mode='lines+markers',
                    line=dict(color='#f59e0b', width=3),
                    marker=dict(color='#667eea', size=8, line=dict(color='white', width=1.5)),
                    fill='tozeroy',
                    fillcolor='rgba(245, 158, 11, 0.08)',
                    hovertemplate="Tarih: %{x}<br>Kümülatif Efor: %{y} Dakika<extra></extra>"
                ))
                
                fig_effort_line.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    height=300,
                    margin=dict(l=40, r=20, t=10, b=40),
                    xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)', title="Tarih"),
                    yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)', title="Toplam Harcanan Süre (Dk)")
                )
                st.plotly_chart(fig_effort_line, use_container_width=True)
            else:
                st.markdown(clean_html("""
                <div style="background: rgba(255,255,255,0.02); border: 1px dashed rgba(255,255,255,0.1); border-radius: 12px; padding: 40px 20px; text-align: center; height: 260px; display: flex; flex-direction: column; justify-content: center;">
                    <div style="font-size: 32px; margin-bottom: 10px;">⏳</div>
                    <div style="color: #9ca3af; font-size: 13px; font-weight: 500;">Zaman takibi efor verisi bulunamadı.</div>
                    <div style="color: #6b7280; font-size: 11px; margin-top: 5px;">Pomodoro sayacını kullanıp günlüklerinizi kaydettikten sonra efor grafiği burada çizilecektir.</div>
                </div>
                """), unsafe_allow_html=True)
