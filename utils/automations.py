import streamlit as st
from datetime import datetime

def run_automations(data):
    """
    Runs configured smart automations on data in-place before saving.
    """
    # Determine dynamic assignee based on logged-in user
    active_user = None
    try:
        active_user = st.session_state.get("logged_in_user")
    except Exception:
        pass
    auto_assignee = "Murat Yıldırım" if active_user == "demo_erpsim" else "Deniz Deviren"

    # 1. Initialize automations state if not present
    if "automations" not in data:
        data["automations"] = [
            {
                "id": "auto_crit",
                "name": "🚨 Kritik Görevleri Ata",
                "description": f"Kritik öncelikli (Critical) bir görev oluşturulduğunda veya güncellendiğinde otomatik olarak {auto_assignee}'e ata.",
                "enabled": True
            },
            {
                "id": "auto_time",
                "name": "⏱️ Tamamlanınca Zaman Kaydet",
                "description": "Bir görev 'Done' (Tamamlandı) durumuna çekildiğinde otomatik olarak Zaman Takibi sayfasına 60 dakikalık (1 saat) çalışma kaydet.",
                "enabled": True
            },
            {
                "id": "auto_milestone",
                "name": "🎯 Son Kilometre Taşını Tamamla",
                "description": "Bir projeye ait tüm görevler 'Done' (Tamamlandı) olduğunda, projenin en son kilometre taşını otomatik olarak 'Tamamlandı' olarak işaretle.",
                "enabled": True
            }
        ]

    # Create key maps for convenience
    rules = {r["id"]: r["enabled"] for r in data["automations"]}
    
    if "activities" not in data:
        data["activities"] = []

    # 2. Rule: Auto-Assign Critical Tasks
    if rules.get("auto_crit"):
        for task in data.get("tasks", []):
            if task.get("priority") == "Critical" and task.get("assignee") != auto_assignee:
                old_assignee = task.get("assignee") or "Atanmamış"
                task["assignee"] = auto_assignee
                
                # Log Activity
                act_msg = f"⚡ [Kritik Görev Otomasyonu] '{task.get('title')}' görevi kritik olduğu için {old_assignee} yerine otomatik olarak {auto_assignee}'e atandı."
                data["activities"].append({
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "text": act_msg,
                    "type": "automation"
                })
                # Show dynamic toast if in streamlit context
                try:
                    st.toast(f"⚡ Görev otomatik atandı: {auto_assignee}", icon="🚨")
                except Exception:
                    pass

    # 3. Rule: Auto Time Logging
    if rules.get("auto_time"):
        for task in data.get("tasks", []):
            if task.get("status") == "Done" and not task.get("time_logged", False):
                task["time_logged"] = True
                
                # Add a time log of 60 mins (1 hour)
                data.setdefault("time_logs", []).append({
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "project_id": task.get("project_id"),
                    "task": f"Otomatik Kayıt: '{task.get('title')}' tamamlandı",
                    "duration": 60
                })
                
                # Log Activity
                act_msg = f"⚡ [Zaman Kayıt Otomasyonu] '{task.get('title')}' görevi tamamlandığı için Zaman Takibi'ne otomatik 1 saatlik çalışma kaydı eklendi."
                data["activities"].append({
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "text": act_msg,
                    "type": "automation"
                })
                try:
                    st.toast(f"⚡ Çalışma süresi eklendi: 1 Saat", icon="⏱️")
                except Exception:
                    pass

    # 4. Rule: Auto Milestone Completion
    if rules.get("auto_milestone"):
        for proj in data.get("projects", []):
            proj_id = proj.get("id")
            milestones = proj.get("milestones", [])
            if not milestones:
                continue
                
            # Find all tasks for this project
            proj_tasks = [t for t in data.get("tasks", []) if t.get("project_id") == proj_id]
            if not proj_tasks:
                continue
                
            # If all tasks are completed
            if all(t.get("status") == "Done" for t in proj_tasks):
                last_milestone = milestones[-1]
                if not last_milestone.get("done", False):
                    last_milestone["done"] = True
                    
                    # Log Activity
                    act_msg = f"⚡ [Kilometre Taşı Otomasyonu] '{proj.get('name')}' projesinin tüm görevleri tamamlandığı için son kilometre taşı '{last_milestone.get('name')}' otomatik olarak tamamlandı."
                    data["activities"].append({
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "text": act_msg,
                        "type": "automation"
                    })
                    try:
                        st.toast(f"⚡ Yol Haritası Güncellendi: Son kilometre taşı tamamlandı!", icon="🎯")
                    except Exception:
                        pass
