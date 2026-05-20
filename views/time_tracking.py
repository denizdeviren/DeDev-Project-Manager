import streamlit as st
import time
from datetime import datetime
from utils.data_handler import save_data

def clean_html(html_str):
    return "\n".join([line.strip() for line in html_str.split("\n")])

def show_time_tracking(data):
    st.markdown('<div class="section-title">⏱️ Pomodoro & Zaman Takibi</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Görevlerine odaklan ve harcadığın süreyi projelerine kaydet</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown('### 🍅 Pomodoro Sayacı')
        
        # State management for timer
        if 'timer_running' not in st.session_state:
            st.session_state.timer_running = False
            st.session_state.time_left = 25 * 60 # 25 mins
        
        # Form out of timer because timer blocks
        selected_proj = st.selectbox("Çalışılan Proje", [p['name'] for p in data.get("projects", [])])
        task_desc = st.text_input("Şu an ne üzerinde çalışıyorsun?")
        
        if st.button("25 Dk Başlat / Sıfırla"):
            st.session_state.timer_running = True
            st.session_state.time_left = 25 * 60
            st.rerun()

        if st.button("Bitir & Kaydet"):
            st.session_state.timer_running = False
            if selected_proj and task_desc:
                proj_id = next((p['id'] for p in data["projects"] if p['name'] == selected_proj), None)
                data.setdefault("time_logs", []).append({
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "project_id": proj_id,
                    "task": task_desc,
                    "duration": 25 # Assuming completed 25 mins for simplicity
                })
                save_data(data)
                st.success("Çalışma süresi kaydedildi!")
            st.session_state.time_left = 25 * 60
            
        mins, secs = divmod(st.session_state.time_left, 60)
        st.markdown(clean_html(f"""
        <div style="background: rgba(2ef,68,68,0.1); border: 2px solid #ef4444; border-radius: 50%; width: 150px; height: 150px; display: flex; align-items: center; justify-content: center; margin: 20px auto;">
            <div style="font-size: 36px; font-weight: bold; color: white;">{mins:02d}:{secs:02d}</div>
        </div>
        """), unsafe_allow_html=True)

    with col2:
        st.markdown('### 📊 Son Çalışma Kayıtları')
        if "time_logs" in data and data["time_logs"]:
            st.markdown("**Çalışma Kayıtları:**")
            for log in reversed(data["time_logs"]):
                p_name = next((p['name'] for p in data["projects"] if p['id'] == log['project_id']), "Bilinmeyen")
                
                # Column structure to separate card and the delete button
                item_col, del_col = st.columns([5, 1])
                
                with item_col:
                    st.markdown(clean_html(f"""
                    <div style="background: rgba(255,255,255,0.05); padding: 12px; border-radius: 8px; border-left: 3px solid #f59e0b; height: 100%;">
                        <div style="display: flex; justify-content: space-between;">
                            <span style="font-weight: 600; color: white;">{log['task']}</span>
                            <span style="color: #f59e0b; font-weight: bold; margin-right: 10px;">{log['duration']} Dk</span>
                        </div>
                        <div style="font-size: 12px; color: #9ca3af; margin-top: 4px;">{p_name} | {log['date']}</div>
                    </div>
                    """), unsafe_allow_html=True)
                
                with del_col:
                    st.write("")  # small spacer
                    if st.button("🗑️", key=f"del_log_{log['date']}_{log['task'][:5]}", help="Kaydı Sil", use_container_width=True):
                        data["time_logs"] = [l for l in data["time_logs"] if not (l["date"] == log["date"] and l["task"] == log["task"] and l["project_id"] == log["project_id"])]
                        save_data(data)
                        st.toast("Çalışma kaydı silindi!", icon="🗑️")
                        st.rerun()
        else:
            st.info("Henüz kaydedilmiş bir çalışma süresi yok.")
