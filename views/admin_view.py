import streamlit as st
import plotly.graph_objects as go
from utils.data_handler import save_data, get_all_accounts

PAGE_KEYS = {
    "🏠 Dashboard": "dashboard",
    "📁 Projeler": "projects",
    "📚 Arşiv ve Belgeler": "archive",
    "📊 DeDev Findeks Skoru": "portfolio_rating",
    "🔒 Gizli Kasa": "secret_vault",
    "📋 Kanban Board": "kanban",
    "📅 Takvim Görünümü": "calendar",
    "📊 Şemalar ve Gantt": "timeline",
    "💻 Tech Stack": "techstack",
    "👥 Ekip Yönetimi": "team",
    "📈 Raporlar": "reports",
    "📝 Hızlı Notlar": "notes",
    "⏱️ Zaman Takibi": "time_tracking",
    "💰 Bütçe & Giderler": "finance",
    "⚙️ Admin Paneli": "admin"
}

def clean_html(html_str):
    return "\n".join([line.strip() for line in html_str.split("\n")])

def show_admin(data):
    st.markdown('<div class="section-title">⚙️ Yönetim & Admin Paneli</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Çoklu hesap profilleri ekleme, silme, yönetme ve çapraz analiz merkezi</div>', unsafe_allow_html=True)
    
    if "accounts" not in data:
        data["accounts"] = [data.get("owner", {
            "name": "Deniz Deviren",
            "role": "Solo Full-Stack Developer & AI Engineer",
            "company": "DeDev",
            "location": "Remote / Global",
            "since": "2023",
            "bio": "Tek kişilik ekip. Yapay zeka, web, mobil ve oyun geliştirme projeleri."
        })]
    if "active_owner" not in data:
        data["active_owner"] = data["accounts"][0]["name"]
        
    active_owner_name = data.get("active_owner", "Deniz Deviren")
    
    # -------------------------------------------------------------
    # STREAMLIT TABS
    # -------------------------------------------------------------
    tab_profiles, tab_new_profile, tab_team_login, tab_cross_stats = st.tabs([
        "👥 Profil Yönetimi & Geçiş", 
        "➕ Yeni Profil (Hesap) Ekle",
        "🔐 Ekip Giriş Yönetimi",
        "📊 Hesaplar Arası Analiz"
    ])
    
    # =============================================================
    # SEKME 1: PROFİL YÖNETİMİ & AKTİF HESAP GEÇİŞİ
    # =============================================================
    with tab_profiles:
        st.markdown("### 🔄 Aktif Hesap Değiştirici")
        st.markdown("""
        <div style="font-size: 13px; color: #9ca3af; margin-bottom: 15px;">
            Aşağıdaki menüden aktif çalışma alanını (profil hesabını) değiştirebilirsiniz. Değişiklik yaptığınızda tüm projeler, Kanban tahtaları ve bütçeler seçilen hesaba göre filtrelenecektir.
        </div>
        """, unsafe_allow_html=True)
        
        all_accounts = get_all_accounts()
        account_names = [acc["name"] for acc in all_accounts]
        
        # Determine active index
        try:
            active_idx = account_names.index(active_owner_name)
        except ValueError:
            active_idx = 0
            
        selected_acc_name = st.selectbox(
            "Aktif Çalışma Alanı (Hesap Profil):",
            account_names,
            index=active_idx,
            key="active_owner_select"
        )
        
        if selected_acc_name != active_owner_name:
            selected_acc = next((acc for acc in all_accounts if acc["name"] == selected_acc_name), None)
            if selected_acc:
                selected_username = selected_acc.get("username")
                # Swap workspace database by changing logged_in_user
                st.session_state["logged_in_user"] = selected_username
                
                # Load the new database context so we can modify its active_owner
                from utils.data_handler import load_data, save_data
                db_data = load_data()
                db_data["active_owner"] = selected_acc_name
                db_data["owner"] = selected_acc
                save_data(db_data)
                
                st.toast(f"⚡ Çalışma alanı '{selected_acc_name}' olarak değiştirildi!", icon="⚡")
                st.rerun()
            
        st.markdown("---")
        st.markdown("### 🏢 Kayıtlı Profiller")
        
        # Grid of accounts
        cols = st.columns(3)
        all_accounts = get_all_accounts()
        for idx, acc in enumerate(all_accounts):
            col_idx = idx % 3
            with cols[col_idx]:
                is_active = acc["name"] == active_owner_name
                border_color = "rgba(102, 126, 234, 0.6)" if is_active else "rgba(255,255,255,0.05)"
                active_badge = '<span style="background: #10b981; color: white; padding: 2px 8px; border-radius: 12px; font-size: 10px; font-weight: bold; float: right;">AKTİF HESAP</span>' if is_active else ''
                
                credentials_html = ""
                if acc.get("username") == "1denizdeviren":
                    credentials_html = """
                    <div style="background: rgba(16, 185, 129, 0.05); border: 1px solid rgba(16, 185, 129, 0.15); padding: 8px; border-radius: 8px; margin-top: 10px; font-family: monospace; font-size: 11px; color: #10b981; font-weight: 500; text-align: center;">
                        🔒 Güvenli Yönetici Hesabı
                    </div>
                    """
                elif acc.get("username") == "furkan":
                    credentials_html = """
                    <div style="background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); padding: 8px; border-radius: 8px; margin-top: 10px; font-family: monospace; font-size: 11px; color: #a5b4fc;">
                        👤 K. Adı: furkan<br>🔑 Şifre: 123456 (Simülasyon)
                    </div>
                    """
                else:
                    credentials_html = f"""
                    <div style="background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); padding: 8px; border-radius: 8px; margin-top: 10px; font-family: monospace; font-size: 11px; color: #a5b4fc;">
                        👤 K. Adı: {acc.get('username', 'yok')}<br>🔑 Şifre: •••••••• (Kriptografik Güvenli)
                    </div>
                    """
                
                st.markdown(clean_html(f"""
                <div style="background: rgba(255,255,255,0.03); padding: 20px; border-radius: 16px; border: 1px solid {border_color}; margin-bottom: 15px; position: relative;">
                    {active_badge}
                    <div style="background: linear-gradient(135deg, #667eea, #764ba2); width: 50px; height: 50px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 20px; font-weight: bold; color: white; margin-bottom: 12px; box-shadow: 0 4px 10px rgba(102,126,234,0.3);">
                        {acc['name'][0].upper()}
                    </div>
                    <div style="font-weight: 700; color: white; font-size: 16px;">{acc['name']}</div>
                    <div style="color: #667eea; font-size: 12px; font-weight: 600; margin-top: 3px;">{acc.get('role', 'Proje Sorumlusu')}</div>
                    
                    {credentials_html}
                    
                    <div style="color: #9ca3af; font-size: 11px; margin-top: 10px; line-height: 1.4; min-height: 45px;">{acc.get('bio', 'Açıklama girilmemiş.')}</div>
                    
                    <div style="border-top: 1px solid rgba(255,255,255,0.08); margin-top: 12px; padding-top: 8px; font-size: 11px; color: #6b7280; display: flex; justify-content: space-between;">
                        <span>🏢 {acc.get('company', 'DeDev')}</span>
                        <span>📍 {acc.get('location', 'Remote')}</span>
                    </div>
                </div>
                """), unsafe_allow_html=True)
                
                # Admin role and permission editor
                if acc.get("username") not in ["1denizdeviren", "furkan", "demo_erpsim"]:
                    with st.expander("⚙️ Yetki ve Rol Düzenle"):
                        current_role_type = acc.get("role_type", "admin")
                        role_type_opts = ["Yönetici (Admin)", "Ekip Üyesi (Sınırlı)"]
                        default_role_idx = 0 if current_role_type == "admin" else 1
                        
                        edit_role_type = st.selectbox(
                            "Hesap Yetki Türü:",
                            role_type_opts,
                            index=default_role_idx,
                            key=f"edit_role_{acc['username']}"
                        )
                        
                        edit_perms = []
                        if edit_role_type == "Ekip Üyesi (Sınırlı)":
                            inverse_page_keys = {v: k for k, v in PAGE_KEYS.items()}
                            current_perms = acc.get("permissions", ["dashboard", "projects", "kanban", "timeline", "calendar", "time_tracking"])
                            pre_selected = [inverse_page_keys[p] for p in current_perms if p in inverse_page_keys]
                            
                            edit_perms = st.multiselect(
                                "Yetkili Sayfalar:",
                                list(PAGE_KEYS.keys()),
                                default=pre_selected,
                                key=f"edit_perms_{acc['username']}"
                            )
                        
                        if st.button("💾 Yetkileri Kaydet", key=f"save_perms_{acc['username']}", use_container_width=True):
                            new_rt = "admin" if edit_role_type == "Yönetici (Admin)" else "member"
                            acc["role_type"] = new_rt
                            if new_rt == "member":
                                acc["permissions"] = [PAGE_KEYS[p] for p in edit_perms]
                            else:
                                acc["permissions"] = list(PAGE_KEYS.values())
                            
                            save_data(data)
                            st.toast(f"🔑 '{acc['name']}' yetkileri başarıyla güncellendi!", icon="✅")
                            st.rerun()
                
                # Delete account button (cannot delete if active, if it's the only account, or if it is demo_erpsim)
                if not is_active and len(all_accounts) > 1 and acc.get("username") != "demo_erpsim":
                    if st.button(f"🗑️ Hesabı Sil", key=f"del_acc_{acc['name']}", type="secondary", use_container_width=True):
                        # Reassign projects of deleted owner to the active owner
                        for p in data.get("projects", []):
                            if p.get("owner_name") == acc["name"]:
                                p["owner_name"] = active_owner_name
                        data["accounts"] = [a for a in data.get("accounts", []) if a["name"] != acc["name"]]
                        save_data(data)
                        st.warning(f"'{acc['name']}' hesabı silindi.")
                        st.rerun()
                        
    # =============================================================
    # SEKME 2: YENİ PROFİL (HESAP) EKLE
    # =============================================================
    with tab_new_profile:
        st.markdown("### ➕ Yeni Hesap / Profil Oluştur")
        st.markdown("""
        <div style="font-size: 13px; color: #9ca3af; margin-bottom: 20px;">
            Sisteme yeni bir ortak veya farklı bir bağımsız proje sahibi profili ekleyin. Her yeni profil kendine özel proje alanına ve iş paneline sahip olacaktır.
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("new_account_form"):
            col1, col2 = st.columns(2)
            n_name = col1.text_input("Ad Soyad", placeholder="Örn: Ahmet Yılmaz")
            n_role = col2.text_input("Rol / Ünvan", placeholder="Örn: Kıdemli Ürün Yöneticisi")
            
            col_u, col_p = st.columns(2)
            n_username = col_u.text_input("Kullanıcı Adı", placeholder="Giriş için kullanılacak")
            n_password = col_p.text_input("Şifre / Parola", placeholder="Giriş şifresi", type="password")
            
            col3, col4 = st.columns(2)
            n_comp = col3.text_input("Şirket / Organizasyon", placeholder="Örn: DeDev Soft")
            n_loc = col4.text_input("Lokasyon", placeholder="Örn: İstanbul / Türkiye")
            
            n_since = st.text_input("Başlangıç Yılı", value="2026")
            n_bio = st.text_area("Kısa Biyografi / Açıklama", placeholder="Profilin uzmanlık alanları ve sorumlulukları...", max_chars=300)
            
            st.markdown("##### 🔑 Rol ve Yetkilendirme Kontrolü")
            n_role_type = st.selectbox("Hesap Yetki Türü", ["Ekip Üyesi (Sınırlı)", "Yönetici (Admin)"])
            n_permissions = st.multiselect(
                "Yetkili Modüller (Yalnızca Sınırlı Ekip Üyeleri İçin):",
                list(PAGE_KEYS.keys()),
                default=["🏠 Dashboard", "📁 Projeler", "📋 Kanban Board", "📊 Şemalar ve Gantt", "📅 Takvim Görünümü", "⏱️ Zaman Takibi"]
            )
            
            if st.form_submit_button("Yeni Profil Oluştur"):
                if n_name and n_username and n_password:
                    # Check duplication
                    if any(a["name"].lower() == n_name.lower() or a.get("username", "").lower() == n_username.lower() for a in get_all_accounts()):
                        st.error("❌ Bu isimle veya kullanıcı adıyla kayıtlı bir profil zaten mevcut!")
                    else:
                        from utils.encryption import hash_password
                        h_val, s_val = hash_password(n_password)
                        
                        role_type_str = "admin" if n_role_type == "Yönetici (Admin)" else "member"
                        permission_keys = [PAGE_KEYS[p] for p in n_permissions] if role_type_str == "member" else list(PAGE_KEYS.values())
                        
                        new_acc = {
                            "username": n_username,
                            "password_hash": h_val,
                            "password_salt": s_val,
                            "name": n_name,
                            "role": n_role if n_role else "Proje Sorumlusu",
                            "company": n_comp if n_comp else "DeDev",
                            "location": n_loc if n_loc else "Remote",
                            "since": n_since if n_since else "2026",
                            "bio": n_bio if n_bio else "Yeni ekip üyesi.",
                            "role_type": role_type_str,
                            "permissions": permission_keys
                        }
                        data["accounts"].append(new_acc)
                        save_data(data)
                        st.success(f"🎉 Yeni profil '{n_name}' başarıyla oluşturuldu!")
                        st.rerun()
                else:
                    st.error("❌ Ad Soyad alanı boş bırakılamaz.")
                    
    # =============================================================
    # SEKME 3: EKİP GİRİŞ YÖNETİMİ
    # =============================================================
    with tab_team_login:
        st.markdown("### 🔐 Ekip Üyesi Giriş Bilgileri Yönetimi")
        st.markdown("""
        <div style="font-size: 13px; color: #9ca3af; margin-bottom: 20px;">
            Ekip üyelerinize kullanıcı adı ve şifre atayın. Bu bilgilerle aynı sisteme giriş yapabilirler.
            Üyelerin görebileceği içerik, yetki ayarlarına göre otomatik filtrelenir.
        </div>
        """, unsafe_allow_html=True)

        team_members = data.get("team", [])
        if not team_members:
            st.info("Henüz ekip üyesi eklenmemiş. Önce Ekip Yönetimi sayfasından üye ekleyin.")
        else:
            for member in team_members:
                member_name = member.get("name", "")
                member_id   = member.get("id", "")
                # Find if this member already has a login account in current data
                existing_acc = next(
                    (a for a in data.get("accounts", []) if a.get("name") == member_name),
                    None
                )
                has_login = existing_acc is not None

                badge_color = "#10b981" if has_login else "#f59e0b"
                badge_text  = "✅ Giriş Tanımlı" if has_login else "⚠️ Giriş Yok"
                current_uname = existing_acc.get("username", "") if existing_acc else ""
                current_email = member.get("email", "")

                with st.expander(f"{'🟢' if has_login else '🟡'} {member_name} — {member.get('role','')}", expanded=False):
                    col_info, col_form = st.columns([1, 2])
                    with col_info:
                        st.markdown(f"""
                        <div style="background: rgba(255,255,255,0.03); padding: 15px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.06);">
                            <div style="font-weight: 700; color: white; font-size: 15px;">{member_name}</div>
                            <div style="color: #667eea; font-size: 12px; margin: 4px 0;">{member.get('role','')}</div>
                            <div style="color: #9ca3af; font-size: 11px;">🏢 {member.get('department','')}</div>
                            <div style="margin-top: 10px; padding: 6px 10px; border-radius: 8px;
                                        background: {'rgba(16,185,129,0.1)' if has_login else 'rgba(245,158,11,0.1)'};
                                        border: 1px solid {'rgba(16,185,129,0.3)' if has_login else 'rgba(245,158,11,0.3)'};
                                        font-size: 11px; font-weight: 600;
                                        color: {'#10b981' if has_login else '#f59e0b'};">
                                {badge_text}
                            </div>
                            {"<div style='margin-top:8px; font-size:11px; color:#a5b4fc;'>👤 " + current_uname + "</div>" if has_login else ""}
                        </div>
                        """, unsafe_allow_html=True)

                    with col_form:
                        with st.form(f"team_login_form_{member_id}"):
                            st.markdown("##### ✏️ Giriş Bilgileri Düzenle")
                            new_uname = st.text_input(
                                "Kullanıcı Adı",
                                value=current_uname,
                                placeholder="örn: furkanisik",
                                key=f"uname_{member_id}"
                            )
                            new_email = st.text_input(
                                "E-posta",
                                value=current_email,
                                placeholder="ornek@sirket.com",
                                key=f"email_{member_id}"
                            )
                            new_pwd = st.text_input(
                                "Yeni Şifre",
                                type="password",
                                placeholder="Boş bırakırsanız şifre değişmez",
                                key=f"pwd_{member_id}"
                            )
                            new_pwd2 = st.text_input(
                                "Şifre Tekrar",
                                type="password",
                                placeholder="Şifreyi tekrar girin",
                                key=f"pwd2_{member_id}"
                            )

                            # Role/permission selector for this member
                            current_rt = existing_acc.get("role_type", "member") if existing_acc else "member"
                            rt_choice = st.selectbox(
                                "Yetki Türü",
                                ["Ekip Üyesi (Sınırlı)", "Yönetici (Admin)"],
                                index=0 if current_rt == "member" else 1,
                                key=f"rt_{member_id}"
                            )
                            if rt_choice == "Ekip Üyesi (Sınırlı)":
                                inv_keys = {v: k for k, v in PAGE_KEYS.items()}
                                cur_perms = existing_acc.get("permissions", ["dashboard", "projects", "kanban", "timeline", "calendar", "time_tracking"]) if existing_acc else ["dashboard", "projects", "kanban", "timeline", "calendar", "time_tracking"]
                                pre_sel = [inv_keys[p] for p in cur_perms if p in inv_keys]
                                sel_perms = st.multiselect(
                                    "Yetkili Sayfalar",
                                    list(PAGE_KEYS.keys()),
                                    default=pre_sel,
                                    key=f"perms_{member_id}"
                                )

                            save_btn = st.form_submit_button("💾 Kaydet", use_container_width=True)
                            if save_btn:
                                if not new_uname:
                                    st.error("Kullanıcı adı boş olamaz.")
                                elif new_pwd and new_pwd != new_pwd2:
                                    st.error("Şifreler eşleşmiyor!")
                                else:
                                    # Check username conflict with other accounts
                                    conflict = next(
                                        (a for a in data.get("accounts", [])
                                         if a.get("username") == new_uname and a.get("name") != member_name),
                                        None
                                    )
                                    if conflict:
                                        st.error(f"'{new_uname}' kullanıcı adı zaten kullanımda.")
                                    else:
                                        from utils.encryption import hash_password
                                        role_type_str = "admin" if rt_choice == "Yönetici (Admin)" else "member"
                                        perm_keys = list(PAGE_KEYS.values()) if role_type_str == "admin" else [PAGE_KEYS[p] for p in sel_perms]

                                        if existing_acc:
                                            # Update existing account
                                            existing_acc["username"]  = new_uname
                                            existing_acc["name"]      = member_name
                                            existing_acc["role_type"] = role_type_str
                                            existing_acc["permissions"] = perm_keys
                                            if new_pwd:
                                                h, s = hash_password(new_pwd)
                                                existing_acc["password_hash"] = h
                                                existing_acc["password_salt"] = s
                                        else:
                                            # Create new login account for this team member
                                            pwd_to_use = new_pwd if new_pwd else "dedev2026"
                                            h, s = hash_password(pwd_to_use)
                                            new_acc_entry = {
                                                "username":      new_uname,
                                                "password_hash": h,
                                                "password_salt": s,
                                                "name":          member_name,
                                                "role":          member.get("role", "Ekip Üyesi"),
                                                "company":       data.get("accounts", [{}])[0].get("company", "DeDev"),
                                                "location":      "Remote",
                                                "since":         "2026",
                                                "bio":           f"{member_name}, ekip üyesi.",
                                                "role_type":     role_type_str,
                                                "permissions":   perm_keys,
                                            }
                                            data.setdefault("accounts", []).append(new_acc_entry)

                                        # Also update email on the team member record
                                        member["email"] = new_email

                                        save_data(data)
                                        st.success(f"✅ {member_name} giriş bilgileri kaydedildi! Kullanıcı adı: **{new_uname}**")
                                        st.rerun()

    # =============================================================
    # SEKME 4: HESAPLAR ARASI ANALİZ
    # =============================================================

    with tab_cross_stats:
        st.markdown("### 📊 Hesap Profilleri Karşılaştırma Analitiği")
        
        # Calculate stats for each account
        acc_stats = []
        for acc in data["accounts"]:
            name = acc["name"]
            proj_count = sum(1 for p in data.get("projects", []) if p.get("owner_name", "Deniz Deviren") == name)
            
            # Tasks count
            proj_ids = {p["id"] for p in data.get("projects", []) if p.get("owner_name", "Deniz Deviren") == name}
            task_count = sum(1 for t in data.get("tasks", []) if t.get("project_id") in proj_ids)
            
            # Completed tasks count
            task_done = sum(1 for t in data.get("tasks", []) if t.get("project_id") in proj_ids and t.get("status") == "Done")
            
            # Budget
            fin_sum = sum(float(f.get("amount", 0)) for f in data.get("finances", []) if f.get("project_id") in proj_ids)
            
            acc_stats.append({
                "name": name,
                "projects": proj_count,
                "tasks": task_count,
                "done": task_done,
                "budget": fin_sum
            })
            
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("Toplam Kayıtlı Hesap", len(data["accounts"]))
        col_m2.metric("Toplam Sistem Projesi", len(data.get("projects", [])))
        col_m3.metric("Toplam Sistem Görevi", len(data.get("tasks", [])))
        
        st.markdown("---")
        
        # Render Comparison Chart
        if acc_stats:
            fig_compare = go.Figure()
            
            names = [s["name"] for s in acc_stats]
            projs = [s["projects"] for s in acc_stats]
            tsks = [s["tasks"] for s in acc_stats]
            
            fig_compare.add_trace(go.Bar(
                name="Toplam Proje",
                x=names,
                y=projs,
                marker_color="#667eea",
                hovertemplate="Hesap: %{x}<br>Proje Sayısı: %{y}<extra></extra>"
            ))
            
            fig_compare.add_trace(go.Bar(
                name="Toplam Görev",
                x=names,
                y=tsks,
                marker_color="#10b981",
                hovertemplate="Hesap: %{x}<br>Görev Sayısı: %{y}<extra></extra>"
            ))
            
            fig_compare.update_layout(
                barmode='group',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                height=300,
                margin=dict(l=40, r=20, t=20, b=40),
                xaxis=dict(showgrid=False, title="Hesap Profilleri"),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)', title="Adet"),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            
            st.plotly_chart(fig_compare, use_container_width=True)
            
            # Show summary table
            st.markdown("#### 📝 Detaylı Hesap Tablosu")
            
            # Custom styled table
            table_rows = ""
            for s in acc_stats:
                table_rows += f"""
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding: 10px; font-weight: bold; color: white;">{s['name']}</td>
                    <td style="padding: 10px; text-align: center; color: #a5b4fc;">{s['projects']}</td>
                    <td style="padding: 10px; text-align: center; color: #e0e7ff;">{s['tasks']}</td>
                    <td style="padding: 10px; text-align: center; color: #6ee7b7;">{s['done']}</td>
                    <td style="padding: 10px; text-align: right; color: #fcd34d; font-weight: 600;">${s['budget']:.2f}</td>
                </tr>
                """
                
            st.markdown(clean_html(f"""
            <table style="width: 100%; border-collapse: collapse; margin-top: 10px; background: rgba(255,255,255,0.01); border-radius: 8px; overflow: hidden; border: 1px solid rgba(255,255,255,0.05);">
                <thead>
                    <tr style="background: rgba(102, 126, 234, 0.1); border-bottom: 1px solid rgba(255,255,255,0.1); color: #c7d2fe;">
                        <th style="padding: 12px; text-align: left;">Hesap / Yönetici</th>
                        <th style="padding: 12px; text-align: center;">Proje</th>
                        <th style="padding: 12px; text-align: center;">Görev</th>
                        <th style="padding: 12px; text-align: center;">Tamamlanan</th>
                        <th style="padding: 12px; text-align: right;">Bütçe Harcaması</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>
            """), unsafe_allow_html=True)
            
        else:
            st.info("Kıyaslanacak hesap verisi bulunamadı.")
