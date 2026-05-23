import streamlit as st
import os
import base64
from datetime import datetime
from utils.data_handler import save_data, get_filtered_elements

def clean_html(html_str):
    return "\n".join([line.strip() for line in html_str.split("\n")])

def show_archive(data):
    st.markdown('<div class="section-title">📚 ERP Arşiv Odası & Belge Yönetimi</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">PDF doküman depolama, proje arşivleme ve print-ready PDF/HTML raporlama merkezi</div>', unsafe_allow_html=True)
    
    # Establish archives directories
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    ARCHIVE_DIR = os.path.normpath(os.path.join(os.path.dirname(CURRENT_DIR), "archives"))
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    
    active_owner = data.get("active_owner", "Deniz Deviren")
    
    # Ensure archived projects list exists
    if "archived_projects" not in data:
        data["archived_projects"] = []
        
    tab_proj_archive, tab_docs, tab_pdf_export = st.tabs([
        "📁 Proje Arşivleme", 
        "📄 Belge & PDF Deposu (Viewer)", 
        "📊 İşleyişi Rapor Olarak İndirme"
    ])
    
    # =========================================================================
    # SEKME 1: PROJE ARŞİVLEME
    # =========================================================================
    with tab_proj_archive:
        col_act, col_arc = st.columns(2)
        
        with col_act:
            st.markdown("### 🟢 Aktif Projeleriniz")
            active_owner_projects = [p for p in data.get("projects", []) if p.get("owner_name", "Deniz Deviren") == active_owner]
            
            if active_owner_projects:
                for proj in active_owner_projects:
                    c1, c2 = st.columns([4, 1.5])
                    with c1:
                        st.markdown(clean_html(f"""
                        <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.04); padding: 12px; border-radius: 8px; margin-bottom: 10px;">
                            <span style="font-weight: bold; color: white;">{proj['name']}</span><br>
                            <span style="font-size: 11px; color: #9ca3af;">{proj.get('category', 'Kategori yok')} | %{proj.get('progress', 0)} Başarı</span>
                        </div>
                        """), unsafe_allow_html=True)
                    with c2:
                        st.write("")  # align
                        if st.button("📁 Arşivle", key=f"arc_btn_{proj['id']}", use_container_width=True):
                            # Move from projects to archived_projects
                            data["projects"] = [p for p in data["projects"] if p["id"] != proj["id"]]
                            proj["archived_at"] = datetime.now().strftime("%Y-%m-%d")
                            data["archived_projects"].append(proj)
                            save_data(data)
                            st.toast(f"'{proj['name']}' başarıyla arşive kaldırıldı.", icon="📁")
                            st.rerun()
            else:
                st.info("Aktif projeniz bulunmamaktadır.")
                
        with col_arc:
            st.markdown("### 📂 Arşivlenen Projeler")
            archived_owner_projects = [p for p in data.get("archived_projects", []) if p.get("owner_name", "Deniz Deviren") == active_owner]
            
            if archived_owner_projects:
                for proj in archived_owner_projects:
                    c1, c2 = st.columns([4, 1.5])
                    with c1:
                        st.markdown(clean_html(f"""
                        <div style="background: rgba(255,255,255,0.01); border: 1px solid rgba(255,255,255,0.03); padding: 12px; border-radius: 8px; margin-bottom: 10px;">
                            <span style="font-weight: bold; color: #9ca3af;">{proj['name']}</span><br>
                            <span style="font-size: 11px; color: #6b7280;">Arşivlenme: {proj.get('archived_at', 'Bilinmiyor')}</span>
                        </div>
                        """), unsafe_allow_html=True)
                    with c2:
                        st.write("")  # align
                        if st.button("🔓 Geri Yükle", key=f"unarc_btn_{proj['id']}", use_container_width=True):
                            # Move from archived_projects to projects
                            data["archived_projects"] = [p for p in data["archived_projects"] if p["id"] != proj["id"]]
                            if "archived_at" in proj:
                                del proj["archived_at"]
                            data["projects"].append(proj)
                            save_data(data)
                            st.toast(f"'{proj['name']}' aktif projelere geri yüklendi.", icon="🔓")
                            st.rerun()
            else:
                st.info("Arşivlenmiş projeniz bulunmuyor.")

    # =========================================================================
    # SEKME 2: BELGE & PDF DEPOSU & PDF VIEWER
    # =========================================================================
    with tab_docs:
        col_up, col_view = st.columns([2, 3])
        
        with col_up:
            st.markdown("### 📤 Belge Yükle")
            uploaded_file = st.file_uploader("Sisteme PDF, Txt veya Görsel yükleyin", type=["pdf", "png", "jpg", "jpeg", "txt"])
            
            if uploaded_file is not None:
                # Save file to archives folder
                file_path = os.path.join(ARCHIVE_DIR, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.success(f"🎉 '{uploaded_file.name}' başarıyla arşive kaydedildi!")
                st.rerun()
                
            st.markdown("---")
            st.markdown("### 📂 Kayıtlı Belgeler")
            files = [f for f in os.listdir(ARCHIVE_DIR) if os.path.isfile(os.path.join(ARCHIVE_DIR, f))]
            
            if files:
                for file in files:
                    fc1, fc2 = st.columns([4, 1.5])
                    with fc1:
                        st.markdown(f"""
                        <div style="font-size: 13px; color: #d1d5db; padding: 6px; background: rgba(255,255,255,0.02); border-radius: 6px; margin-bottom: 5px;">
                            📄 {file}
                        </div>
                        """, unsafe_allow_html=True)
                    with fc2:
                        if st.button("🗑️ Sil", key=f"del_file_{file}", use_container_width=True):
                            os.remove(os.path.join(ARCHIVE_DIR, file))
                            st.toast(f"'{file}' silindi.")
                            st.rerun()
            else:
                st.info("Arşivlenmiş fiziksel belge bulunamadı.")
                
        with col_view:
            st.markdown("### 📄 Uygulama İçi PDF Okuyucu")
            pdf_files = [f for f in files if f.lower().endswith(".pdf")]
            
            if pdf_files:
                selected_pdf = st.selectbox("Görüntülenecek PDF Dosyasını Seçin:", pdf_files)
                
                if selected_pdf:
                    pdf_path = os.path.join(ARCHIVE_DIR, selected_pdf)
                    with open(pdf_path, "rb") as f:
                        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
                        
                    pdf_display = f"""
                    <iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="550px" style="border: none; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.3);"></iframe>
                    """
                    st.markdown(pdf_display, unsafe_allow_html=True)
            else:
                st.info("Okunacak PDF dosyası bulunmuyor. Sol menüden PDF yükleyebilirsiniz.")

    # =========================================================================
    # SEKME 3: İŞLEYİŞİ RAPOR OLARAK İNDİRME
    # =========================================================================
    with tab_pdf_export:
        st.markdown("### 📊 İş Akışı & Rapor İndirme Aracı")
        st.markdown("""
        Bu alandan seçeceğiniz herhangi bir projenin tüm detaylı işleyişini, tamamlanan kilometre taşlarını, bütçesini, 
        ekibini ve efor takvimini şık, yazdırılabilir bir HTML/PDF ERP raporu olarak dışa aktarabilirsiniz.
        """)
        
        all_owner_projects = active_owner_projects + archived_owner_projects
        
        if all_owner_projects:
            selected_report_proj = st.selectbox("Raporu Üretilecek Proje:", [p['name'] for p in all_owner_projects])
            
            if selected_report_proj:
                proj = next((p for p in all_owner_projects if p['name'] == selected_report_proj), None)
                
                # Fetch details for the report
                proj_tasks = [t for t in data.get("tasks", []) if t.get("project_id") == proj["id"]]
                proj_expenses = [e for e in data.get("finances", []) if e.get("project_id") == proj["id"]]
                proj_invoices = [i for i in data.get("invoices", []) if i.get("project_id") == proj["id"] and i.get("status") == "Ödendi"]
                
                total_income = sum(float(i.get("grand_total", 0)) for i in proj_invoices)
                total_expenses = sum(float(e.get("amount", 0)) for e in proj_expenses)
                net_profit = total_income - total_expenses
                
                milestones_html = ""
                for ms in proj.get("milestones", []):
                    status_symbol = "✅ Completed" if ms.get("status") == "Completed" or ms.get("done", False) else "⏳ Pending"
                    milestones_html += f"<li><b>{ms['name']}</b> ({ms.get('date', '')}) - {status_symbol}</li>"
                    
                tasks_html = ""
                for t in proj_tasks:
                    tasks_html += f"""
                    <tr>
                        <td>{t['title']}</td>
                        <td>{t.get('assignee') or 'Bilinmeyen'}</td>
                        <td>{t.get('priority', 'Medium')}</td>
                        <td style="text-align: right;">{t['status']}</td>
                    </tr>
                    """
                    
                report_html = f"""
                <html>
                <head>
                <style>
                    body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #333; margin: 45px; line-height: 1.6; }}
                    .header {{ border-bottom: 3px solid #764ba2; padding-bottom: 15px; margin-bottom: 25px; display: flex; justify-content: space-between; }}
                    .h-title {{ font-size: 28px; font-weight: bold; color: #764ba2; }}
                    .section-h {{ font-size: 18px; font-weight: bold; color: #667eea; border-bottom: 1px solid #ddd; padding-bottom: 5px; margin-top: 25px; }}
                    .table-erp {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
                    .table-erp th {{ background-color: #667eea; color: white; padding: 8px; text-align: left; }}
                    .table-erp td {{ padding: 8px; border-bottom: 1px solid #eee; font-size: 13px; }}
                    .summary-box {{ background-color: #f7f9fa; border: 1px solid #e2e8f0; padding: 15px; border-radius: 8px; margin-top: 15px; display: flex; justify-content: space-between; }}
                    .sum-val {{ font-size: 18px; font-weight: bold; color: #764ba2; }}
                </style>
                </head>
                <body>
                    <div class="header">
                        <div>
                            <div class="h-title">{proj['name']}</div>
                            <div>Kategori: {proj.get('category', 'Genel')} | Sahibi: {active_owner}</div>
                        </div>
                        <div style="text-align: right; font-size: 12px; color: #777;">
                            Rapor Tarihi: {datetime.now().strftime("%Y-%m-%d")}<br>
                            Command Center ERP
                        </div>
                    </div>
                    
                    <div class="section-h">📝 Proje Tanımı</div>
                    <p>{proj.get('description', 'Açıklama girilmemiş.')}</p>
                    
                    <div class="summary-box">
                        <div>
                            <div>Proje Durumu</div>
                            <div class="sum-val">{proj.get('status', 'In Progress')}</div>
                        </div>
                        <div>
                            <div>İlerleme Yüzdesi</div>
                            <div class="sum-val">%{proj.get('progress', 0)}</div>
                        </div>
                        <div>
                            <div>Net Kâr (ERP ROI)</div>
                            <div class="sum-val" style="color: {'#10b981' if net_profit >= 0 else '#ef4444'}">${net_profit:,.2f}</div>
                        </div>
                    </div>
                    
                    <div class="section-h">🎯 Kilometre Taşları (Milestones)</div>
                    <ul>
                        {milestones_html if milestones_html else "<li>Kilometre taşı bulunamadı.</li>"}
                    </ul>
                    
                    <div class="section-h">📋 Görev Listesi ve Dağılımı</div>
                    <table class="table-erp">
                        <thead>
                            <tr>
                                <th>Görev Başlığı</th>
                                <th>Atanan</th>
                                <th>Öncelik</th>
                                <th style="text-align: right;">Durum</th>
                            </tr>
                        </thead>
                        <tbody>
                            {tasks_html if tasks_html else "<tr><td colspan='4'>Görev bulunmamaktadır.</td></tr>"}
                        </tbody>
                    </table>
                    
                    <div class="section-h">💰 Finansal Analiz Raporu</div>
                    <table class="table-erp" style="margin-top: 10px;">
                        <tr>
                            <td><b>Toplam Gelir (Ödenen Faturalar):</b></td>
                            <td style="text-align: right; color: #10b981; font-weight: bold;">${total_income:,.2f}</td>
                        </tr>
                        <tr>
                            <td><b>Toplam Gider & Harcama Masrafı:</b></td>
                            <td style="text-align: right; color: #ef4444; font-weight: bold;">${total_expenses:,.2f}</td>
                        </tr>
                        <tr style="border-top: 2px solid #667eea;">
                            <td><b>Dönem Kâr / Zarar Durumu:</b></td>
                            <td style="text-align: right; color: {'#10b981' if net_profit >= 0 else '#ef4444'}; font-weight: bold; font-size: 15px;">${net_profit:,.2f}</td>
                        </tr>
                    </table>
                    
                    <div style="margin-top: 60px; font-size: 10px; color: #888; border-top: 1px solid #eee; padding-top: 10px; text-align: center;">
                        Bu rapor DeDev ERP Command Center tarafından oluşturulmuştur. MIT Lisanslı Elektronik Çıktıdır.
                    </div>
                </body>
                </html>
                """
                
                st.download_button(
                    label="📤 Raporu HTML / PDF Rapor Olarak İndir",
                    data=report_html,
                    file_name=f"Rapor-{proj['id']}.html",
                    mime="text/html",
                    use_container_width=True
                )
        else:
            st.info("Rapor oluşturulacak proje bulunamadı.")
