import streamlit as st
import uuid
from datetime import datetime
from utils.data_handler import save_data
from utils.encryption import encrypt_text, decrypt_text

def clean_html(html_str):
    return "\n".join([line.strip() for line in html_str.split("\n")])

def show_secret_vault(data):
    st.markdown('<div class="section-title">🔒 Şifreli Gizli Kasa</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">SHA-256 ve XOR Algoritmaları ile Güvenli Kriptolanmış Ticari ve Özel Projeler</div>', unsafe_allow_html=True)

    active_owner = data.get("active_owner", "Deniz Deviren")
    # 1. Session State Initialization for Unlock Keys
    if "unlocked_secrets" not in st.session_state:
        st.session_state.unlocked_secrets = {}

    secret_projects = [p for p in data.get("projects", []) if p.get("owner_name", "Deniz Deviren") == active_owner and p.get("is_secret", False)]
    total_secrets = len(secret_projects)
    
    # 2. Premium Vault Summary Cards
    st.markdown(f"""
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; margin-bottom: 25px;">
        <div style="background: linear-gradient(135deg, rgba(239, 68, 68, 0.12) 0%, rgba(153, 27, 27, 0.12) 100%); border: 1px solid rgba(239, 68, 68, 0.25); border-radius: 16px; padding: 20px; text-align: center; box-shadow: 0 4px 20px rgba(0,0,0,0.15);">
            <div style="font-size: 26px; margin-bottom: 6px;">🔒</div>
            <div style="font-size: 11px; color: #fca5a5; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;">Kasadaki Projeler</div>
            <div style="font-size: 28px; font-weight: 800; color: white; margin-top: 5px;">{total_secrets}</div>
        </div>
        <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.12) 0%, rgba(4, 120, 87, 0.12) 100%); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 16px; padding: 20px; text-align: center; box-shadow: 0 4px 20px rgba(0,0,0,0.15);">
            <div style="font-size: 26px; margin-bottom: 6px;">🔓</div>
            <div style="font-size: 11px; color: #a7f3d0; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;">Açık Kilit Sayısı</div>
            <div style="font-size: 28px; font-weight: 800; color: white; margin-top: 5px;">{len(st.session_state.unlocked_secrets)}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not secret_projects:
        st.info("Kasadaki gizli proje bulunamadı. Aşağıdaki formdan yeni bir gizli proje oluşturabilirsiniz.")
    else:
        for proj in secret_projects:
            proj_id = proj["id"]
            
            # Check if this project is already unlocked in session state
            saved_pwd = st.session_state.unlocked_secrets.get(proj_id, "")
            is_currently_unlocked = False
            decrypted_desc = ""
            decrypted_tech = []

            if saved_pwd:
                dec_res = decrypt_text(proj.get('description', ''), saved_pwd)
                if dec_res != "ERROR_WRONG_PASSWORD" and dec_res:
                    is_currently_unlocked = True
                    decrypted_desc = dec_res
                    # Decrypt tech stack
                    if proj.get('tech_stack') and len(proj['tech_stack']) > 0:
                        t_res = decrypt_text(proj['tech_stack'][0], saved_pwd)
                        if t_res and t_res != "ERROR_WRONG_PASSWORD":
                            decrypted_tech = [t.strip() for t in t_res.split(",")]
                        else:
                            decrypted_tech = proj['tech_stack']

            # Render Lock Screen / Locked Status Badge or Full Card
            status_color = {
                "Production": "#22c55e",
                "In Progress": "#3b82f6",
                "Planning": "#f59e0b"
            }.get(proj.get('status', 'Planning'), "#6b7280")

            if not is_currently_unlocked:
                # LOCKED VIEW
                header_card = f"""
                <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(239, 68, 68, 0.15); border-radius: 16px; padding: 24px; margin-bottom: 12px; box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px;">
                        <div>
                            <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
                                <div style="font-size: 22px; font-weight: 700; color: white;">{proj.get('name', 'Bilinmeyen')}</div>
                                <span style="background: rgba(239, 68, 68, 0.15); color: #ef4444; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: bold; border: 1px solid rgba(239, 68, 68, 0.3);">🔒 ŞİFRELİ KASA</span>
                            </div>
                            <div style="font-size: 13px; color: #9ca3af; margin-top: 4px;">🏷️ {proj.get('category')}</div>
                        </div>
                        <div style="background-color: {status_color}22; color: {status_color}; padding: 6px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; border: 1px solid {status_color}55;">
                            {proj.get('status')}
                        </div>
                    </div>
                </div>
                """
                st.markdown(clean_html(header_card), unsafe_allow_html=True)
                
                # Password Input and Unlock Button
                col_pwd1, col_pwd2 = st.columns([3, 1])
                pwd_input = col_pwd1.text_input(
                    f"'{proj.get('name')}' Detaylarını Çözmek İçin Şifre Girin",
                    type="password",
                    key=f"input_secret_{proj_id}",
                    placeholder="Anahtarı yazın...",
                    label_visibility="collapsed"
                )
                unlock_btn = col_pwd2.button("🔓 Kilit Aç", key=f"unlock_btn_{proj_id}", use_container_width=True)
                
                if unlock_btn and pwd_input:
                    dec_test = decrypt_text(proj.get('description', ''), pwd_input)
                    if dec_test == "ERROR_WRONG_PASSWORD" or not dec_test:
                        st.error("❌ Hatalı Şifre! Lütfen doğru anahtarı girin.")
                    else:
                        st.session_state.unlocked_secrets[proj_id] = pwd_input
                        st.success("🔓 Başarıyla deşifre edildi!")
                        st.rerun()

                # Password Reset Expander for Locked Projects
                with st.expander("⚠️ Şifre Sıfırlama (Şifremi Unuttum)"):
                    st.error("""
                    **UYARI: VERİ KAYBI RİSKİ!**
                    
                    Bu projenin şifresini unuttuysanız, yeni bir kasa şifresi belirleyerek şifreyi sıfırlayabilirsiniz. 
                    Ancak eski şifreyle şifrelenmiş olan **Proje Açıklaması** ve **Teknoloji Listesi** verileri kurtarılamayacaktır.
                    Bu veriler güvenli varsayılan metinlerle sıfırlanıp yeni şifrenizle şifrelenecektir. 
                    *Diğer proje üst bilgileri (isim, durum, ekip, vb.) korunacaktır.*
                    """)
                    confirm_reset = st.checkbox("Şifrelenmiş proje detaylarının kalıcı olarak silineceğini ve sıfırlanacağını onaylıyorum.", key=f"confirm_reset_{proj_id}")
                    
                    with st.form(f"reset_pwd_form_{proj_id}"):
                        reset_pwd = st.text_input("Yeni Kasa Şifresi", type="password", key=f"reset_pwd_{proj_id}")
                        reset_pwd_confirm = st.text_input("Yeni Kasa Şifresini Doğrulayın", type="password", key=f"reset_pwd_conf_{proj_id}")
                        submit_reset = st.form_submit_button("⚠️ Şifreyi Sıfırla ve Kasayı Aç")
                        if submit_reset:
                            if not confirm_reset:
                                st.error("Lütfen önce verilerin sıfırlanacağını onaylayan kutucuğu işaretleyin.")
                            elif not reset_pwd:
                                st.error("Lütfen geçerli bir yeni şifre girin.")
                            elif reset_pwd != reset_pwd_confirm:
                                st.error("Girdiğiniz şifreler birbiriyle eşleşmiyor.")
                            else:
                                # Reset description and tech stack to safe defaults
                                default_desc = "Bu projenin şifresi sıfırlanmıştır. Yeni açıklama detaylarını Proje Ayarlarını Yönet panelinden düzenleyebilirsiniz."
                                default_tech = "Python, Streamlit"
                                
                                proj["description"] = encrypt_text(default_desc, reset_pwd)
                                proj["tech_stack"] = [encrypt_text(default_tech, reset_pwd)]
                                
                                save_data(data)
                                st.session_state.unlocked_secrets[proj_id] = reset_pwd
                                st.success("🎉 Şifre başarıyla sıfırlandı! Kasa kilidi açıldı ve varsayılan bilgiler oluşturuldu.")
                                st.rerun()

                st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
            
            else:
                # UNLOCKED VIEW - Premium Glassmorphism Details
                progress = proj.get("progress", 0)
                start_date = proj.get("start_date", "")
                end_date = proj.get("end_date", "")
                lines_of_code = proj.get("lines_of_code", 0)
                commits = proj.get("commits", 0)
                
                proj_tasks = [t for t in data.get("tasks", []) if t.get("project_id") == proj_id]
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
                for tech in decrypted_tech:
                    tech_badges += f'<span style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); color: #a7f3d0; padding: 4px 10px; border-radius: 6px; font-size: 11px; margin-right: 8px; margin-bottom: 8px; display: inline-block;">{tech}</span>'
                
                # Assigned Team Members
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
                
                details_card = f"""
                <div style="background: rgba(16, 185, 129, 0.03); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 16px; padding: 24px; margin-bottom: 15px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25); backdrop-filter: blur(8px);">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px; margin-bottom: 12px;">
                        <div>
                            <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
                                <div style="font-size: 24px; font-weight: 800; color: white;">{proj.get('name')}</div>
                                <span style="background: rgba(16, 185, 129, 0.2); color: #10b981; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: bold; border: 1px solid rgba(16, 185, 129, 0.4);">🔓 KİLİT AÇILDI</span>
                            </div>
                            <div style="font-size: 13px; color: #9ca3af; margin-top: 4px;">🏷️ {proj.get('category')}</div>
                        </div>
                        <div style="display: flex; gap: 8px; align-items: center;">
                            <span style="background-color: {status_color}22; color: {status_color}; padding: 6px 12px; border-radius: 20px; font-size: 11px; font-weight: 700; border: 1px solid {status_color}55;">
                                {proj.get('status')}
                            </span>
                        </div>
                    </div>
                    
                    <p style="color: #e5e7eb; font-size: 14.5px; line-height: 1.6; margin-bottom: 20px; background: rgba(0,0,0,0.15); padding: 15px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.02);">
                        {decrypted_desc}
                    </p>
                    
                    <!-- Progress Bar -->
                    <div style="margin-bottom: 20px;">
                        <div style="display: flex; justify-content: space-between; font-size: 12px; color: #9ca3af; margin-bottom: 6px;">
                            <span>Gizli Proje İlerlemesi</span>
                            <span style="font-weight: 700; color: #10b981;">%{progress}</span>
                        </div>
                        <div style="width: 100%; background: rgba(255,255,255,0.05); border-radius: 10px; height: 8px;">
                            <div style="width: {progress}%; background: linear-gradient(90deg, #10b981 0%, #059669 100%); height: 6px; border-radius: 10px;"></div>
                        </div>
                    </div>
                    
                    <!-- Stats Grid -->
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 15px; background: rgba(0, 0, 0, 0.2); border-radius: 12px; padding: 16px; margin-bottom: 20px; border: 1px solid rgba(255,255,255,0.02);">
                        <div>
                            <div style="font-size: 10.5px; color: #9ca3af; text-transform: uppercase;">📅 Zaman Çizelgesi</div>
                            <div style="font-size: 12.5px; color: white; font-weight: 600; margin-top: 4px;">{start_date} / {end_date}</div>
                        </div>
                        <div>
                            <div style="font-size: 10.5px; color: #9ca3af; text-transform: uppercase;">💻 Geliştirme Eforu</div>
                            <div style="font-size: 12.5px; color: white; font-weight: 600; margin-top: 4px;">{lines_of_code:,} LOC | {commits} Commit</div>
                        </div>
                        <div>
                            <div style="font-size: 10.5px; color: #9ca3af; text-transform: uppercase;">🎯 Görev Oranı</div>
                            <div style="font-size: 12.5px; color: white; font-weight: 600; margin-top: 4px;">{tasks_completed} / {tasks_total} ({tasks_pct}%)</div>
                        </div>
                        <div>
                            <div style="font-size: 10.5px; color: #9ca3af; text-transform: uppercase;">🚩 Kilometre Taşları</div>
                            <div style="font-size: 12.5px; color: white; font-weight: 600; margin-top: 4px;">{milestones_done} / {milestones_total}</div>
                        </div>
                    </div>

                    <!-- Team Members Badges -->
                    <div style="margin-bottom: 20px;">
                        <div style="font-size: 11px; color: #9ca3af; text-transform: uppercase; margin-bottom: 8px; letter-spacing: 0.5px;">👥 Sorumlu Ekip / Ortaklar</div>
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
                st.markdown(clean_html(details_card), unsafe_allow_html=True)

                # Action Buttons (Lock or Make Public)
                col_actions = st.columns(2)
                with col_actions[0]:
                    if st.button("🔒 Projeyi Tekrar Kilitle", key=f"lock_btn_action_{proj_id}", use_container_width=True):
                        st.session_state.unlocked_secrets.pop(proj_id, None)
                        st.success("Güvenle kilitlendi!")
                        st.rerun()
                with col_actions[1]:
                    if st.button("🔓 Kasadan Çıkar (Genelleştir)", key=f"make_public_action_{proj_id}", type="primary", use_container_width=True):
                        decrypted_description = decrypt_text(proj.get('description', ''), saved_pwd)
                        decrypted_tech_list = []
                        if proj.get('tech_stack') and len(proj['tech_stack']) > 0:
                            t_res = decrypt_text(proj['tech_stack'][0], saved_pwd)
                            if t_res and t_res != "ERROR_WRONG_PASSWORD":
                                decrypted_tech_list = [t.strip() for t in t_res.split(",")]
                            else:
                                decrypted_tech_list = proj['tech_stack']
                        
                        # Remove secret status and restore decrypted values
                        proj["is_secret"] = False
                        proj["description"] = decrypted_description
                        proj["tech_stack"] = decrypted_tech_list
                        
                        # Log action
                        data["activities"].insert(0, {
                            "date": datetime.now().strftime("%Y-%m-%d"),
                            "time": datetime.now().strftime("%H:%M"),
                            "action": f"🔓 Proje kasadan çıkarıldı: {proj.get('name')}",
                            "project": proj_id
                        })
                        
                        save_data(data)
                        st.session_state.unlocked_secrets.pop(proj_id, None)
                        st.success("🔓 Proje başarıyla kasadan çıkarıldı ve genel projelere taşındı!")
                        st.rerun()

                # Interactive Milestones checklist (Session safe!)
                if milestones:
                    with st.expander(f"🚩 Yol Haritası & Kilometre Taşları ({milestones_done}/{milestones_total})"):
                        for idx, ms in enumerate(milestones):
                            ms_key = f"ms_check_secret_{proj_id}_{idx}"
                            ms_is_done = ms.get('done', False) or ms.get('status') == 'Completed'
                            checked = st.checkbox(f"{ms['name']} ({ms.get('date', '')})", value=ms_is_done, key=ms_key)
                            if checked != ms_is_done:
                                ms['done'] = checked
                                ms['status'] = 'Completed' if checked else 'Pending'
                                save_data(data)
                                st.rerun()

                # Task linkages for Secret Projects
                if proj_tasks:
                    with st.expander(f"📋 Proje Görevleri ({len(proj_tasks)} Görev)"):
                        for t in proj_tasks:
                            status_icon = "✅" if t.get('status') == "Done" else ("⏳" if t.get('status') == "In Progress" else "💤")
                            st.markdown(f"{status_icon} **{t.get('title')}** - `{t.get('status')}` - *{t.get('date', '')}*")

                # Project Settings (Auto re-encrypting on submission!)
                with st.expander("⚙️ Gizli Proje Ayarlarını Yönet"):
                    st.markdown("##### 📝 Proje Bilgilerini Güncelle (Otomatik Şifrelenerek Kaydedilir)")
                    edit_secret_form_key = f"edit_secret_form_{proj_id}"
                    with st.form(edit_secret_form_key):
                        col_esp1, col_esp2 = st.columns(2)
                        new_status = col_esp1.selectbox("Durum", ["Planning", "In Progress", "Production"], index=["Planning", "In Progress", "Production"].index(proj.get("status", "Planning")))
                        new_priority = col_esp2.selectbox("Öncelik", ["Low", "Medium", "High", "Critical"], index=["Low", "Medium", "High", "Critical"].index(proj.get("priority", "Medium")))
                        
                        col_esp3, col_esp4 = st.columns(2)
                        new_progress = col_esp3.slider("İlerleme Oranı (%)", 0, 100, int(proj.get("progress", 0)))
                        new_cat = col_esp4.text_input("Kategori", value=proj.get("category", ""))
                        
                        new_desc = st.text_area("Açıklama (Şifresiz girin, sistem kasaya yazarken şifreler)", value=decrypted_desc)
                        new_tech_str = st.text_input("Teknolojiler (Şifresiz girin, virgülle ayırın)", value=", ".join(decrypted_tech))
                        
                        # Team Assignment Multi-Select
                        team_list = [active_owner] + [m['name'] for m in data.get('team', [])]
                        current_team = proj.get("team", [])
                        new_team = st.multiselect("Sorumlu Geliştiriciler / Ekip", team_list, default=[t for t in current_team if t in team_list])

                        col_esp5, col_esp6 = st.columns(2)
                        new_live = col_esp5.text_input("Canlı Link", value=proj.get("live_url", ""))
                        new_repo = col_esp6.text_input("Repo Linki", value=proj.get("repo_url", ""))
                        
                        col_esp7, col_esp8 = st.columns(2)
                        new_loc = col_esp7.number_input("Kod Satırı (LOC)", value=int(proj.get("lines_of_code", 0)), min_value=0)
                        new_commits = col_esp8.number_input("Commit Sayısı", value=int(proj.get("commits", 0)), min_value=0)
                        
                        save_btn = st.form_submit_button("Gizli Bilgileri Güncelle ve Şifrele")
                        if save_btn:
                            proj["status"] = new_status
                            proj["priority"] = new_priority
                            proj["progress"] = new_progress
                            proj["category"] = new_cat
                            proj["description"] = encrypt_text(new_desc, saved_pwd)
                            proj["tech_stack"] = [encrypt_text(new_tech_str, saved_pwd)]
                            proj["team"] = new_team
                            proj["live_url"] = new_live
                            proj["repo_url"] = new_repo
                            proj["lines_of_code"] = new_loc
                            proj["commits"] = new_commits
                            
                            save_data(data)
                            st.success("Gizli bilgileriniz deşifre edilmiş şifreyle yeniden kriptolanarak başarıyla kaydedildi!")
                            st.rerun()
                            
                    st.markdown("##### 🚩 Kilometre Taşlarını Yönet (Şifresiz)")
                    st.markdown("###### Yeni Kilometre Taşı Ekle")
                    with st.form(f"add_ms_secret_form_{proj_id}"):
                        col_ams1, col_ams2 = st.columns([3, 1])
                        new_ms_name = col_ams1.text_input("Kilometre Taşı Adı", placeholder="Örn: Alpha Sürümü Testleri")
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
                            st.success("Gizli projeye kilometre taşı başarıyla eklendi!")
                            st.rerun()
                            
                    if proj.get("milestones"):
                        st.markdown("###### Mevcut Kilometre Taşları (Silmek için butona tıklayın)")
                        for ms_idx, ms in enumerate(proj["milestones"]):
                            col_ms1, col_ms2 = st.columns([4, 1])
                            col_ms1.write(f"🚩 {ms['name']} ({ms.get('date', '')}) - {'✅ Tamamlandı' if ms.get('done', False) or ms.get('status') == 'Completed' else '⏳ Bekliyor'}")
                            if col_ms2.button("🗑️ Sil", key=f"del_ms_secret_{proj_id}_{ms_idx}"):
                                proj["milestones"].pop(ms_idx)
                                save_data(data)
                                st.success("Kilometre taşı başarıyla silindi!")
                                st.rerun()
                                
                    # Password Change Expander (only for unlocked projects)
                    with st.expander("🔑 Kasa Şifresini Değiştir (Şifre Yenileme)"):
                        st.markdown("##### 🔑 Proje Kasa Şifresini Yenile")
                        st.info("Bu işlem projenin tüm gizli detaylarını çözüp yeni belirleyeceğiniz şifre ile yeniden şifreler.")
                        with st.form(f"change_pwd_form_{proj_id}"):
                            new_vault_pwd = st.text_input("Yeni Kasa Şifresi", type="password", key=f"new_v_pwd_{proj_id}")
                            new_vault_pwd_confirm = st.text_input("Yeni Kasa Şifresini Doğrulayın", type="password", key=f"new_v_pwd_conf_{proj_id}")
                            submit_change_pwd = st.form_submit_button("🔑 Şifreyi Yenile")
                            if submit_change_pwd:
                                if not new_vault_pwd:
                                    st.error("Lütfen geçerli bir şifre girin.")
                                elif new_vault_pwd != new_vault_pwd_confirm:
                                    st.error("Girdiğiniz şifreler birbiriyle eşleşmiyor.")
                                else:
                                    # Decrypt using old password (saved_pwd)
                                    desc_dec = decrypt_text(proj.get('description', ''), saved_pwd)
                                    tech_dec = ""
                                    if proj.get('tech_stack') and len(proj['tech_stack']) > 0:
                                        t_res = decrypt_text(proj['tech_stack'][0], saved_pwd)
                                        if t_res and t_res != "ERROR_WRONG_PASSWORD":
                                            tech_dec = t_res
                                        else:
                                            tech_dec = ",".join(proj['tech_stack'])
                                    
                                    # Re-encrypt with new password
                                    proj["description"] = encrypt_text(desc_dec, new_vault_pwd)
                                    proj["tech_stack"] = [encrypt_text(tech_dec, new_vault_pwd)]
                                    
                                    save_data(data)
                                    st.session_state.unlocked_secrets[proj_id] = new_vault_pwd
                                    st.success("🎉 Kasa şifresi başarıyla yenilendi ve veriler yeni anahtarla tekrar şifrelendi!")
                                    st.rerun()

                    st.markdown("---")
                    st.markdown("##### ⚠️ Tehlikeli Alan")
                    confirm_delete = st.checkbox("Bu gizli projeyi kalıcı olarak kasadan silmek istediğimi onaylıyorum.", key=f"confirm_del_secret_{proj_id}")
                    if st.button("🗑️ GİZLİ PROJEYİ TAMAMEN SİL", key=f"del_secret_proj_btn_{proj_id}", type="primary"):
                        if confirm_delete:
                            data["projects"] = [p for p in data["projects"] if p["id"] != proj_id]
                            data["activities"].insert(0, {
                                "date": datetime.now().strftime("%Y-%m-%d"),
                                "time": datetime.now().strftime("%H:%M"),
                                "action": f"🗑️ Gizli proje kasadan silindi: {proj.get('name')}",
                                "project": "Genel"
                            })
                            save_data(data)
                            st.session_state.unlocked_secrets.pop(proj_id, None)
                            st.warning("Gizli proje başarıyla kasadan silindi!")
                            st.rerun()
                        else:
                            st.error("Lütfen önce silme işlemini onaylayan kutucuğu işaretleyin.")
            st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
            st.markdown("---")

    # 4. PREMIUM ADD NEW SECRET PROJECT FORM
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">➕ Kasaya Yeni Gizli Proje Ekle</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Oluşturulan tüm proje verileri belirlenen şifreyle anında şifrelenir.</div>', unsafe_allow_html=True)
    
    with st.form("new_secret_project_form"):
        col_np1, col_np2 = st.columns(2)
        p_name = col_np1.text_input("Gizli Proje Adı *", placeholder="Örn: Sparkz Sosyal Medya")
        p_cat = col_np2.text_input("Kategori *", placeholder="Örn: Sosyal Ağ & Mobil Oyun")
        
        p_desc = st.text_area("Şifresiz Açıklama (Veritabanında şifrelenecektir)", placeholder="Detayları buraya girin...")
        p_tech = st.text_input("Teknolojiler (Şifresiz girin, virgülle ayırın)", placeholder="Flutter, Python, Ollama...")
        
        col_np3, col_np4 = st.columns(2)
        p_status = col_np3.selectbox("Durum", ["Planning", "In Progress", "Production"])
        p_priority = col_np4.selectbox("Öncelik Derecesi", ["Low", "Medium", "High", "Critical"])
        
        # Team Assignment
        team_list = [active_owner] + [m['name'] for m in data.get('team', [])]
        p_team = st.multiselect("Ekip Arkadaşları atayın (Örn: M. Furkan Işık)", team_list)

        col_np5, col_np6 = st.columns(2)
        p_live = col_np5.text_input("Canlı Link (Opsiyonel)", placeholder="https://example.com")
        p_repo = col_np6.text_input("Repo Linki (Opsiyonel)", placeholder="https://github.com/...")
        
        col_np7, col_np8 = st.columns(2)
        p_loc = col_np7.number_input("Kod Satırı (LOC) Başlangıç", value=0, min_value=0)
        p_commits = col_np8.number_input("Commit Sayısı Başlangıç", value=0, min_value=0)
        
        p_milestones = st.text_input("Hedef Kilometre Taşları (Virgülle ayırın, Opsiyonel)", placeholder="Örn: Alpha Tasarımı, Beta Sürümü Yayını")
        
        st.markdown("###### 🔑 Kasa Şifreleme Anahtarı")
        col_pwd_np1, col_pwd_np2 = st.columns(2)
        p_pwd = col_pwd_np1.text_input("Kasa Şifresi Belirleyin *", type="password", placeholder="Anahtarı girin...")
        p_pwd_confirm = col_pwd_np2.text_input("Şifreyi Doğrulayın *", type="password", placeholder="Anahtarı doğrulayın...")
        
        submit_btn = st.form_submit_button("Gizli Projeyi Kasaya Ekle")
        
        if submit_btn:
            if p_name and p_cat:
                if not p_pwd:
                    st.error("⚠️ Gizli projeyi şifrelemek için bir kasa şifresi girmelisiniz.")
                elif p_pwd != p_pwd_confirm:
                    st.error("⚠️ Şifreler uyuşmuyor! Lütfen kontrol edin.")
                else:
                    encrypted_desc = encrypt_text(p_desc, p_pwd)
                    encrypted_tech = [encrypt_text(p_tech, p_pwd)]
                    
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
                        "description": encrypted_desc,
                        "status": p_status,
                        "progress": 0,
                        "priority": p_priority,
                        "start_date": datetime.now().strftime("%Y-%m-%d"),
                        "end_date": datetime.now().strftime("%Y-%m-%d"),
                        "live_url": p_live,
                        "repo_url": p_repo,
                        "tech_stack": encrypted_tech,
                        "team": p_team,
                        "lines_of_code": p_loc,
                        "commits": p_commits,
                        "tasks_total": 0,
                        "tasks_completed": 0,
                        "milestones": final_milestones,
                        "is_secret": True,
                        "owner_name": active_owner
                    }
                    
                    data["projects"].append(new_proj)
                    data["activities"].insert(0, {
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "time": datetime.now().strftime("%H:%M"),
                        "action": f"🔒 KASAYA YENİ GİZLİ PROJE EKLENDİ: {p_name}",
                        "project": new_proj["id"]
                    })
                    
                    save_data(data)
                    # Automatically set unlocked state so it displays unlocked immediately
                    st.session_state.unlocked_secrets[new_proj["id"]] = p_pwd
                    st.success("🎉 Yeni gizli proje başarıyla şifrelendi ve Kasaya kaydedildi!")
                    st.rerun()
            else:
                st.error("⚠️ Gizli Proje Adı ve Kategori doldurulması zorunlu alanlardır.")
