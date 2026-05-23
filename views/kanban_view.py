import streamlit as st
import uuid
from datetime import datetime
from utils.data_handler import save_data, get_filtered_elements
from views.task_details import render_task_details

def clean_html(html_str):
    return "\n".join([line.strip() for line in html_str.split("\n")])

def show_kanban(data):
    st.markdown('<div class="section-title">📋 Kanban Board</div>', unsafe_allow_html=True)
    active_owner, active_projects, active_tasks, _, _, _, _ = get_filtered_elements(data)
    active_project_ids = {p["id"] for p in active_projects}
    
    # -------------------------------------------------------------
    # SECURE VAULT DECRYPTION IN KANBAN
    # -------------------------------------------------------------
    locked_secrets = [p for p in active_projects if p.get("is_secret", False) and p["id"] not in st.session_state.get("unlocked_secrets", {})]
    
    if locked_secrets:
        with st.expander("🔑 Kanban Tahtasında Gizli Projeleri Göster (Şifre Çöz)", expanded=False):
            st.markdown("""
            <div style="background: rgba(239, 68, 68, 0.05); border: 1px dashed rgba(239, 68, 68, 0.2); padding: 15px; border-radius: 12px; margin-bottom: 15px;">
                <span style="font-size: 13px; color: #fca5a5;">🔒 Kasadaki şifreli projelerin görevlerini Kanban tahtasında görebilmek için kasa şifrenizi girin.</span>
            </div>
            """, unsafe_allow_html=True)
            col_dec1, col_dec2 = st.columns([3, 1])
            kanban_pwd = col_dec1.text_input("Gizli Kasa Şifresi:", type="password", key="kanban_pwd_input", placeholder="Şifrenizi yazın...", label_visibility="collapsed")
            dec_btn = col_dec2.button("🔓 Görevleri Göster", key="kanban_dec_btn", use_container_width=True)
            if kanban_pwd:
                from utils.encryption import decrypt_text
                unlocked_count = 0
                for proj in locked_secrets:
                    dec_res = decrypt_text(proj.get('description', ''), kanban_pwd)
                    if dec_res != "ERROR_WRONG_PASSWORD" and dec_res:
                        if "unlocked_secrets" not in st.session_state:
                            st.session_state.unlocked_secrets = {}
                        st.session_state.unlocked_secrets[proj["id"]] = kanban_pwd
                        unlocked_count += 1
                if unlocked_count > 0:
                    st.success(f"🔓 {unlocked_count} Gizli Proje görevi başarıyla deşifre edildi!")
                    st.rerun()
                elif dec_btn:
                    st.error("❌ Eşleşen şifre bulunamadı!")
        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
        
    project_names = ["Tüm Projeler"] + [p['name'] for p in active_projects]
    selected_project = st.selectbox("Proje Filtresi", project_names)
    
    st.markdown("---")
    
    # Yeni Görev Ekle Formu
    st.markdown("### ➕ Yeni Görev Ekle")
    if not active_projects:
        st.info("💡 Görev eklemek için öncelikle '📁 Projeler' sayfasından bu profil için bir proje eklemelisiniz.")
    else:
        with st.form("new_task_form"):
            col1, col2, col_assignee = st.columns([2, 2, 1])
            t_title = col1.text_input("Görev Başlığı", placeholder="Örn: Veritabanı optimizasyonu")
            t_proj = col2.selectbox("İlgili Proje", [p['name'] for p in active_projects])
            
            team_options = [active_owner] + [m['name'] for m in data.get('team', [])]
            t_assignee = col_assignee.selectbox("Atanan Kişi", team_options)
            
            col3, col4 = st.columns(2)
            t_date = col3.date_input("Bitiş Tarihi (Deadline)")
            t_prio = col4.selectbox("Öncelik", ["High", "Medium", "Low", "Critical"])
            
            if st.form_submit_button("Görevi Ekle (To Do)"):
                if t_title:
                    proj_id = next((p['id'] for p in active_projects if p['name'] == t_proj), None)
                    new_task = {
                        "id": f"T-{str(uuid.uuid4())[:6].upper()}",
                        "project_id": proj_id,
                        "title": t_title,
                        "status": "To Do",
                        "priority": t_prio,
                        "date": t_date.strftime("%Y-%m-%d"),
                        "assignee": t_assignee
                    }
                    data["tasks"].append(new_task)
                    
                    # Proje istatistiğini güncelle (KeyError korumalı)
                    for p in data["projects"]:
                        if p["id"] == proj_id:
                            p["tasks_total"] = p.get("tasks_total", 0) + 1
                            break
                            
                    save_data(data)
                    st.success("Görev başarıyla eklendi!")
                    st.rerun()
                else:
                    st.error("Görev başlığı boş olamaz.")
    
    st.markdown("---")
    
    # Kanban Sütunları
    col1, col2, col3 = st.columns(3)
    
    status_columns = {
        "To Do": (col1, "📌", "#f59e0b"),
        "In Progress": (col2, "⚙️", "#3b82f6"),
        "Done": (col3, "✅", "#22c55e")
    }
    
    for status, (col, icon, color) in status_columns.items():
        with col:
            st.markdown(clean_html(f"""
            <div style="background-color: rgba(255,255,255,0.05); padding: 15px; border-radius: 12px; border-top: 4px solid {color}; margin-bottom: 20px;">
                <div style="font-weight: bold; font-size: 16px; margin-bottom: 5px;">{icon} {status}</div>
            </div>
            """), unsafe_allow_html=True)
            
            for task in [t for t in active_tasks if t.get("project_id") in active_project_ids]:
                if task['status'] == status:
                    proj = next((p for p in active_projects if p['id'] == task['project_id']), None)
                    if selected_project != "Tüm Projeler" and (proj is None or proj['name'] != selected_project):
                        continue
                        
                    is_sec = proj.get("is_secret", False) if proj else False
                    is_unlocked = proj['id'] in st.session_state.get("unlocked_secrets", {}) if proj else False
                    
                    if is_sec and not is_unlocked:
                        if status == "To Do":
                            task_title = "🔒 ***************"
                        else:
                            task_title = "🔒 **********"
                        proj_name = "🔒 Şifreli Proje"
                        is_locked = True
                    else:
                        task_title = task['title']
                        proj_name = proj['name'] if proj else "Bilinmiyor"
                        is_locked = False
                        
                    prio_color = "#ef4444" if task['priority'] in ["High", "Critical"] else "#f59e0b" if task['priority'] == "Medium" else "#22c55e"
                    assignee_name = "Şifreli" if is_locked else (task.get("assignee") or "Atanmadı")
                    assignee_initial = "?" if is_locked else (assignee_name[0].upper() if assignee_name and assignee_name != "Atanmadı" else "?")
                    
                    if is_locked:
                        assignee_label = "🔒 Sorumlu: Şifreli"
                    elif status == "Done":
                        assignee_label = f"✅ Tamamlayan: <b>{assignee_name}</b>"
                    else:
                        assignee_label = f"👤 Sorumlu: <b>{assignee_name}</b>"
                        
                    assignee_html = f"""
                    <div style="margin-top: 10px; padding: 6px 10px; border-radius: 8px; background: rgba(102, 126, 234, 0.05); border: 1px solid rgba(255, 255, 255, 0.08); font-size: 11px; color: #a5b4fc; display: flex; align-items: center; gap: 6px;">
                        <span>{assignee_label}</span>
                    </div>
                    """
                    
                    # 1. Dependency checking
                    dep_warning_html = ""
                    dep_id = task.get("depends_on")
                    if dep_id and not is_locked:
                        dep_task = next((t for t in data.get("tasks", []) if t.get("id") == dep_id), None)
                        if dep_task and dep_task.get("status") != "Done":
                            dep_warning_html = f"""
                            <div style="background-color: rgba(239, 68, 68, 0.08); border: 1px solid rgba(239, 68, 68, 0.2); border-radius: 6px; padding: 6px; font-size: 10px; color: #fca5a5; margin-bottom: 8px;">
                                🔗 Önkoşul Bekleniyor: {dep_task.get('title')}
                            </div>
                            """
                            
                    # 2. Sub-tasks progress indicator
                    subtasks_html = ""
                    subtasks = task.get("subtasks", [])
                    if subtasks and not is_locked:
                        completed = sum(1 for st_item in subtasks if st_item.get("done", False))
                        total = len(subtasks)
                        pct = int((completed / total) * 100) if total > 0 else 0
                        subtasks_html = f"""
                        <div style="margin-top: 8px; font-size: 10px; color: #9ca3af; display: flex; justify-content: space-between; align-items: center;">
                            <span>📋 Alt Görevler: {completed}/{total}</span>
                            <span style="font-weight: bold; color: #818cf8;">%{pct}</span>
                        </div>
                        """
                    
                    st.markdown(clean_html(f"""
                    <div style="background-color: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 16px; margin-bottom: 12px; transition: transform 0.2s; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                        {dep_warning_html}
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                            <div style="font-size: 14px; font-weight: 600; color: white;">{task_title}</div>
                            <div title="{assignee_name}" style="background: linear-gradient(135deg, #667eea, #764ba2); width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: bold; color: white; flex-shrink: 0; box-shadow: 0 2px 5px rgba(102,126,234,0.5);">
                                {assignee_initial}
                            </div>
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: center; font-size: 11px;">
                            <span style="color: #9ca3af; background: rgba(255,255,255,0.05); padding: 4px 8px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.1);">{proj_name}</span>
                            <span style="color: {prio_color}; font-weight: 700; background: {prio_color}15; padding: 4px 8px; border-radius: 6px; border: 1px solid {prio_color}40;">{task['priority']}</span>
                        </div>
                        {assignee_html}
                        {subtasks_html}
                    </div>
                    """), unsafe_allow_html=True)
                    
                    # Detaylar & Durum Değiştirme
                    if not is_locked:
                        col_det, col_mov = st.columns(2)
                        with col_det:
                            if st.button("🔍 Detaylar", key=f"det_{task['id']}", use_container_width=True):
                                st.session_state.active_kanban_task_id = task['id']
                                st.rerun()
                                
                        with col_mov:
                            with st.expander("Taşı", expanded=False):
                                new_statuses = [s for s in status_columns.keys() if s != status]
                                for ns in new_statuses:
                                    if st.button(f"{ns}", key=f"move_{task['id']}_{ns}", use_container_width=True):
                                        task['status'] = ns
                                        if ns == "Done":
                                            for p in data["projects"]:
                                                if p["id"] == task["project_id"]:
                                                    p["tasks_completed"] = p.get("tasks_completed", 0) + 1
                                                    break
                                            # Aktivite ekle
                                            data["activities"].insert(0, {
                                                "date": datetime.now().strftime("%Y-%m-%d"),
                                                "time": datetime.now().strftime("%H:%M"),
                                                "action": f"✅ Görev tamamlandı: {task['title']}",
                                                "project": task['project_id']
                                            })
                                        elif status == "Done":
                                            for p in data["projects"]:
                                                if p["id"] == task["project_id"]:
                                                    p["tasks_completed"] = max(0, p.get("tasks_completed", 0) - 1)
                                                    break
                                        save_data(data)
                                        st.rerun()

    # -------------------------------------------------------------
    # DETAILED TASK VIEW DRAWER (BOTTOM OF KANBAN)
    # -------------------------------------------------------------
    active_task_id = st.session_state.get("active_kanban_task_id")
    if active_task_id:
        active_task = next((t for t in active_tasks if t.get("id") == active_task_id), None)
        if active_task:
            st.markdown("---")
            st.markdown("### 📋 Görev Detay Çalışma Alanı")
            col_space, col_close = st.columns([5, 1])
            with col_close:
                if st.button("❌ Detayları Kapat", key="close_kanban_details", use_container_width=True):
                    del st.session_state.active_kanban_task_id
                    st.rerun()
            
            render_task_details(active_task, data)
