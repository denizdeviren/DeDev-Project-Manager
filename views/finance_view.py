import streamlit as st
import uuid
from datetime import datetime
from utils.data_handler import save_data

def clean_html(html_str):
    return "\n".join([line.strip() for line in html_str.split("\n")])

def show_finance(data):
    st.markdown('<div class="section-title">💰 Bütçe & Gider Takibi</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Sunucu masrafları, API maliyetleri ve lisans harcamaları</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown('### 💸 Gider Ekle')
        with st.form("new_expense_form"):
            e_title = st.text_input("Açıklama", placeholder="Örn: Vercel Pro Plan")
            e_amount = st.number_input("Tutar ($)", min_value=0.0, step=1.0)
            e_proj = st.selectbox("İlgili Proje", ["Genel (Tüm Projeler)"] + [p['name'] for p in data.get("projects", [])])
            e_date = st.date_input("Tarih")
            
            if st.form_submit_button("Ekle"):
                if e_title and e_amount > 0:
                    proj_id = None
                    if e_proj != "Genel (Tüm Projeler)":
                        proj_id = next((p['id'] for p in data["projects"] if p['name'] == e_proj), None)
                    
                    data.setdefault("finances", []).append({
                        "id": f"EXP-{str(uuid.uuid4())[:6].upper()}",
                        "title": e_title,
                        "amount": e_amount,
                        "project_id": proj_id,
                        "date": e_date.strftime("%Y-%m-%d")
                    })
                    save_data(data)
                    st.success("Gider eklendi!")
                    st.rerun()

    with col2:
        st.markdown('### 📊 Toplam Maliyet & Dağılım')
        total_exp = sum(e['amount'] for e in data.get("finances", []))
        st.markdown(clean_html(f"""
        <div style="background: rgba(239, 68, 68, 0.1); border: 1px solid #ef4444; border-radius: 12px; padding: 20px; text-align: center; margin-bottom: 20px;">
            <div style="font-size: 14px; color: #ef4444; font-weight: 600; text-transform: uppercase;">Toplam Harcama</div>
            <div style="font-size: 36px; font-weight: bold; color: white;">${total_exp:.2f}</div>
        </div>
        """), unsafe_allow_html=True)

        if "finances" in data and data["finances"]:
            st.markdown("**Giderler:**")
            for exp in reversed(data["finances"]):
                p_name = "Genel" if not exp['project_id'] else next((p['name'] for p in data["projects"] if p['id'] == exp['project_id']), "Bilinmeyen")
                
                # Column structure to separate card and the delete button
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
                    # Space to align vertically or simple button
                    st.write("")  # small spacer
                    if st.button("🗑️", key=f"del_exp_{exp['id']}", help="Gideri Sil", use_container_width=True):
                        data["finances"] = [e for e in data["finances"] if e["id"] != exp["id"]]
                        save_data(data)
                        st.toast("Gider başarıyla silindi!", icon="🗑️")
                        st.rerun()
        else:
            st.info("Henüz eklenmiş bir harcama yok.")

