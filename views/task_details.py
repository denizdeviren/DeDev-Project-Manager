import streamlit as st
from datetime import datetime
from utils.data_handler import save_data

def clean_html(html_str):
    return "\n".join([line.strip() for line in html_str.split("\n")])

def render_task_details(task, data):
    """
    Renders an interactive, premium details panel for a task (Sub-tasks, Comments, and Dependencies).
    Mutates data and calls save_data when updates occur.
    """
    st.markdown(f"""
    <div style="background: rgba(102, 126, 234, 0.05); border: 1px solid rgba(102, 126, 234, 0.2); border-radius: 12px; padding: 20px; margin-bottom: 20px;">
        <h4 style="margin: 0; color: white;">🔍 Görev Detayları: {task.get('title')}</h4>
        <div style="font-size: 13px; color: #9ca3af; margin-top: 5px;">
            <b>ID:</b> {task.get('id')} | <b>Durum:</b> {task.get('status')} | <b>Öncelik:</b> {task.get('priority')} | <b>Bitiş Tarihi:</b> {task.get('date')}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 1. DEPENDENCY CHECK & MANAGEMENT
    st.markdown("### 🔗 Görev Bağımlılığı (Önkoşul)")
    
    # Find list of other tasks in the same project for dependency selection
    project_id = task.get("project_id")
    other_tasks = [t for t in data.get("tasks", []) if t.get("project_id") == project_id and t.get("id") != task.get("id")]
    
    dep_options = ["(Yok)"] + [f"{t.get('id')} - {t.get('title')}" for t in other_tasks]
    current_dep_id = task.get("depends_on")
    
    # Calculate default index
    default_idx = 0
    if current_dep_id:
        for idx, opt in enumerate(dep_options):
            if opt.startswith(current_dep_id):
                default_idx = idx
                break
                
    selected_dep = st.selectbox(
        "Bu görevin başlayabilmesi için tamamlanması gereken önkoşul görev:",
        options=dep_options,
        index=default_idx,
        key=f"dep_sel_{task.get('id')}"
    )
    
    new_dep_id = None
    if selected_dep != "(Yok)":
        new_dep_id = selected_dep.split(" - ")[0]
        
    if new_dep_id != current_dep_id:
        task["depends_on"] = new_dep_id
        save_data(data)
        st.toast("🔗 Görev bağımlılığı güncellendi!", icon="🔗")
        st.rerun()

    # Visual dependency warning
    if current_dep_id:
        dep_task = next((t for t in data.get("tasks", []) if t.get("id") == current_dep_id), None)
        if dep_task:
            is_done = dep_task.get("status") == "Done"
            badge_color = "#22c55e" if is_done else "#ef4444"
            status_text = "Tamamlandı" if is_done else f"Bekleniyor ({dep_task.get('status')})"
            
            st.markdown(clean_html(f"""
            <div style="background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255,255,255,0.05); padding: 12px; border-radius: 8px; margin-bottom: 20px; display: flex; align-items: center; justify-content: space-between;">
                <span style="font-size: 13px; color: #d1d5db;">🔗 Önkoşul Görev: <b>{dep_task.get('title')}</b></span>
                <span style="background: {badge_color}; color: white; font-size: 11px; font-weight: 600; padding: 4px 10px; border-radius: 20px;">{status_text}</span>
            </div>
            """), unsafe_allow_html=True)
            if not is_done:
                st.warning(f"⚠️ Dikkat: Önkoşul görev ('{dep_task.get('title')}') henüz tamamlanmadığı için bu göreve başlanması önerilmez!")

    st.markdown("---")

    # 2. SUB-TASKS (ALT GÖREVLER) MANAGEMENT
    st.markdown("### 📋 Alt Görevler (Sub-tasks)")
    
    subtasks = task.setdefault("subtasks", [])
    
    if subtasks:
        completed = sum(1 for st_item in subtasks if st_item.get("done", False))
        total = len(subtasks)
        progress_val = completed / total
        
        st.progress(progress_val, text=f"İlerleme: %{int(progress_val * 100)} ({completed}/{total})")
        
        # Render each sub-task in columns
        for idx, st_item in enumerate(subtasks):
            col_check, col_del = st.columns([6, 1])
            with col_check:
                checked = st.checkbox(
                    st_item.get("title"), 
                    value=st_item.get("done", False),
                    key=f"chk_st_{task.get('id')}_{idx}"
                )
                if checked != st_item.get("done", False):
                    st_item["done"] = checked
                    save_data(data)
                    st.rerun()
            with col_del:
                if st.button("🗑️", key=f"del_st_{task.get('id')}_{idx}", use_container_width=True):
                    task["subtasks"].pop(idx)
                    save_data(data)
                    st.toast("Alt görev silindi.", icon="🗑️")
                    st.rerun()
    else:
        st.info("Bu göreve ait henüz bir alt görev eklenmemiş.")

    # Form to add a new subtask
    with st.form(key=f"add_subtask_form_{task.get('id')}"):
        col_in, col_btn = st.columns([4, 1])
        new_st_title = col_in.text_input("Yeni Alt Görev Ekle:", placeholder="Örn: Taslak çizimlerin yapılması...", label_visibility="collapsed")
        submitted = col_btn.form_submit_button("➕ Ekle", use_container_width=True)
        if submitted and new_st_title:
            task["subtasks"].append({
                "id": f"ST-{datetime.now().strftime('%M%S%f')[:6]}",
                "title": new_st_title,
                "done": False
            })
            save_data(data)
            st.success("Alt görev eklendi!")
            st.rerun()

    st.markdown("---")

    # 3. COMMENTS (YORUMLAR) THREAD
    st.markdown("### 💬 Görev Yorumları")
    
    comments = task.setdefault("comments", [])
    
    if comments:
        for idx, c_item in enumerate(comments):
            author = c_item.get("author", "Deniz Deviren")
            st.markdown(clean_html(f"""
            <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 12px 15px; border-radius: 8px; margin-bottom: 10px;">
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.04); padding-bottom: 4px; margin-bottom: 6px;">
                    <span style="font-weight: 700; color: #818cf8; font-size: 13px;">👤 {author}</span>
                    <span style="color: #6b7280; font-size: 11px;">⏱️ {c_item.get('date')}</span>
                </div>
                <div style="color: #e5e7eb; font-size: 13px; line-height: 1.4;">
                    {c_item.get('text')}
                </div>
            </div>
            """), unsafe_allow_html=True)
    else:
        st.info("Bu göreve henüz yorum yazılmamış.")

    # Form to add a new comment
    with st.form(key=f"add_comment_form_{task.get('id')}"):
        comment_text = st.text_area("Yeni yorum ekle:", placeholder="Görevin durumu hakkında bilgi yazın...", label_visibility="collapsed")
        col_space, col_btn = st.columns([4, 1])
        c_submitted = col_btn.form_submit_button("✍️ Yorum Yaz", use_container_width=True)
        if c_submitted and comment_text:
            task["comments"].append({
                "id": f"C-{datetime.now().strftime('%M%S%f')[:6]}",
                "author": data.get("owner", {}).get("name", "Deniz Deviren"),
                "text": comment_text,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            save_data(data)
            st.success("Yorum başarıyla eklendi!")
            st.rerun()
