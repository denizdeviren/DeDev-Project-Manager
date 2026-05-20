import streamlit as st
import calendar
from datetime import datetime
from views.task_details import render_task_details, clean_html
from utils.data_handler import colors_map

def show_calendar(data):
    st.markdown('<div class="section-title">📅 Takvim Görünümü</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Görevlerinizin teslim tarihlerini (deadline) aylık takvim üzerinde izleyin</div>', unsafe_allow_html=True)

    # 1. Gather all tasks and filter secret ones if locked
    unlocked_secrets = st.session_state.get("unlocked_secrets", {})
    all_projects = data.get("projects", [])
    all_tasks = data.get("tasks", [])

    filtered_tasks = []
    for t in all_tasks:
        proj_ref = next((p for p in all_projects if p["id"] == t["project_id"]), None)
        if proj_ref:
            is_sec = proj_ref.get("is_secret", False)
            if is_sec and proj_ref["id"] not in unlocked_secrets:
                continue # Skip locked secret tasks
        filtered_tasks.append(t)

    # 2. Add filters in two columns
    filter_col1, filter_col2, filter_col3 = st.columns([1, 1, 2])
    
    current_year = datetime.now().year
    current_month = datetime.now().month
    
    # Year selectbox
    selected_year = filter_col1.selectbox("Yıl Seçin", [2024, 2025, 2026, 2027], index=2) # Default 2026
    
    # Month selectbox
    months_tr = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
    selected_month = filter_col2.selectbox(
        "Ay Seçin", 
        options=list(range(1, 13)), 
        index=selected_month_idx if (selected_month_idx := current_month - 1) < 12 else 4, 
        format_func=lambda m: months_tr[m-1]
    )

    # Project Filter
    proj_names = ["Tüm Projeler"] + [p["name"] for p in all_projects if not p.get("is_secret") or p["id"] in unlocked_secrets]
    selected_proj_filter = filter_col3.selectbox("Proje Filtresi", proj_names)

    # Filter tasks by project if selected
    if selected_proj_filter != "Tüm Projeler":
        proj_id = next((p["id"] for p in all_projects if p["name"] == selected_proj_filter), None)
        filtered_tasks = [t for t in filtered_tasks if t["project_id"] == proj_id]

    st.markdown("---")

    # 3. Monthly Calendar Generation
    calendar.setfirstweekday(calendar.MONDAY)
    month_matrix = calendar.monthcalendar(selected_year, selected_month)
    
    # Custom styling for calendar grid headers
    st.markdown(clean_html("""
    <style>
        .calendar-header {
            text-align: center;
            font-weight: 700;
            color: #818cf8;
            background: rgba(129, 140, 248, 0.08);
            border: 1px solid rgba(129, 140, 248, 0.15);
            padding: 8px 0;
            border-radius: 6px;
            margin-bottom: 10px;
            font-size: 13px;
        }
        .calendar-cell {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 10px;
            height: 120px;
            padding: 8px;
            margin-bottom: 10px;
            position: relative;
            transition: all 0.2s ease;
        }
        .calendar-cell:hover {
            background: rgba(255, 255, 255, 0.04);
            border-color: rgba(129, 140, 248, 0.3);
            box-shadow: 0 4px 12px rgba(129, 140, 248, 0.08);
        }
        .calendar-cell-today {
            background: rgba(129, 140, 248, 0.06);
            border: 1px solid #818cf8;
        }
        .calendar-cell-empty {
            opacity: 0.15;
            border: 1px solid rgba(255, 255, 255, 0.02);
            border-radius: 10px;
            height: 120px;
            margin-bottom: 10px;
        }
        .calendar-day-num {
            font-weight: 800;
            font-size: 15px;
            color: #9ca3af;
            margin-bottom: 4px;
            display: inline-block;
        }
        .calendar-day-num-today {
            color: #818cf8 !important;
        }
        .task-badge-pill {
            font-size: 9px;
            font-weight: 600;
            padding: 2px 6px;
            border-radius: 4px;
            margin-bottom: 4px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            display: block;
            color: white;
            border-left: 3px solid rgba(255,255,255,0.3);
        }
    </style>
    """), unsafe_allow_html=True)

    # Render day headers
    days_headers = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
    cols_header = st.columns(7)
    for idx, d_name in enumerate(days_headers):
        cols_header[idx].markdown(f'<div class="calendar-header">{d_name}</div>', unsafe_allow_html=True)

    # Determine today's date elements
    today_dt = datetime.now()
    is_current_month_year = (today_dt.year == selected_year and today_dt.month == selected_month)

    tasks_in_selected_month = []

    # Render each week
    for week in month_matrix:
        cols_week = st.columns(7)
        for day_idx in range(7):
            day = week[day_idx]
            
            if day == 0:
                # Empty cell
                cols_week[day_idx].markdown('<div class="calendar-cell-empty"></div>', unsafe_allow_html=True)
            else:
                # Construct date
                date_str = f"{selected_year:04d}-{selected_month:02d}-{day:02d}"
                
                # Find tasks due on this day
                day_tasks = [t for t in filtered_tasks if t.get("date") == date_str]
                
                # Check if this cell is today
                is_today = is_current_month_year and (today_dt.day == day)
                cell_class = "calendar-cell calendar-cell-today" if is_today else "calendar-cell"
                num_class = "calendar-day-num calendar-day-num-today" if is_today else "calendar-day-num"
                
                # Start HTML for cell
                cell_html = f'<div class="{cell_class}"><span class="{num_class}">{day}</span><div style="overflow-y: auto; height: 80px; margin-top: 2px;">'
                
                # Add task badges
                for t in day_tasks:
                    tasks_in_selected_month.append(t)
                    proj_ref = next((p for p in all_projects if p["id"] == t["project_id"]), None)
                    p_name = proj_ref["name"] if proj_ref else "Bilinmeyen"
                    
                    # Determine color mapping
                    color = colors_map.get(p_name, "#4f46e5")
                    
                    # Highlight critical tasks
                    prio_border = "solid 1px red" if t.get("priority") == "Critical" else "none"
                    status_prefix = "✅" if t.get("status") == "Done" else "⚙️" if t.get("status") == "In Progress" else "📌"
                    
                    cell_html += f'<span class="task-badge-pill" style="background-color: {color}; border-left-color: rgba(255,255,255,0.6); outline: {prio_border};" title="{t.get("title")} ({t.get("status")})">{status_prefix} {t.get("title")}</span>'
                    
                cell_html += '</div></div>'
                cols_week[day_idx].markdown(cell_html, unsafe_allow_html=True)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # 4. Interactive task details selector & panel
    if tasks_in_selected_month:
        st.markdown("### 🔍 Görev Detayları & Yönetimi")
        st.markdown("Aşağıdaki listeden takvimde bulunan herhangi bir görevi seçerek alt görevlerini yönetebilir, yorum yazabilir veya bağımlılıklarını yapılandırabilirsiniz.")
        
        # Unique list of tasks sorted by date
        tasks_in_selected_month.sort(key=lambda x: x.get("date", ""))
        
        task_options = []
        task_map = {}
        for t in tasks_in_selected_month:
            proj_ref = next((p for p in all_projects if p["id"] == t["project_id"]), None)
            p_name = proj_ref["name"] if proj_ref else "Bilinmeyen"
            
            opt_label = f"[{t.get('date')}] {t.get('title')} ({p_name}) - [{t.get('status')}]"
            task_options.append(opt_label)
            task_map[opt_label] = t

        selected_task_label = st.selectbox(
            "Detaylarını incelemek istediğiniz görevi seçin:",
            options=task_options,
            key="calendar_task_selector"
        )
        
        if selected_task_label:
            selected_task = task_map[selected_task_label]
            render_task_details(selected_task, data)
    else:
        st.info("Bu ay için planlanmış bir görev teslim tarihi bulunmamaktadır.")
