import streamlit as st

def show_about(data):
    st.markdown('<div class="section-title">ℹ️ Hakkında & Yasal Sorumluluk Sınırı</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">DeDev Command Center V2 metodolojisi, hesaplama kriterleri ve yasal bildirimler</div>', unsafe_allow_html=True)

    # 1. Premium Glassmorphic Header Card
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); 
                border: 1px solid rgba(102, 126, 234, 0.2); border-radius: 20px; padding: 30px; margin-bottom: 25px; 
                backdrop-filter: blur(15px); box-shadow: 0 10px 30px rgba(0,0,0,0.2);">
        <h3 style="color: white; margin-top: 0; font-size: 20px; font-weight: 700; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
            🚀 DeDev Command Center V2.0
        </h3>
        <p style="color: #d1d5db; font-size: 14px; line-height: 1.6; margin-bottom: 15px;">
            DeDev Command Center; yazılım geliştiriciler, dijital ajanslar ve teknoloji şirketleri için özel olarak geliştirilmiş, 
            kendi kendine yeten modüler bir Proje Yönetimi ve Finansal Denetim (ERP) simülasyon aracıdır.
            Bu platformda yer alan finansal tablolar, defter-i kebir kayıtları ve operasyonel metrik puanlamaları, 
            modern yönetim modellerine dayanarak dinamik algoritmalar tarafından işlenmektedir.
        </p>
        <span style="background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.3); color: #a7f3d0; 
                     padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 700; display: inline-block;">
            📄 MIT Lisansı Altında Dağıtılmaktadır
        </span>
    </div>
    """, unsafe_allow_html=True)

    # Tabs for different details
    tab_calc, tab_disclaimer = st.tabs([
        "📊 Hesaplama Metodolojileri",
        "⚖️ Yasal Sorumluluk Reddi (Disclaimer)"
    ])

    with tab_calc:
        st.markdown("### 🧮 Metrikler ve Algoritmik Hesaplamalar")
        
        # Grid layout for explanation of metrics
        col_c1, col_c2 = st.columns(2)
        
        with col_c1:
            st.markdown("""
            <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 16px; padding: 20px; margin-bottom: 15px; min-height: 290px;">
                <h4 style="color: #667eea; margin-top:0; font-size:16px; font-weight:700; display:flex; align-items:center; gap:8px;">
                    📈 DeDev Findeks Skoru Kriterleri (350 - 1900)
                </h4>
                <p style="color: #9ca3af; font-size:12.5px; line-height:1.6;">
                    Uygulamada yer alan Findeks Kredi Notu / Proje Performans Puanı, şirketinizin operasyonel ve finansal kararlılığını ölçen 4 temel alt metriğe dayanır:
                </p>
                <ul style="color: #d1d5db; font-size:12.5px; line-height:1.8; padding-left: 20px;">
                    <li><b>Proje Başarı & Teslim Oranı (%30 - Maks 500 Puan):</b> Tamamlanan / toplam proje oranı ve projelerin gecikme sürelerine göre hesaplanır.</li>
                    <li><b>Görev Bitirme Yoğunluğu (%30 - Maks 500 Puan):</b> Kanban panosundaki 'Done' (Tamamlandı) statüsündeki işlerin hızı ve efor yoğunluğu.</li>
                    <li><b>Efor & Zaman Kayıtları (%20 - Maks 400 Puan):</b> Ekip üyelerinin sisteme girdiği zaman loglarının sürekliliği ve veri kararlılığı.</li>
                    <li><b>ERP ROI & Fatura Kârlılığı (%20 - Maks 500 Puan):</b> Gelir-gider oranınız (ROI) ve kesilen kurumsal faturaların tahsilat başarı derecesi.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        with col_c2:
            st.markdown("""
            <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 16px; padding: 20px; margin-bottom: 15px; min-height: 290px;">
                <h4 style="color: #10b981; margin-top:0; font-size:16px; font-weight:700; display:flex; align-items:center; gap:8px;">
                    💰 Çift Taraflı Muhasebe & ERP Metotları
                </h4>
                <p style="color: #9ca3af; font-size:12.5px; line-height:1.6;">
                    Sistemdeki finansal analizler ve muhasebe raporları, standart çift taraflı (double-entry) defter-i kebir yapısını temel alır:
                </p>
                <ul style="color: #d1d5db; font-size:12.5px; line-height:1.8; padding-left: 20px;">
                    <li><b>Borç (Debit) & Alacak (Credit) Dengesi:</b> Her işlem (fatura veya gider girişi) mutlaka dengeli iki ayrı yevmiye kaydı oluşturur.</li>
                    <li><b>Dinamik Mizan (Trial Balance):</b> Şirketin borç/alacak hesap toplamlarının eşitliğini doğrulamak amacıyla matematiksel mizan dengesi kurulur.</li>
                    <li><b>Bilanço ve Gelir Tablosu:</b> Varlıklar = Yükümlülükler + Özkaynaklar denkliği ile Net Dönem Kâr/Zararı anlık hesaplanır.</li>
                    <li><b>Proje ROI (Yatırım Getirisi):</b> İlgili projeye harcanan bütçe ile elde edilen faturalandırılmış gelir arasındaki oran formüle edilir.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    with tab_disclaimer:
        st.markdown("### ⚖️ Yasal Sorumluluk Reddi (Disclaimer)")
        
        st.markdown("""
        <div style="background: rgba(239, 68, 68, 0.05); border: 1px solid rgba(239, 68, 68, 0.2); border-radius: 16px; padding: 24px; margin-bottom: 20px;">
            <div style="color: #fca5a5; font-size: 16px; font-weight: 700; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
                ⚠️ ÖNEMLİ HUKUKİ BİLDİRİM & GARANTİ YOKSUNLUĞU (AS IS)
            </div>
            <p style="color: #fca5a5; font-size: 13px; line-height: 1.7; margin-bottom: 15px; text-align: justify;">
                <b>1. YALNIZCA SİMÜLASYON VE BİLGİ AMAÇLIDIR:</b><br>
                DeDev Command Center uygulaması içerisinde hesaplanan tüm metrikler, Findeks puanları, finansal tablolar, 
                bilanço dengeleri, KDV/vergi tutarları, defter-i kebir kayıtları ve grafik analizleri 
                <b>tamamen simülasyon, eğitim ve genel referans amaçlıdır</b>. 
                Bu hesaplamaların hiçbirisi resmi, yasal veya profesyonel mali/hukuki danışmanlık niteliği taşımamaktadır.
            </p>
            <p style="color: #d1d5db; font-size: 13px; line-height: 1.7; margin-bottom: 15px; text-align: justify;">
                <b>2. YÜKÜMLÜLÜK VE DENETİM SORUMLULUĞU KULLANICI ŞİRKETE AİTTİR:</b><br>
                Yazılımın doğruluğunun teyit edilmesi, olası sistemsel veya mantıksal hataların (veri kaybı, hesaplama farklılıkları vb.) kontrolü ve finansal kararların alınmasından kaynaklanan 
                <b>tüm idari, mali, operasyonel ve hukuki sorumluluk tamamen sistemi kullanan şirket ve/veya kişilere aittir</b>. 
                Bu platformda yer alan herhangi bir bilginin veya raporun resmi kurumlarla (vergi daireleri, bankalar vb.) paylaşılmasından doğan yasal yükümlülükler tamamen kullanıcıya aittir.
            </p>
            <p style="color: #d1d5db; font-size: 13px; line-height: 1.7; margin-bottom: 15px; text-align: justify;">
                <b>3. LİSANS VE SORUMLULUK SINIRLANDIRILMASI (MIT LICENSE CLAUSE):</b><br>
                İşbu yazılım, MIT Lisansı altında, <b>"OLDUĞU GİBİ" (AS IS)</b> sunulmakta olup; ticari elverişlilik, belirli bir amaca uygunluk 
                veya ihlal durumlarının bulunmamasına ilişkin garantiler de dahil olmak üzere, doğrudan veya dolaylı olarak 
                <b>hiçbir garanti verilmemektedir</b>. Yazarlar veya telif hakkı sahipleri; yazılımla, yazılımın kullanımıyla veya 
                yazılımla yapılan diğer işlemlerle ilgili olarak ortaya çıkan hiçbir sözleşme davası, haksız fiil davası veya diğer taleplerden, 
                hasarlardan veya diğer yükümlülüklerden <b>hukuken sorumlu tutulamaz</b>.
            </p>
            <p style="color: #d1d5db; font-size: 13px; line-height: 1.7; margin-bottom: 0; text-align: justify;">
                <b>4. ANLAŞMA KABULÜ:</b><br>
                Sisteme giriş yapan, kayıt olan veya Command Center modüllerini aktif olarak kullanan her kişi ve şirket, 
                yukarıda belirtilen şartları, yasal sınırlandırmaları ve sorumluluk reddi beyanını <b>kayıtsız şartsız kabul etmiş sayılır</b>.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.info("ℹ️ DeDev Command Center V2.0, ticari kararlar almadan önce harici bağımsız mali müşavirler ve lisanslı finans denetçileri ile çalışmanızı önemle tavsiye eder.")
