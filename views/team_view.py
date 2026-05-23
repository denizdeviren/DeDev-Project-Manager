import streamlit as st
import uuid
import plotly.graph_objects as go
from utils.data_handler import save_data

def clean_html(html_str):
    return "\n".join([line.strip() for line in html_str.split("\n")])

def show_team(data):
    st.markdown('<div class="section-title">👥 Ekip & Departman Yönetimi</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Takım arkadaşların, roller, dinamik departmanlar ve ekip analitiği merkezi</div>', unsafe_allow_html=True)

    if "team" not in data:
        data["team"] = []
    if "departments" not in data:
        data["departments"] = [
            {"id": "DEP-YAZILIM", "name": "Yazılım Geliştirme", "description": "Web, mobil ve backend geliştirme süreçleri.", "color": "#3b82f6", "icon": "💻"},
            {"id": "DEP-AI", "name": "Yapay Zeka & Veri Bilimi", "description": "Makine öğrenimi modelleri, LLM entegrasyonları.", "color": "#8b5cf6", "icon": "🧠"},
            {"id": "DEP-TASARIM", "name": "Tasarım & UI/UX", "description": "Arayüz tasarımı, grafikler ve marka kimliği.", "color": "#ec4899", "icon": "🎨"},
            {"id": "DEP-PAZARLAMA", "name": "Pazarlama & Satış", "description": "Müşteri ilişkileri ve ürün tanıtımları.", "color": "#f59e0b", "icon": "📈"},
            {"id": "DEP-YONETIM", "name": "Yönetim", "description": "Stratejik yönetim ve karar alma süreçleri.", "color": "#ef4444", "icon": "👑"}
        ]

    # Streamlit Tabs
    tab_workers, tab_depts, tab_stats = st.tabs([
        "👥 Çalışanlar (Ekip Üyeleri)",
        "🏢 Departman Yönetimi",
        "📊 Ekip Analitiği & Grafikler"
    ])

    # Map department name -> dict for quick lookup
    dept_map = {d["name"]: d for d in data["departments"]}
    dept_names = [d["name"] for d in data["departments"]]

    # =============================================================
    # SEKME 1: ÇALIŞANLAR
    # =============================================================
    with tab_workers:
        col_w1, col_w2 = st.columns([2, 1])

        with col_w1:
            st.markdown("### 👥 Ekip Listesi")
            
            # Department Filter
            filter_depts = ["Tüm Departmanlar"] + dept_names
            selected_filter = st.selectbox("Departmana Göre Filtrele", filter_depts, key="worker_dept_filter")
            
            st.markdown("---")
            
            # Filter team members
            filtered_team = data["team"]
            if selected_filter != "Tüm Departmanlar":
                filtered_team = [m for m in filtered_team if m.get("department") == selected_filter]
                
            if filtered_team or (selected_filter == "Tüm Departmanlar"):
                # Grid of 3 columns
                cols = st.columns(3)
                
                # Show Owner first if in "Tüm" or "Yönetim"
                owner_dept = "Yönetim"
                if selected_filter in ["Tüm Departmanlar", "Yönetim"]:
                    active_owner_name = data.get("active_owner", "Deniz Deviren")
                    owner_acc = next((a for a in data.get("accounts", []) if a.get("name") == active_owner_name), {})
                    owner_name = active_owner_name
                    owner_role = owner_acc.get("role", "Solo Developer" if active_owner_name == "Deniz Deviren" else "CEO & Software Architect")
                    owner_company = owner_acc.get("company", "DeDev" if active_owner_name == "Deniz Deviren" else "Aura Yazılım Teknolojileri")
                    
                    with cols[0]:
                        st.markdown(clean_html(f"""
                        <div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 16px; border: 1px solid rgba(16, 185, 129, 0.4); text-align: center; margin-bottom: 15px; position: relative;">
                            <span style="background: #10b981; color: white; padding: 2px 8px; border-radius: 12px; font-size: 10px; font-weight: bold; position: absolute; top: 12px; right: 12px;">SAHİBİ 👑</span>
                            <div style="background: linear-gradient(135deg, #10b981, #047857); width: 60px; height: 60px; border-radius: 50%; margin: 10px auto 10px; display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: bold; color: white; box-shadow: 0 4px 10px rgba(16, 185, 129, 0.3);">
                                {owner_name[0].upper()}
                            </div>
                            <div style="font-weight: 700; color: white; font-size: 16px; margin-top: 5px;">{owner_name}</div>
                            <div style="color: #9ca3af; font-size: 12px; margin-top: 3px;">{owner_role}</div>
                            
                            <div style="margin-top: 12px; display: inline-block; background: rgba(239, 68, 68, 0.15); color: #fca5a5; padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; border: 1px solid rgba(239, 68, 68, 0.2);">
                                👑 Yönetim
                            </div>
                            <div style="font-size: 11px; color: #6b7280; margin-top: 10px;">{owner_company}</div>
                        </div>
                        """), unsafe_allow_html=True)
                        st.markdown('<div style="height: 38px;"></div>', unsafe_allow_html=True)
                        
                start_col = 1 if selected_filter in ["Tüm Departmanlar", "Yönetim"] else 0
                
                for idx, member in enumerate(filtered_team):
                    col_idx = (idx + start_col) % 3
                    m_dept_name = member.get("department", "Yazılım Geliştirme")
                    m_dept = dept_map.get(m_dept_name, {"color": "#6b7280", "icon": "👥"})
                    
                    status_val = member.get("status", "Aktif")
                    status_color = "#10b981" if status_val == "Aktif" else "#f59e0b" if status_val == "İzinli" else "#ef4444"
                    status_badge = f'<span style="color: {status_color}; font-size: 11px; font-weight: bold;">● {status_val}</span>'
                    
                    with cols[col_idx]:
                        st.markdown(clean_html(f"""
                        <div style="background: rgba(255,255,255,0.03); padding: 20px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.06); text-align: center; margin-bottom: 15px; position: relative;">
                            <div style="position: absolute; top: 12px; left: 12px;">
                                {status_badge}
                            </div>
                            <div style="background: linear-gradient(135deg, #667eea, #764ba2); width: 60px; height: 60px; border-radius: 50%; margin: 10px auto 10px; display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: bold; color: white; box-shadow: 0 4px 10px rgba(102, 126, 234, 0.3);">
                                {member['name'][0].upper() if member['name'] else '?'}
                            </div>
                            <div style="font-weight: 700; color: white; font-size: 16px; margin-top: 5px;">{member['name']}</div>
                            <div style="color: #9ca3af; font-size: 12px; margin-top: 3px;">{member['role']}</div>
                            
                            <div style="margin-top: 12px; display: inline-block; background: {m_dept['color']}20; color: {m_dept['color']}; padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; border: 1px solid {m_dept['color']}35;">
                                {m_dept['icon']} {m_dept_name}
                            </div>
                            
                            <div style="font-size: 11px; margin-top: 10px;">
                                <a href="mailto:{member.get('email', '')}" style="color: #667eea; text-decoration: none;">✉️ {member.get('email', 'E-posta Yok')}</a>
                            </div>
                        </div>
                        """), unsafe_allow_html=True)
                        
                        # Login credentials lifecycle
                        from utils.data_handler import get_all_accounts
                        from utils.encryption import hash_password
                        
                        all_accs = get_all_accounts()
                        matched_acc = next((acc for acc in all_accs if acc.get("name") == member.get("name")), None)
                        
                        m_id = member.get("id", member.get("name", "unknown"))
                        exp_title = f"🔑 Giriş Bilgileri ({matched_acc.get('username')})" if matched_acc else "🔑 Giriş Yetkisi Ver"
                        with st.expander(exp_title):
                            if matched_acc:
                                # Update existing credentials
                                st.markdown(f"**👤 Kullanıcı Adı:** `{matched_acc.get('username')}`")
                                with st.form(f"edit_credentials_form_{m_id}"):
                                    new_uname = st.text_input("Kullanıcı Adı Güncelle", value=matched_acc.get('username', ''))
                                    new_pass = st.text_input("Yeni Şifre Belirle", type="password", placeholder="Değiştirmek istemiyorsanız boş bırakın")
                                    
                                    if st.form_submit_button("Giriş Bilgilerini Güncelle"):
                                        if not new_uname:
                                            st.error("Kullanıcı adı boş olamaz.")
                                        else:
                                            # Check uniqueness if username changed
                                            username_taken = any(
                                                acc.get("username").lower() == new_uname.lower() and acc.get("name") != member.get("name")
                                                for acc in all_accs
                                            )
                                            if username_taken:
                                                st.error("❌ Bu kullanıcı adı başka bir hesap tarafından kullanılıyor!")
                                            else:
                                                # Update account inside data["accounts"]
                                                db_acc = next((acc for acc in data.setdefault("accounts", []) if acc.get("name") == member.get("name")), None)
                                                if not db_acc:
                                                    db_acc = matched_acc
                                                    data["accounts"].append(db_acc)
                                                    
                                                db_acc["username"] = new_uname
                                                if new_pass:
                                                    h_val, s_val = hash_password(new_pass)
                                                    db_acc["password_hash"] = h_val
                                                    db_acc["password_salt"] = s_val
                                                    if "password" in db_acc:
                                                        del db_acc["password"]
                                                
                                                save_data(data)
                                                st.success("🎉 Giriş bilgileri başarıyla güncellendi!")
                                                st.rerun()
                            else:
                                # Create new credentials
                                with st.form(f"create_credentials_form_{m_id}"):
                                    new_uname = st.text_input("Kullanıcı Adı", placeholder="Örn: elif_demir")
                                    new_pass = st.text_input("Şifre", type="password", placeholder="Şifre belirleyin")
                                    
                                    if st.form_submit_button("Giriş Yetkisi Tanımla"):
                                        if not new_uname or not new_pass:
                                            st.error("Lütfen tüm alanları doldurun.")
                                        else:
                                            username_taken = any(acc.get("username").lower() == new_uname.lower() for acc in all_accs)
                                            if username_taken:
                                                st.error("❌ Bu kullanıcı adı zaten mevcut!")
                                            else:
                                                h_val, s_val = hash_password(new_pass)
                                                new_acc = {
                                                    "username": new_uname,
                                                    "password_hash": h_val,
                                                    "password_salt": s_val,
                                                    "name": member.get("name"),
                                                    "role": member.get("role", "Geliştirici"),
                                                    "company": "DeDev",
                                                    "location": "Remote",
                                                    "since": "2026",
                                                    "bio": f"{member.get('name')} - Ekip Üyesi Profili.",
                                                    "role_type": "member",
                                                    "permissions": ["dashboard", "projects", "kanban", "timeline", "calendar", "time_tracking", "reports"]
                                                }
                                                data.setdefault("accounts", []).append(new_acc)
                                                save_data(data)
                                                st.success(f"🎉 {member.get('name')} için giriş yetkisi tanımlandı!")
                                                st.rerun()
                        
                        # Delete button
                        if st.button("🗑️ Ekipten Çıkar", key=f"del_worker_{m_id}", type="secondary", use_container_width=True):
                            data["team"] = [m for m in data["team"] if m.get("id") != member.get("id") or m.get("name") != member.get("name")]
                            save_data(data)
                            st.warning(f"'{member.get('name')}' ekibinizden çıkarıldı!")
                            st.rerun()
            else:
                st.info("Bu filtreye uygun ekip üyesi bulunamadı.")

        with col_w2:
            st.markdown("### ➕ Yeni Çalışan Ekle")
            with st.form("new_worker_form"):
                w_name = st.text_input("Ad Soyad", placeholder="Örn: Elif Aksoy")
                w_role = st.text_input("Rol / Ünvan", placeholder="Örn: Frontend Developer")
                w_dept = st.selectbox("Departman", dept_names)
                w_email = st.text_input("E-posta", placeholder="Örn: elif@dedev.com")
                w_status = st.selectbox("Durum", ["Aktif", "İzinli", "Ayrıldı"])
                
                # Username and password fields for automatic login credentials creation
                st.markdown("---")
                st.markdown("##### 🔑 Giriş Yetkisi Tanımla (İsteğe Bağlı)")
                w_username = st.text_input("Giriş Kullanıcı Adı", placeholder="Örn: elif_demir")
                w_password = st.text_input("Giriş Şifresi", type="password", placeholder="Örn: 123456")
                
                if st.form_submit_button("Çalışanı Ekip Listesine Ekle"):
                    if w_name:
                        new_member = {
                            "id": f"USR-{str(uuid.uuid4())[:6].upper()}",
                            "name": w_name,
                            "role": w_role if w_role else "Geliştirici",
                            "department": w_dept,
                            "email": w_email if w_email else f"{w_name.lower().replace(' ', '')}@dedev.com",
                            "status": w_status
                        }
                        data["team"].append(new_member)
                        
                        if w_username and w_password:
                            from utils.data_handler import get_all_accounts
                            from utils.encryption import hash_password
                            
                            all_accs = get_all_accounts()
                            username_taken = any(acc.get("username").lower() == w_username.lower() for acc in all_accs)
                            if username_taken:
                                st.warning("⚠️ Çalışan eklendi ancak bu kullanıcı adı zaten mevcut olduğu için giriş yetkisi oluşturulamadı! Lütfen listeden başka bir kullanıcı adı verin.")
                            else:
                                h_val, s_val = hash_password(w_password)
                                new_acc = {
                                    "username": w_username,
                                    "password_hash": h_val,
                                    "password_salt": s_val,
                                    "name": w_name,
                                    "role": w_role if w_role else "Geliştirici",
                                    "company": data.get("accounts", [{}])[0].get("company", "DeDev") if data.get("accounts") else "DeDev",
                                    "location": "Remote",
                                    "since": "2026",
                                    "bio": f"{w_name} - Ekip Üyesi Profili.",
                                    "role_type": "member",
                                    "permissions": ["dashboard", "projects", "kanban", "timeline", "calendar", "time_tracking", "reports"]
                                }
                                data.setdefault("accounts", []).append(new_acc)
                                st.success(f"🔑 {w_name} için '{w_username}' kullanıcı adı ile giriş yetkisi başarıyla tanımlandı!")
                        
                        save_data(data)
                        st.success(f"🎉 {w_name} başarıyla ekibe dahil edildi!")
                        st.rerun()
                    else:
                        st.error("Çalışan ismi boş bırakılamaz.")

    # =============================================================
    # SEKME 2: DEPARTMAN YÖNETİMİ
    # =============================================================
    with tab_depts:
        col_d1, col_d2 = st.columns([2, 1])

        with col_d1:
            st.markdown("### 🏢 Aktif Departmanlar")
            st.markdown("""
            <div style="font-size: 13px; color: #9ca3af; margin-bottom: 20px;">
                Mevcut tüm iş birimleri ve departmanlar. Her departmandaki çalışan sayısı anlık olarak gösterilmektedir.
            </div>
            """, unsafe_allow_html=True)

            cols = st.columns(2)
            for idx, dept in enumerate(data["departments"]):
                col_idx = idx % 2
                
                # Count employees
                emp_count = sum(1 for m in data["team"] if m.get("department") == dept["name"])
                if dept["name"] == "Yönetim":
                    emp_count += 1 # Include Owner
                    
                with cols[col_idx]:
                    st.markdown(clean_html(f"""
                    <div style="background: rgba(255,255,255,0.02); padding: 20px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.05); border-left: 4px solid {dept['color']}; margin-bottom: 15px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                            <span style="font-size: 24px;">{dept['icon']}</span>
                            <span style="background: {dept['color']}20; color: {dept['color']}; font-size: 11px; font-weight: bold; padding: 3px 8px; border-radius: 12px;">{emp_count} Çalışan</span>
                        </div>
                        <div style="font-weight: 700; color: white; font-size: 16px;">{dept['name']}</div>
                        <div style="color: #9ca3af; font-size: 11px; margin-top: 6px; line-height: 1.4; min-height: 40px;">{dept['description']}</div>
                    </div>
                    """), unsafe_allow_html=True)
                    
                    # Cannot delete legacy system departments
                    legacy_depts = ["Yazılım Geliştirme", "Yönetim"]
                    if dept["name"] not in legacy_depts:
                        if st.button(f"🗑️ Departmanı Sil", key=f"del_dept_{dept['id']}", type="secondary", use_container_width=True):
                            # Reassign workers to default
                            for m in data["team"]:
                                if m.get("department") == dept["name"]:
                                    m["department"] = "Yazılım Geliştirme"
                            data["departments"] = [d for d in data["departments"] if d["id"] != dept["id"]]
                            save_data(data)
                            st.warning(f"'{dept['name']}' departmanı silindi! Bu departmandaki tüm çalışanlar 'Yazılım Geliştirme' departmanına aktarıldı.")
                            st.rerun()

        with col_d2:
            st.markdown("### 🏢 Yeni Departman Ekle")
            with st.form("new_dept_form"):
                d_name = st.text_input("Departman Adı", placeholder="Örn: Mobil Geliştirme")
                d_desc = st.text_area("Açıklama", placeholder="Departmanın görev tanımı ve hedefleri...")
                
                col_icon, col_color = st.columns(2)
                d_icon = col_icon.selectbox("İkon", ["💻", "🧠", "🎨", "📈", "👑", "📞", "🛠️", "⚖️", "🔬", "🛒", "🔒", "💡"])
                d_color = col_color.selectbox("Renk", [
                    ("Mavi", "#3b82f6"),
                    ("Yeşil", "#10b981"),
                    ("Mor", "#8b5cf6"),
                    ("Pembe", "#ec4899"),
                    ("Turuncu", "#f59e0b"),
                    ("Kırmızı", "#ef4444"),
                    ("Turkuaz", "#14b8a6")
                ], format_func=lambda x: x[0])[1]
                
                if st.form_submit_button("Departmanı Kaydet"):
                    if d_name:
                        # Check duplicate
                        if any(d["name"].lower() == d_name.lower() for d in data["departments"]):
                            st.error("Bu departman zaten mevcut!")
                        else:
                            new_dept = {
                                "id": f"DEP-{str(uuid.uuid4())[:6].upper()}",
                                "name": d_name,
                                "description": d_desc if d_desc else "İş geliştirme ve takip departmanı.",
                                "icon": d_icon,
                                "color": d_color
                            }
                            data["departments"].append(new_dept)
                            save_data(data)
                            st.success(f"🎉 {d_name} departmanı başarıyla kuruldu!")
                            st.rerun()
                    else:
                        st.error("Departman adı boş olamaz.")

    # =============================================================
    # SEKME 3: EKİP ANALİTİĞİ & GRAFİKLER
    # =============================================================
    with tab_stats:
        st.markdown("### 📊 Ekip Demografisi ve Analitik")
        
        # Calculations
        tot_members = len(data["team"]) + 1 # Include Owner
        tot_depts = len(data["departments"])
        
        active_members = sum(1 for m in data["team"] if m.get("status", "Aktif") == "Aktif") + 1
        active_ratio = int((active_members / tot_members) * 100) if tot_members else 0
        
        # Most populated department
        dept_counts = {}
        for m in data["team"]:
            d = m.get("department", "Yazılım Geliştirme")
            dept_counts[d] = dept_counts.get(d, 0) + 1
        dept_counts["Yönetim"] = dept_counts.get("Yönetim", 0) + 1 # Owner
        
        most_pop_dept = max(dept_counts, key=dept_counts.get) if dept_counts else "Yazılım Geliştirme"
        most_pop_val = dept_counts.get(most_pop_dept, 1)
        
        cols_metric = st.columns(4)
        cols_metric[0].metric("Toplam Çalışan", tot_members, help="Proje sahibi ve ekip üyeleri dahil")
        cols_metric[1].metric("Toplam Departman", tot_depts)
        cols_metric[2].metric("Aktif Çalışan Oranı", f"%{active_ratio}")
        cols_metric[3].metric("En Kalabalık Departman", f"{most_pop_dept} ({most_pop_val})")
        
        st.markdown("---")
        
        col_c1, col_c2 = st.columns(2)
        
        with col_c1:
            st.markdown("#### 🍩 Departman Dağılımı")
            if dept_counts:
                labels = list(dept_counts.keys())
                values = list(dept_counts.values())
                
                # Fetch color mapping based on department configuration
                marker_colors = []
                for label in labels:
                    dept_obj = dept_map.get(label, {"color": "#6b7280"})
                    marker_colors.append(dept_obj["color"])
                    
                fig_dept_pie = go.Figure(data=[go.Pie(
                    labels=labels,
                    values=values,
                    hole=.4,
                    marker=dict(colors=marker_colors),
                    textinfo='value+percent',
                    textfont=dict(size=12, color='white'),
                    hovertemplate="<b>%{label}</b><br>Çalışan Sayısı: %{value} (%{percent})<extra></extra>"
                )])
                
                fig_dept_pie.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    height=280,
                    margin=dict(l=10, r=10, t=10, b=10),
                    legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
                )
                st.plotly_chart(fig_dept_pie, use_container_width=True)
            else:
                st.info("Gösterilecek grafik verisi bulunamadı.")
                
        with col_c2:
            st.markdown("#### 📈 Çalışan Durum Analizi")
            
            status_counts = {"Aktif": 1, "İzinli": 0, "Ayrıldı": 0} # Owner is Active
            for m in data["team"]:
                st_val = m.get("status", "Aktif")
                status_counts[st_val] = status_counts.get(st_val, 0) + 1
                
            fig_status_bar = go.Figure()
            fig_status_bar.add_trace(go.Bar(
                x=list(status_counts.keys()),
                y=list(status_counts.values()),
                marker_color=["#10b981", "#f59e0b", "#ef4444"],
                hovertemplate="Durum: %{x}<br>Kişi Sayısı: %{y}<extra></extra>"
            ))
            
            fig_status_bar.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                height=280,
                margin=dict(l=40, r=20, t=20, b=40),
                xaxis=dict(showgrid=False, title="Çalışan Durumu"),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)', title="Kişi Sayısı", dtick=1)
            )
            st.plotly_chart(fig_status_bar, use_container_width=True)
