import streamlit as st
import uuid
from datetime import datetime
from utils.data_handler import save_data

def clean_html(html_str):
    return "\n".join([line.strip() for line in html_str.split("\n")])

def show_finance(data):
    st.markdown('<div class="section-title">💰 ERP Bütçe, Gelir & Fatura Takibi</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Fatura kesme, müşteri yönetimi, sunucu masrafları ve net kârlılık oranları</div>', unsafe_allow_html=True)
    
    active_owner = data.get("active_owner", "Deniz Deviren")
    active_projects = [p for p in data.get("projects", []) if p.get("owner_name", "Deniz Deviren") == active_owner]
    active_project_ids = {p["id"] for p in active_projects}
    
    # Initialize invoices in data if not present
    if "invoices" not in data:
        data["invoices"] = []
        
    # Filter finances (expenses) and invoices for active owner
    active_expenses = [f for f in data.get("finances", []) if not f.get("project_id") or f.get("project_id") in active_project_ids]
    active_invoices = [inv for inv in data.get("invoices", []) if not inv.get("project_id") or inv.get("project_id") in active_project_ids]
    
    # ERP Financial Synchronization Calculations
    total_expenses = sum(float(e.get("amount", 0)) for e in active_expenses)
    total_income = sum(float(inv.get("grand_total", 0)) for inv in active_invoices if inv.get("status") == "Ödendi")
    net_profit = total_income - total_expenses
    
    # Render financial command dashboard
    st.markdown("### 📊 ERP Finansal Özet Tablosu")
    col_inc, col_exp, col_prof = st.columns(3)
    
    with col_inc:
        st.markdown(clean_html(f"""
        <div style="background: rgba(16, 185, 129, 0.08); border: 1px solid #10b981; border-radius: 16px; padding: 20px; text-align: center;">
            <div style="font-size: 13px; color: #10b981; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Toplam Gelir (Ödenen Faturalar)</div>
            <div style="font-size: 32px; font-weight: 800; color: white; margin-top: 5px;">${total_income:,.2f}</div>
        </div>
        """), unsafe_allow_html=True)
        
    with col_exp:
        st.markdown(clean_html(f"""
        <div style="background: rgba(239, 68, 68, 0.08); border: 1px solid #ef4444; border-radius: 16px; padding: 20px; text-align: center;">
            <div style="font-size: 13px; color: #ef4444; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Toplam Gider Masrafları</div>
            <div style="font-size: 32px; font-weight: 800; color: white; margin-top: 5px;">${total_expenses:,.2f}</div>
        </div>
        """), unsafe_allow_html=True)
        
    with col_prof:
        prof_color = "#10b981" if net_profit >= 0 else "#ef4444"
        prof_bg = "rgba(16, 185, 129, 0.08)" if net_profit >= 0 else "rgba(239, 68, 68, 0.08)"
        st.markdown(clean_html(f"""
        <div style="background: {prof_bg}; border: 1px solid {prof_color}; border-radius: 16px; padding: 20px; text-align: center;">
            <div style="font-size: 13px; color: {prof_color}; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Net Dönem Kârı (ROI)</div>
            <div style="font-size: 32px; font-weight: 800; color: white; margin-top: 5px;">${net_profit:,.2f}</div>
        </div>
        """), unsafe_allow_html=True)

    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
    
    # 2 Sekmeli ERP Yapısı
    tab_invoices, tab_expenses = st.tabs(["🧾 Fatura Kesme & Gelir Yönetimi", "💸 Gider & Masraf Takibi"])
    
    # =========================================================================
    # TAB 1: FATURA KESME & GELİR YÖNETİMİ
    # =========================================================================
    with tab_invoices:
        col_inv_form, col_inv_list = st.columns([2, 3])
        
        with col_inv_form:
            st.markdown("### 📝 Yeni Fatura Kes")
            
            # Auto-generate default invoice ID
            default_inv_id = f"INV-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:4].upper()}"
            
            with st.form("new_invoice_form"):
                inv_number = st.text_input("Fatura No", value=default_inv_id, help="Faturanın benzersiz takip numarası")
                inv_client = st.text_input("Müşteri / Alıcı Adı", placeholder="Örn: DeDev Tech Ltd.")
                inv_proj = st.selectbox("İlgili Proje", [p['name'] for p in active_projects])
                
                col_sub1, col_sub2 = st.columns(2)
                inv_subtotal = col_sub1.number_input("Hizmet Net Tutarı ($)", min_value=0.0, step=10.0)
                inv_vat = col_sub2.selectbox("KDV / VAT Oranı (%)", [20, 10, 8, 0], index=0)
                
                col_d1, col_d2 = st.columns(2)
                inv_date = col_d1.date_input("Düzenleme Tarihi", value=datetime.now())
                inv_due = col_d2.date_input("Vade Tarihi", value=datetime.now())
                
                inv_status = st.selectbox("Ödeme Durumu", ["Ödendi", "Beklemede", "İptal Edildi"])
                inv_desc = st.text_area("Hizmet Kalemleri Açıklaması", placeholder="Örn: 1 Adet Flutter Mobil Cüzdan Uygulaması Arayüz Tasarımı ve Entegrasyonu.")
                
                if st.form_submit_button("Faturayı Kes"):
                    if inv_client and inv_subtotal > 0:
                        proj_id = next((p['id'] for p in active_projects if p['name'] == inv_proj), None)
                        
                        # Calculations
                        tax_amount = (inv_subtotal * inv_vat) / 100
                        grand_total = inv_subtotal + tax_amount
                        
                        data["invoices"].append({
                            "id": inv_number,
                            "client_name": inv_client,
                            "project_id": proj_id,
                            "project_name": inv_proj,
                            "subtotal": float(inv_subtotal),
                            "vat_rate": int(inv_vat),
                            "tax_amount": float(tax_amount),
                            "grand_total": float(grand_total),
                            "date": inv_date.strftime("%Y-%m-%d"),
                            "due_date": inv_due.strftime("%Y-%m-%d"),
                            "status": inv_status,
                            "description": inv_desc if inv_desc else "Hizmet bedeli."
                        })
                        save_data(data)
                        st.toast("🎉 Fatura başarıyla kesildi ve sisteme işlendi!", icon="🎉")
                        st.rerun()
                    else:
                        st.error("Lütfen müşteri adını ve tutarını girin.")
                        
        with col_inv_list:
            st.markdown("### 🏢 Kesilen Faturalar")
            
            if active_invoices:
                for inv in reversed(active_invoices):
                    status_badge_color = "#10b981" if inv["status"] == "Ödendi" else ("#f59e0b" if inv["status"] == "Beklemede" else "#ef4444")
                    status_badge_bg = "rgba(16, 185, 129, 0.08)" if inv["status"] == "Ödendi" else ("rgba(245, 158, 11, 0.08)" if inv["status"] == "Beklemede" else "rgba(239, 68, 68, 0.08)")
                    
                    inv_col, act_col = st.columns([4, 1.2])
                    
                    with inv_col:
                        st.markdown(clean_html(f"""
                        <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.04); border-left: 3px solid {status_badge_color}; border-radius: 12px; padding: 15px; margin-bottom: 12px;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                                <span style="font-weight: 700; color: white; font-size: 14px;">{inv["client_name"]}</span>
                                <span style="background: {status_badge_bg}; color: {status_badge_color}; border: 1px solid {status_badge_color}; padding: 2px 8px; border-radius: 12px; font-size: 10px; font-weight: bold;">{inv["status"]}</span>
                            </div>
                            <div style="font-size: 11px; color: #9ca3af;">
                                🆔 {inv["id"]} | 📁 {inv.get("project_name", "Bilinmeyen")}
                            </div>
                            <div style="font-size: 12px; color: #d1d5db; margin: 8px 0; line-height: 1.4;">
                                {inv.get("description", "")}
                            </div>
                            <div style="display: flex; justify-content: space-between; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 8px; font-size: 11px; color: #6b7280;">
                                <span>📅 Tarih: {inv["date"]}</span>
                                <span style="font-weight: 700; color: white; font-size: 13px;">Toplam: ${inv["grand_total"]:,.2f}</span>
                            </div>
                        </div>
                        """), unsafe_allow_html=True)
                        
                    with act_col:
                        st.write("")  # spacer
                        # PDF/HTML printing tool
                        pdf_data = f"""
                        <html>
                        <head>
                        <style>
                            body {{ font-family: Arial, sans-serif; color: #333; margin: 40px; line-height: 1.5; }}
                            .header {{ display: flex; justify-content: space-between; border-bottom: 2px solid #667eea; padding-bottom: 20px; margin-bottom: 30px; }}
                            .title {{ font-size: 26px; font-weight: bold; color: #667eea; }}
                            .meta-table {{ width: 100%; margin-bottom: 30px; border-collapse: collapse; }}
                            .meta-table td {{ padding: 6px 0; }}
                            .meta-table td.label {{ font-weight: bold; width: 120px; }}
                            .items-table {{ width: 100%; border-collapse: collapse; margin-bottom: 30px; }}
                            .items-table th {{ background-color: #667eea; color: white; padding: 10px; text-align: left; }}
                            .items-table td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
                            .totals {{ float: right; width: 250px; text-align: right; }}
                            .totals table {{ width: 100%; }}
                            .totals td {{ padding: 6px 0; }}
                            .totals td.bold {{ font-weight: bold; font-size: 16px; border-top: 2px solid #667eea; padding-top: 8px; }}
                        </style>
                        </head>
                        <body>
                            <div class="header">
                                <div>
                                    <div class="title">DeDev Command Center</div>
                                    <div>Solo Full-Stack Developer & ERP</div>
                                </div>
                                <div style="text-align: right;">
                                    <div style="font-size: 20px; font-weight: bold;">RESMİ FATURA</div>
                                    <div style="font-size: 12px; color: #777;">Fatura No: {inv["id"]}</div>
                                </div>
                            </div>
                            
                            <table class="meta-table">
                                <tr>
                                    <td class="label">Müşteri / Alıcı:</td>
                                    <td>{inv["client_name"]}</td>
                                    <td class="label" style="text-align: right;">Düzenleme:</td>
                                    <td style="text-align: right;">{inv["date"]}</td>
                                </tr>
                                <tr>
                                    <td class="label">Proje:</td>
                                    <td>{inv.get("project_name", "Genel")}</td>
                                    <td class="label" style="text-align: right;">Vade:</td>
                                    <td style="text-align: right;">{inv["due_date"]}</td>
                                </tr>
                            </table>
                            
                            <table class="items-table">
                                <thead>
                                    <tr>
                                        <th>Hizmet / Açıklama</th>
                                        <th style="text-align: right; width: 100px;">KDV</th>
                                        <th style="text-align: right; width: 120px;">Tutar</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td>{inv["description"]}</td>
                                        <td style="text-align: right;">%{inv["vat_rate"]}</td>
                                        <td style="text-align: right;">${inv["subtotal"]:,.2f}</td>
                                    </tr>
                                </tbody>
                            </table>
                            
                            <div class="totals">
                                <table>
                                    <tr>
                                        <td>Net Tutar:</td>
                                        <td>${inv["subtotal"]:,.2f}</td>
                                    </tr>
                                    <tr>
                                        <td>Hesaplanan KDV (%{inv["vat_rate"]}):</td>
                                        <td>${inv["tax_amount"]:,.2f}</td>
                                    </tr>
                                    <tr>
                                        <td class="bold">Genel Toplam:</td>
                                        <td class="bold">${inv["grand_total"]:,.2f}</td>
                                    </tr>
                                </table>
                            </div>
                            <div style="margin-top: 150px; font-size: 11px; color: #777; border-top: 1px solid #ddd; padding-top: 10px;">
                                Not: Bu fatura DeDev ERP Command Center sistemi tarafından elektronik ortamda oluşturulmuştur. MIT Lisanslıdır.
                            </div>
                        </body>
                        </html>
                        """
                        
                        st.download_button(
                            label="📥 PDF / Rapor İndir",
                            data=pdf_data,
                            file_name=f"Fatura-{inv['id']}.html",
                            mime="text/html",
                            key=f"dl_inv_{inv['id']}",
                            use_container_width=True
                        )
                        
                        if st.button("🗑️ Sil", key=f"del_inv_{inv['id']}", use_container_width=True):
                            data["invoices"] = [iv for iv in data["invoices"] if iv["id"] != inv["id"]]
                            save_data(data)
                            st.toast("Fatura başarıyla silindi!", icon="🗑️")
                            st.rerun()
            else:
                st.info("Henüz kesilmiş fatura kaydı yok.")
                
    # =========================================================================
    # TAB 2: GİDER & MASRAF TAKİBİ
    # =========================================================================
    with tab_expenses:
        col_exp_form, col_exp_list = st.columns([1, 2])
        
        with col_exp_form:
            st.markdown('### 💸 Gider Ekle')
            with st.form("new_expense_form"):
                e_title = st.text_input("Açıklama", placeholder="Örn: Vercel Pro Plan")
                e_amount = st.number_input("Tutar ($)", min_value=0.0, step=1.0)
                e_proj = st.selectbox("İlgili Proje", ["Genel (Tüm Projeler)"] + [p['name'] for p in active_projects])
                e_date = st.date_input("Tarih", key="exp_date")
                
                if st.form_submit_button("Ekle"):
                    if e_title and e_amount > 0:
                        proj_id = None
                        if e_proj != "Genel (Tüm Projeler)":
                            proj_id = next((p['id'] for p in active_projects if p['name'] == e_proj), None)
                        
                        data.setdefault("finances", []).append({
                            "id": f"EXP-{str(uuid.uuid4())[:6].upper()}",
                            "title": e_title,
                            "amount": e_amount,
                            "project_id": proj_id,
                            "date": e_date.strftime("%Y-%m-%d")
                        })
                        save_data(data)
                        st.toast("Gider başarıyla eklendi!", icon="💸")
                        st.rerun()
                        
        with col_exp_list:
            st.markdown('### 📊 Gider Hareketleri')
            
            if active_expenses:
                for exp in reversed(active_expenses):
                    p_name = "Genel" if not exp['project_id'] else next((p['name'] for p in active_projects if p['id'] == exp['project_id']), "Bilinmeyen")
                    
                    item_col, del_col = st.columns([5, 1])
                    
                    with item_col:
                        st.markdown(clean_html(f"""
                        <div style="display: flex; justify-content: space-between; background: rgba(255,255,255,0.02); padding: 12px; border-radius: 8px; border-left: 2px solid #ef4444; height: 100%;">
                            <div>
                                <div style="font-size: 14px; font-weight: 600; color: white;">{exp['title']}</div>
                                <div style="font-size: 11px; color: #9ca3af;">{p_name} | {exp['date']}</div>
                            </div>
                            <div style="color: #ef4444; font-weight: bold; font-size: 16px; align-self: center; margin-right: 10px;">${exp['amount']}</div>
                        </div>
                        """), unsafe_allow_html=True)
                    
                    with del_col:
                        st.write("")  # spacer
                        if st.button("🗑️", key=f"del_exp_{exp['id']}", help="Gideri Sil", use_container_width=True):
                            data["finances"] = [e for e in data["finances"] if e["id"] != exp["id"]]
                            save_data(data)
                            st.toast("Gider başarıyla silindi!", icon="🗑️")
                            st.rerun()
            else:
                st.info("Henüz eklenmiş bir harcama yok.")
