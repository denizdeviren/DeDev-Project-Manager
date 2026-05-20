import streamlit as st
from datetime import datetime
from utils.data_handler import save_data

def show_notes(data):
    st.markdown('<div class="section-title">📝 Hızlı Notlar</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Geliştirme notları, fikirler ve toplantı özetleri</div>', unsafe_allow_html=True)

    with st.form("new_note_form"):
        new_note_title = st.text_input("Not Başlığı", placeholder="Örn: AI model güncellemesi")
        new_note_content = st.text_area("İçerik (Markdown destekler)", height=150)
        if st.form_submit_button("Notu Kaydet"):
            if new_note_title and new_note_content:
                if "notes" not in data:
                    data["notes"] = []
                data["notes"].append({
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "title": new_note_title,
                    "content": new_note_content
                })
                save_data(data)
                st.success("Not kaydedildi!")
                st.rerun()

    st.markdown("---")
    st.markdown('### 📌 Kaydedilen Notlar')
    if "notes" in data and data["notes"]:
        for note in reversed(data["notes"]):
            with st.expander(f"{note['title']} ({note['date']})"):
                st.markdown(note['content'])
                if st.button("Sil", key=f"del_{note['title']}_{note['date']}"):
                    data["notes"].remove(note)
                    save_data(data)
                    st.rerun()
    else:
        st.info("Henüz hiç not eklenmemiş.")
