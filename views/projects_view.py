import streamlit as st
import uuid
from datetime import datetime
from utils.data_handler import save_data, get_filtered_elements
from views.task_details import render_task_details

def clean_html(html_str):
    return "\n".join([line.strip() for line in html_str.split("\n")])

def show_projects(data):
    active_owner, active_projects, active_tasks, _, _, _, _ = get_filtered_elements(data)
    st.markdown('<div class="section-title">📁 Projeler Command Center</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Tüm genel projelerin, kilometre taşlarının, kod metriklerinin ve ekip atamalarının tek bir merkezden takibi.</div>', unsafe_allow_html=True)
    
    # -------------------------------------------------------------
    # 1. PREMIUM EXECUTIVE METRIC CARDS
    # -------------------------------------------------------------
    public_projects = [p for p in active_projects if not p.get("is_secret", False)]
    total_pub = len(public_projects)
    avg_progress = int(sum(p.get("progress", 0) for p in public_projects) / total_pub) if total_pub else 0
    total_loc = sum(p.get("lines_of_code", 0) for p in public_projects)
    total_commits = sum(p.get("commits", 0) for p in public_projects)
    
    st.markdown(f"""
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 25px;">
        <div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.12) 0%, rgba(118, 75, 162, 0.12) 100%); border: 1px solid rgba(102, 126, 234, 0.2); border-radius: 16px; padding: 20px; text-align: center; box-shadow: 0 4px 20px rgba(0,0,0,0.15);">
            <div style="font-size: 26px; margin-bottom: 6px;">📁</div>
            <div style="font-size: 11px; color: #a5b4fc; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;">Genel Projeler</div>
            <div style="font-size: 28px; font-weight: 800; color: white; margin-top: 5px;">{total_pub}</div>
        </div>
        <div style="background: linear-gradient(135deg, rgba(34, 197, 94, 0.12) 0%, rgba(20, 184, 166, 0.12) 100%); border: 1px solid rgba(34, 197, 94, 0.2); border-radius: 16px; padding: 20px; text-align: center; box-shadow: 0 4px 20px rgba(0,0,0,0.15);">
            <div style="font-size: 26px; margin-bottom: 6px;">📈</div>
            <div style="font-size: 11px; color: #a7f3d0; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;">Ortalama İlerleme</div>
            <div style="font-size: 28px; font-weight: 800; color: white; margin-top: 5px;">%{avg_progress}</div>
        </div>
        <div style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.12) 0%, rgba(147, 51, 234, 0.12) 100%); border: 1px solid rgba(59, 130, 246, 0.2); border-radius: 16px; padding: 20px; text-align: center; box-shadow: 0 4px 20px rgba(0,0,0,0.15);">
            <div style="font-size: 26px; margin-bottom: 6px;">💻</div>
            <div style="font-size: 11px; color: #93c5fd; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;">Toplam Kod Satırı</div>
            <div style="font-size: 28px; font-weight: 800; color: white; margin-top: 5px;">{total_loc:,}</div>
        </div>
        <div style="background: linear-gradient(135deg, rgba(245, 158, 11, 0.12) 0%, rgba(239, 68, 68, 0.12) 100%); border: 1px solid rgba(245, 158, 11, 0.2); border-radius: 16px; padding: 20px; text-align: center; box-shadow: 0 4px 20px rgba(0,0,0,0.15);">
            <div style="font-size: 26px; margin-bottom: 6px;">🔄</div>
            <div style="font-size: 11px; color: #fde047; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;">Toplam Commit</div>
            <div style="font-size: 28px; font-weight: 800; color: white; margin-top: 5px;">{total_commits}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # -------------------------------------------------------------
    # 2. ADVANCED CONTROL PANEL (SEARCH & FILTERS)
    # -------------------------------------------------------------
    st.markdown('<div style="font-size: 16px; font-weight: 700; color: white; margin-top: 10px; margin-bottom: 12px;">🔍 Arama ve Filtre Kontrolleri</div>', unsafe_allow_html=True)
    f_col1, f_col2, f_col3 = st.columns([2, 1, 1])
    search_query = f_col1.text_input("Proje adı, açıklama veya teknoloji ara...", placeholder="Örn: Flutter, Python, Emlak...", label_visibility="collapsed")
    status_filter = f_col2.selectbox("Durum", ["Tümü", "Planning", "In Progress", "Production"])
    priority_filter = f_col3.selectbox("Öncelik", ["Tümü", "Critical", "High", "Medium", "Low"])
    
    # Filter public projects
    filtered_projects = []
    for proj in active_projects:
        if proj.get("is_secret", False):
            continue
        
        # Apply Filter Rules
        if status_filter != "Tümü" and proj.get("status") != status_filter:
            continue
        if priority_filter != "Tümü" and proj.get("priority") != priority_filter:
            continue
        
        if search_query:
            query = search_query.lower()
            name_match = query in proj.get("name", "").lower()
            desc_match = query in proj.get("description", "").lower()
            tech_match = any(query in t.lower() for t in proj.get("tech_stack", []))
            cat_match = query in proj.get("category", "").lower()
            if not (name_match or desc_match or tech_match or cat_match):
                continue
        
        filtered_projects.append(proj)
        
    st.markdown("---")

    if not filtered_projects:
        st.info("Kriterlere uygun genel proje bulunamadı.")
    else:
        for proj in filtered_projects:
            proj_id = proj['id']
            status_color = {
                "Production": "#22c55e",
                "In Progress": "#3b82f6",
                "Planning": "#f59e0b"
            }.get(proj.get('status', 'Planning'), "#6b7280")
            
            priority_color = {
                "Critical": "#ef4444",
                "High": "#f97316",
                "Medium": "#3b82f6",
                "Low": "#10b981"
            }.get(proj.get('priority', 'Medium'), "#6b7280")
            
            progress = proj.get("progress", 0)
            start_date = proj.get("start_date", "")
            end_date = proj.get("end_date", "")
            lines_of_code = proj.get("lines_of_code", 0)
            commits = proj.get("commits", 0)
            
            proj_tasks = [t for t in active_tasks if t.get("project_id") == proj_id]
            tasks_total = len(proj_tasks)
            tasks_completed = sum(1 for t in proj_tasks if t.get("status") == "Done")
            tasks_pct = int((tasks_completed / tasks_total) * 100) if tasks_total else 0
            
            milestones = proj.get("milestones", [])
            milestones_total = len(milestones)
            milestones_done = sum(1 for m in milestones if m.get("done", False) or m.get("status") == "Completed")
            
            live_url_val = proj.get("live_url", "")
            repo_url_val = proj.get("repo_url", "")
            
            live_link = f'<a href="{live_url_val}" target="_blank" style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.25); color: #a7f3d0; padding: 6px 14px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 12px; display: inline-flex; align-items: center; gap: 6px; transition: all 0.3s ease;">🌐 Canlı Link</a>' if live_url_val else ""
            repo_link = f'<a href="{repo_url_val}" target="_blank" style="background: rgba(102, 126, 234, 0.08); border: 1px solid rgba(102, 126, 234, 0.25); color: #c7d2fe; padding: 6px 14px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 12px; display: inline-flex; align-items: center; gap: 6px; transition: all 0.3s ease;">💻 Kod Deposu</a>' if repo_url_val else ""
            
            tech_badges = ""
            for tech in proj.get('tech_stack', []):
                tech_badges += f'<span style="background: rgba(102, 126, 234, 0.1); border: 1px solid rgba(102, 126, 234, 0.3); color: #c7d2fe; padding: 4px 10px; border-radius: 6px; font-size: 11px; margin-right: 8px; margin-bottom: 8px; display: inline-block;">{tech}</span>'
            
            # Team Members assigned
            assigned_team = proj.get("team", [])
            team_badges = ""
            if assigned_team:
                for name in assigned_team:
                    team_badges += f'<span style="background: rgba(102, 126, 234, 0.12); color: #c7d2fe; padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: 500; margin-right: 8px; margin-bottom: 8px; display: inline-block;">👤 {name}</span>'
            else:
                team_badges = '<span style="color: #6b7280; font-size: 12px; font-style: italic;">Atanmış ekip üyesi yok</span>'

            links_html = ""
            if live_link or repo_link:
                links_html = f"""
                <div style="display: flex; gap: 20px; margin-top: 15px; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 15px;">
                    {live_link}
                    {repo_link}
                </div>
                """
            
            # HTML Card Layout
            html_card = f"""
            <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); border-radius: 16px; padding: 24px; margin-bottom: 12px; box-shadow: 0 4px 30px rgba(0, 0, 0, 0.15); backdrop-filter: blur(5px);">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px; flex-wrap: wrap; gap: 10px;">
                    <div>
                        <div style="font-size: 22px; font-weight: 800; color: white; margin-bottom: 4px;">{proj.get('name', 'Bilinmeyen')}</div>
                        <div style="font-size: 13px; color: #9ca3af;">🏷️ {proj.get('category', 'Genel')}</div>
                    </div>
                    <div style="display: flex; gap: 8px; align-items: center;">
                        <span style="background-color: {priority_color}22; color: {priority_color}; padding: 6px 12px; border-radius: 20px; font-size: 11px; font-weight: 700; border: 1px solid {priority_color}55;">
                            🔥 {proj.get('priority', 'Medium')}
                        </span>
                        <span style="background-color: {status_color}22; color: {status_color}; padding: 6px 12px; border-radius: 20px; font-size: 11px; font-weight: 700; border: 1px solid {status_color}55;">
                            {proj.get('status', 'Planning')}
                        </span>
                    </div>
                </div>
                
                <p style="color: #d1d5db; font-size: 14.5px; line-height: 1.6; margin-bottom: 20px;">
                    {proj.get('description', '')}
                </p>
                
                <!-- Progress Bar -->
                <div style="margin-bottom: 20px;">
                    <div style="display: flex; justify-content: space-between; font-size: 12px; color: #9ca3af; margin-bottom: 6px;">
                        <span>Proje İlerleme Durumu</span>
                        <span style="font-weight: 700; color: #667eea;">%{progress}</span>
                    </div>
                    <div style="width: 100%; background: rgba(255,255,255,0.05); border-radius: 10px; height: 8px; border: 1px solid rgba(255,255,255,0.05);">
                        <div style="width: {progress}%; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); height: 6px; border-radius: 10px;"></div>
                    </div>
                </div>
                
                <!-- Stats Grid -->
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 15px; background: rgba(0, 0, 0, 0.15); border-radius: 12px; padding: 16px; margin-bottom: 20px; border: 1px solid rgba(255,255,255,0.02);">
                    <div>
                        <div style="font-size: 10.5px; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.5px;">📅 Zaman Çizelgesi</div>
                        <div style="font-size: 12.5px; color: white; font-weight: 600; margin-top: 4px;">{start_date} / {end_date}</div>
                    </div>
                    <div>
                        <div style="font-size: 10.5px; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.5px;">💻 Geliştirme Boyutu</div>
                        <div style="font-size: 12.5px; color: white; font-weight: 600; margin-top: 4px;">{lines_of_code:,} LOC | {commits} Commit</div>
                    </div>
                    <div>
                        <div style="font-size: 10.5px; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.5px;">🎯 Görev Oranı</div>
                        <div style="font-size: 12.5px; color: white; font-weight: 600; margin-top: 4px;">{tasks_completed} / {tasks_total} ({tasks_pct}%)</div>
                    </div>
                    <div>
                        <div style="font-size: 10.5px; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.5px;">🚩 Kilometre Taşları</div>
                        <div style="font-size: 12.5px; color: white; font-weight: 600; margin-top: 4px;">{milestones_done} / {milestones_total}</div>
                    </div>
                </div>

                <!-- Responsible Team -->
                <div style="margin-bottom: 20px;">
                    <div style="font-size: 11px; color: #9ca3af; text-transform: uppercase; margin-bottom: 8px; letter-spacing: 0.5px;">👥 Sorumlu Geliştiriciler</div>
                    <div style="display: flex; flex-wrap: wrap;">
                        {team_badges}
                    </div>
                </div>
                
                <div style="display: flex; flex-wrap: wrap; margin-bottom: 10px;">
                    {tech_badges}
                </div>
                {links_html}
            </div>
            """
            st.markdown(clean_html(html_card), unsafe_allow_html=True)
            
            # INTERACTIVE ACCORDIONS
            # Accordion 1: Roadmap & Milestone Checklist
            if milestones:
                with st.expander(f"🚩 Yol Haritası & Kilometre Taşları ({milestones_done}/{milestones_total})"):
                    for idx, ms in enumerate(milestones):
                        ms_key = f"ms_check_{proj_id}_{idx}"
                        ms_is_done = ms.get('done', False) or ms.get('status') == 'Completed'
                        checked = st.checkbox(f"{ms['name']} ({ms.get('date', '')})", value=ms_is_done, key=ms_key)
                        if checked != ms_is_done:
                            ms['done'] = checked
                            ms['status'] = 'Completed' if checked else 'Pending'
                            save_data(data)
                            st.rerun()
                            
            # Accordion 2: Kanban Task linkages
            if proj_tasks:
                with st.expander(f"📋 Proje Görevleri ({len(proj_tasks)} Görev)"):
                    for t in proj_tasks:
                        col_tk1, col_tk2 = st.columns([5, 1])
                        with col_tk1:
                            status_icon = "✅" if t.get('status') == "Done" else ("⏳" if t.get('status') == "In Progress" else "💤")
                            st.markdown(f"{status_icon} **{t.get('title')}** - `{t.get('status')}` - *{t.get('date', '')}*")
                        with col_tk2:
                            if st.button("🔍 Detaylar", key=f"proj_det_{t.get('id')}", use_container_width=True):
                                st.session_state.active_proj_task_id = t.get('id')
                                st.rerun()
                                
                    # If this project's active task detail is open, render it!
                    active_pt_id = st.session_state.get("active_proj_task_id")
                    if active_pt_id:
                        active_task = next((t for t in proj_tasks if t.get("id") == active_pt_id), None)
                        if active_task:
                            st.markdown("---")
                            col_pspace, col_pclose = st.columns([5, 1])
                            with col_pclose:
                                if st.button("❌ Kapat", key="close_proj_task_details", use_container_width=True):
                                    del st.session_state.active_proj_task_id
                                    st.rerun()
                            render_task_details(active_task, data)
                        
            # Accordion 3: Project settings (Edit & Delete)
            with st.expander("⚙️ Proje Ayarlarını Yönet"):
                st.markdown("##### 📝 Proje Bilgilerini Güncelle")
                edit_form_key = f"edit_form_{proj_id}"
                with st.form(edit_form_key):
                    col_ep1, col_ep2 = st.columns(2)
                    new_status = col_ep1.selectbox("Durum", ["Planning", "In Progress", "Production"], index=["Planning", "In Progress", "Production"].index(proj.get("status", "Planning")))
                    new_priority = col_ep2.selectbox("Öncelik", ["Low", "Medium", "High", "Critical"], index=["Low", "Medium", "High", "Critical"].index(proj.get("priority", "Medium")))
                    
                    col_ep3, col_ep4 = st.columns(2)
                    new_progress = col_ep3.slider("İlerleme Oranı (%)", 0, 100, int(proj.get("progress", 0)))
                    new_cat = col_ep4.text_input("Kategori", value=proj.get("category", ""))
                    
                    new_desc = st.text_area("Açıklama", value=proj.get("description", ""))
                    new_tech_str = st.text_input("Teknolojiler (Virgülle ayırın)", value=", ".join(proj.get("tech_stack", [])))
                    
                    # Team assignment in edit form
                    team_list = [data.get('owner', {}).get('name', 'Deniz Deviren')] + [m['name'] for m in data.get('team', [])]
                    current_team = proj.get("team", [])
                    new_team = st.multiselect("Sorumlu Geliştiriciler / Ekip Üyeleri", team_list, default=[t for t in current_team if t in team_list])

                    col_ep5, col_ep6 = st.columns(2)
                    new_live = col_ep5.text_input("Canlı Link", value=proj.get("live_url", ""))
                    new_repo = col_ep6.text_input("Repo Linki", value=proj.get("repo_url", ""))
                    
                    col_ep7, col_ep8 = st.columns(2)
                    new_loc = col_ep7.number_input("Kod Satırı (LOC)", value=int(proj.get("lines_of_code", 0)), min_value=0)
                    new_commits = col_ep8.number_input("Commit Sayısı", value=int(proj.get("commits", 0)), min_value=0)
                    
                    save_btn = st.form_submit_button("Değişiklikleri Kaydet")
                    if save_btn:
                        proj["status"] = new_status
                        proj["priority"] = new_priority
                        proj["progress"] = new_progress
                        proj["category"] = new_cat
                        proj["description"] = new_desc
                        proj["tech_stack"] = [t.strip() for t in new_tech_str.split(",") if t.strip()]
                        proj["team"] = new_team
                        proj["live_url"] = new_live
                        proj["repo_url"] = new_repo
                        proj["lines_of_code"] = new_loc
                        proj["commits"] = new_commits
                        
                        save_data(data)
                        st.success("Proje başarıyla güncellendi!")
                        st.rerun()
                        
                st.markdown("##### 🚩 Kilometre Taşlarını Yönet")
                st.markdown("###### Yeni Kilometre Taşı Ekle")
                with st.form(f"add_ms_form_{proj_id}"):
                    col_ams1, col_ams2 = st.columns([3, 1])
                    new_ms_name = col_ams1.text_input("Kilometre Taşı Adı", placeholder="Örn: Beta Sürümü Yayını")
                    new_ms_date = col_ams2.text_input("Hedef Tarih (YYYY-MM-DD)", value=datetime.now().strftime("%Y-%m-%d"))
                    add_ms_btn = st.form_submit_button("➕ Ekle")
                    if add_ms_btn and new_ms_name:
                        if "milestones" not in proj:
                            proj["milestones"] = []
                        proj["milestones"].append({
                            "name": new_ms_name,
                            "date": new_ms_date,
                            "done": False
                        })
                        save_data(data)
                        st.success("Kilometre taşı başarıyla eklendi!")
                        st.rerun()
                        
                if proj.get("milestones"):
                    st.markdown("###### Mevcut Kilometre Taşları (Silmek için butona tıklayın)")
                    for ms_idx, ms in enumerate(proj["milestones"]):
                        col_ms1, col_ms2 = st.columns([4, 1])
                        col_ms1.write(f"🚩 {ms['name']} ({ms.get('date', '')}) - {'✅ Tamamlandı' if ms.get('done', False) or ms.get('status') == 'Completed' else '⏳ Bekliyor'}")
                        if col_ms2.button("🗑️ Sil", key=f"del_ms_{proj_id}_{ms_idx}"):
                            proj["milestones"].pop(ms_idx)
                            save_data(data)
                            st.success("Kilometre taşı başarıyla silindi!")
                            st.rerun()
                            
                st.markdown("---")
                st.markdown("##### 🔒 Projeyi Gizli Kasaya Gönder (Şifrele)")
                st.markdown("Bu projeyi şifreleyerek gizli kasaya taşıyabilirsiniz. Projeye ait tüm detaylar belirleyeceğiniz şifre ile XOR/SHA-256 algoritmaları kullanılarak kriptolanacaktır.")
                with st.form(f"encrypt_project_form_{proj_id}"):
                    pwd1 = st.text_input("Kasa Şifresi Belirleyin *", type="password", key=f"enc_pwd1_{proj_id}", placeholder="Şifre...")
                    pwd2 = st.text_input("Şifreyi Doğrulayın *", type="password", key=f"enc_pwd2_{proj_id}", placeholder="Şifre Doğrulama...")
                    encrypt_btn = st.form_submit_button("🔒 Projeyi Kriptola ve Kasaya Gönder")
                    if encrypt_btn:
                        if not pwd1:
                            st.error("⚠️ Şifre alanı boş bırakılamaz.")
                        elif pwd1 != pwd2:
                            st.error("⚠️ Şifreler uyuşmuyor! Lütfen kontrol edin.")
                        else:
                            from utils.encryption import encrypt_text
                            # Encrypt data
                            proj["is_secret"] = True
                            p_desc = proj.get("description", "")
                            p_tech_str = ", ".join(proj.get("tech_stack", []))
                            proj["description"] = encrypt_text(p_desc, pwd1)
                            proj["tech_stack"] = [encrypt_text(p_tech_str, pwd1)]
                            
                            # Log action
                            data["activities"].insert(0, {
                                "date": datetime.now().strftime("%Y-%m-%d"),
                                "time": datetime.now().strftime("%H:%M"),
                                "action": f"🔒 Proje şifrelendi ve kasaya taşındı: {proj.get('name')}",
                                "project": proj_id
                            })
                            
                            save_data(data)
                            # Put password in unlocked secrets in session state
                            if "unlocked_secrets" not in st.session_state:
                                st.session_state.unlocked_secrets = {}
                            st.session_state.unlocked_secrets[proj_id] = pwd1
                            
                            st.success("🔓 Proje başarıyla şifrelendi ve Gizli Kasa'ya gönderildi!")
                            st.rerun()
                            
                st.markdown("---")
                st.markdown("##### ⚠️ Tehlikeli Alan")
                confirm_delete = st.checkbox("Bu projeyi tamamen ve geri döndürülemez şekilde silmek istiyorum.", key=f"confirm_del_{proj_id}")
                if st.button("🗑️ PROJEYİ TAMAMEN SİL", key=f"del_proj_btn_{proj_id}", type="primary"):
                    if confirm_delete:
                        data["projects"] = [p for p in data["projects"] if p["id"] != proj_id]
                        # Log action
                        data["activities"].insert(0, {
                            "date": datetime.now().strftime("%Y-%m-%d"),
                            "time": datetime.now().strftime("%H:%M"),
                            "action": f"🗑️ Proje kalıcı olarak silindi: {proj.get('name')}",
                            "project": "Genel"
                        })
                        save_data(data)
                        st.warning("Proje başarıyla silindi!")
                        st.rerun()
                    else:
                        st.error("Lütfen önce silme işlemini onaylayan kutucuğu işaretleyin.")
                        
            st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
            
    # -------------------------------------------------------------
    # 3. PREMIUM ADD NEW GENERAL PROJECT FORM
    # -------------------------------------------------------------
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<div class="section-title">➕ Yeni Genel Proje Ekle</div>', unsafe_allow_html=True)
    with st.form("new_project_form"):
        col_np1, col_np2 = st.columns(2)
        p_name = col_np1.text_input("Proje Adı *", placeholder="Örn: Emlak Fiyat Tahmin AI")
        p_cat = col_np2.text_input("Kategori *", placeholder="Örn: Yapay Zeka / Web Servisi")
        p_desc = st.text_area("Açıklama", placeholder="Proje detaylarını, hedeflerini buraya yazın...")
        
        col_np3, col_np4 = st.columns(2)
        p_status = col_np3.selectbox("Durum", ["Planning", "In Progress", "Production"])
        p_priority = col_np4.selectbox("Öncelik Derecesi", ["Low", "Medium", "High", "Critical"])
        
        p_progress = st.slider("Başlangıç İlerleme Derecesi (%)", 0, 100, 0)
        p_tech = st.text_input("Teknolojiler (Virgülle ayırın)", placeholder="Python, Streamlit, Scikit-learn...")
        
        # Team selection in creation form
        team_list = [data.get('owner', {}).get('name', 'Deniz Deviren')] + [m['name'] for m in data.get('team', [])]
        p_team = st.multiselect("Ekip / Ortak Atayın", team_list)

        col_np5, col_np6 = st.columns(2)
        p_live = col_np5.text_input("Canlı Link (Opsiyonel)", placeholder="https://example.com")
        p_repo = col_np6.text_input("Repo Linki (Opsiyonel)", placeholder="https://github.com/...")
        
        col_np7, col_np8 = st.columns(2)
        p_loc = col_np7.number_input("Kod Satırı (LOC) Başlangıç", value=0, min_value=0)
        p_commits = col_np8.number_input("Commit Sayısı Başlangıç", value=0, min_value=0)
        
        p_milestones = st.text_input("Başlangıç Kilometre Taşları (Virgülle ayırın, Opsiyonel)", placeholder="Örn: Veri Analizi, API Entegrasyonu, Beta Sürümü")
        
        submit_btn = st.form_submit_button("Genel Projeyi Ekle")
        
        if submit_btn:
            if p_name and p_cat:
                final_milestones = []
                if p_milestones:
                    for ms_name in p_milestones.split(","):
                        if ms_name.strip():
                            final_milestones.append({
                                "name": ms_name.strip(),
                                "date": datetime.now().strftime("%Y-%m-%d"),
                                "done": False
                            })
                            
                new_proj = {
                    "id": f"PRJ-{str(uuid.uuid4())[:6].upper()}",
                    "name": p_name,
                    "category": p_cat,
                    "description": p_desc,
                    "status": p_status,
                    "progress": p_progress,
                    "priority": p_priority,
                    "start_date": datetime.now().strftime("%Y-%m-%d"),
                    "end_date": datetime.now().strftime("%Y-%m-%d"),
                    "live_url": p_live,
                    "repo_url": p_repo,
                    "tech_stack": [t.strip() for t in p_tech.split(",") if t.strip()],
                    "team": p_team,
                    "lines_of_code": p_loc,
                    "commits": p_commits,
                    "tasks_total": 0,
                    "tasks_completed": 0,
                    "milestones": final_milestones,
                    "is_secret": False,
                    "owner_name": active_owner
                }
                data["projects"].append(new_proj)
                
                data["activities"].insert(0, {
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "time": datetime.now().strftime("%H:%M"),
                    "action": f"🔥 Yeni genel proje eklendi: {p_name}",
                    "project": new_proj["id"]
                })
                
                save_data(data)
                st.success("🎉 Proje başarıyla oluşturuldu ve Command Center'a eklendi!")
                st.rerun()
            else:
                st.error("⚠️ Proje Adı ve Kategori zorunludur.")
