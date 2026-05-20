import streamlit as st
import textwrap

def show_api_docs(data):
    st.markdown('<div class="section-title">📖 API Dokümantasyonu</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Servis kotaları, endpoint adresleri ve API anahtarları yönetimi</div>', unsafe_allow_html=True)
    
    st.markdown(textwrap.dedent("""
    <div style="background: rgba(255,255,255,0.05); border-radius: 12px; padding: 16px;">
        <h3 style="color: white; font-size: 16px; margin-bottom: 12px;">🤖 OpenAI API</h3>
        <p style="color: #d1d5db; font-size: 14px;"><strong>Bağlı Proje:</strong> Washington Emlak AI</p>
        <div style="background: #1f2937; padding: 8px; border-radius: 6px; font-family: monospace; color: #34d399; font-size: 12px;">Endpoint: https://api.openai.com/v1/chat/completions</div>
        <p style="color: #9ca3af; font-size: 12px; margin-top: 8px;">Kota Durumu: %45 Kullanıldı</p>
    </div>
    """), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown(textwrap.dedent("""
    <div style="background: rgba(255,255,255,0.05); border-radius: 12px; padding: 16px;">
        <h3 style="color: white; font-size: 16px; margin-bottom: 12px;">🔥 Firebase REST API</h3>
        <p style="color: #d1d5db; font-size: 14px;"><strong>Bağlı Proje:</strong> ComTerms DeDe AI</p>
        <div style="background: #1f2937; padding: 8px; border-radius: 6px; font-family: monospace; color: #34d399; font-size: 12px;">Endpoint: https://[PROJECT_ID].firebaseio.com/</div>
        <p style="color: #9ca3af; font-size: 12px; margin-top: 8px;">Durum: Sağlıklı 🟢</p>
    </div>
    """), unsafe_allow_html=True)
