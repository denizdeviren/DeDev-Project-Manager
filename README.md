# 🚀 DeDev AI Project Command Center (V3.0 - Premium Enterprise Edition)

<p align="center">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Google%20Sheets-34A853?style=for-the-badge&logo=google-sheets&logoColor=white" alt="Google Sheets">
  <img src="https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white" alt="Plotly">
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS Custom">
  <img src="https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge" alt="License">
</p>

**DeDev AI Project Command Center**, solo yazılım geliştiricileri, ürün yöneticileri, yapay zeka mühendisleri ve teknoloji şirketleri için tasarlanmış, **premium dark-glassmorphism** arayüzüne sahip, çoklu kiracı (multi-tenant) destekli, yüksek güvenlikli ve MIT Lisanslı kurumsal düzeyde bir **ERP, Finansal Yönetim ve Proje Komuta Merkezidir**.

Bu sistem; yerel NoSQL dosya tabanlı kararlılık sunan izole **`data_user_<username>.json`** yapısı ile asenkron multi-threading **Google Sheets Bulut Senkronizasyonunu** birleştirerek, ücretsiz sunucularda bile sıfır veri kaybı, tam kullanıcı izolasyonu ve sıfır arayüz gecikmesi (zero-lag) ile çalışır.

---

## 💎 Tasarım Felsefesi & Arayüz Deneyimi

Uygulamanın görsel tasarımı sıradan tablolardan veya basit formlardan tamamen farklıdır. **Modern Web Standartları (Premium UX)** ve en son trendler göz önünde bulundurularak sıfırdan geliştirilen CSS yapısı şu benzersiz özellikleri sunar:
* **Glassmorphism & Cam Efekti:** Yarı saydam arka planlar, ince degrade kenarlıklar (borders), bulanıklık (backdrop-filter) efektleri ve derinlik hissi veren yumuşak gölgelerle premium bir atmosfer.
* **Modern Tipografi ve Renk Harmonisi:** Koyu mod (dark mode) üzerinde parlayan neon mavi, zümrüt yeşili, turkuaz ve derin mor degrade renk tonları ile gözü yormayan yüksek kontrastlı arayüz.
* **Mikro-Animasyonlar ve Hover Efektleri:** Fare ile üzerine gelindiğinde yumuşak bir şekilde büyüyen kartlar (scale-up), pürüzsüz kaydırmalar (smooth-scroll) ve etkileşimli geçişler.
* **Tam Sayfa Yenileme Koruması (Session & Page Persistence):** Streamlit'in yenileme anında oturumu kapatma ve sayfayı sıfırlama davranışı, tarayıcı URL query parametrelerine (`?user=<username>&page=<page>`) yapılan çift taraflı senkronizasyon ile engellenmiştir. Sayfa yenilense dahi kullanıcı oturumu açık kalır ve en son kaldığı sayfada kesintisiz çalışmaya devam eder.
* **Global Ctrl+S & 10 Saniye Otomatik Kaydetme Altyapısı:**
  * **Ctrl+S / Cmd+S Kısayolu:** Kullanıcı herhangi bir veri girişi yaparken `Ctrl+S` (Mac için `Cmd+S`) tuş kombinasyonuna bastığı anda, Javascript tetikleyicisi formu otomatik olarak kaydeder ve ekranda yeşil renkli, şık bir *"💾 DeDev Veritabanı ve Bulut Senkronizasyonu Kaydedildi!"* uyarısı gösterir.
  * **10 Saniyelik Akıllı Otomatik Kayıt (Autosave):** Kullanıcı formu göndermeyi unutsa dahi, her 10 saniyede bir çalışan arka plan motoru açık olan formu otomatik olarak kaydeder ve ekranın sağ altında zarafetle yanıp sönen bir *"🟢 Otomatik Kaydedildi (Autosaved)"* bildirimi görüntüler.

---

## 🧭 Kapsamlı Modül Rehberi (18+ Kurumsal Modül)

DeDev Command Center, şirket süreçlerinizi ve projelerinizi tek noktadan denetleyebilmeniz için tamamen birbiriyle entegre **18 modül** sunar:

### 🏠 1. Ana Komuta Merkezi (Dashboard)
* **Dinamik Yönetici Metrikleri:** Toplam proje sayısı, aktif/tamamlanan görevler ve genel iş tamamlama oranlarını yansıtan görsel kartlar.
* **Aktivite Akışı (Activity Feed):** Sistemde yapılan tüm ekleme, silme, güncelleme ve bulut senkronizasyonu işlemlerini şık zaman damgalarıyla kronolojik olarak listeleyen canlı günlük.

### 📁 2. Projeler Command Center
* **Gelişmiş Proje Kartları:** Proje adı, kategorisi, açıklaması ve teknoloji envanteri.
* **💰 Proje Sözleşme Bedeli (Project Fee):** Banka yevmiye hareketlerinden bağımsız olarak, her projenin kartı üzerinde yeşil renkli ve formatlı (`150,000.00 TRY`) olarak anlık gösterilen kurumsal sözleşme tutarı. Proje oluştururken veya düzenlerken doğrudan bütçe kontrolü sağlar.
* **Zaman Çizelgesi ve İlerleme Barı:** Projenin başlangıç/bitiş tarihleri ile tamamlanma yüzdesini gösteren dinamik ilerleme çubukları.

### 🔒 3. Gizli Kasa (Secret Vault)
* **XOR & SHA-256 Şifreleme:** Kasa içerisine eklenen projelerin açıklamaları ve teknolojileri, veritabanına doğrudan kaydedilmez. Belirlediğiniz parola ile anında şifrelenir.
* **Çift Aşamalı Güvenlik:** Kasa kilitlendiğinde, gizli projeler tüm arayüzlerde, grafiklerde ve hatta Google Sheets yedeklerinde `🔒 [ŞİFRELİ - GİZLİ KASA]` olarak maskelenir. Parola doğru girilmeden verilerin ham hali asla belleğe yüklenmez.

### 📋 4. Kanban Görev Yönetimi (Kanban Board)
* **Sürükle-Seç İş Akışı:** Görevleri durumlarına göre (`To Do`, `In Progress`, `Done`) ayıran, görev detaylarını ve öncelik derecelerini kart halinde gösteren premium pano.
* **Hata Korumalı İstatistik Güncelleyici (KeyError-Safe):** Görev eklerken veya taşırken projelere ait istatistik sayaçlarının olmamasından kaynaklanan tüm hatalar `get()` korumalı algoritma ile tamamen engellenmiştir.

### 📅 5. İnteraktif Gantt Şeması ve Zaman Tüneli (Timeline)
* **Sorumlu Geliştirici Görselleştirmesi:** Gantt şeması üzerinde her görevin yanında doğrudan kimin sorumlu olduğunu gösteren `👤 {Atanan Kişi}` etiket entegrasyonu.
* **Zengin Hover Detayları (Tooltips):** Zaman çizgisi üzerindeki çubukların üzerine gelindiğinde; Proje Adı, Kategori, Atanan Kişi, Görev Durumu, Öncelik Derecesi, İş Gücü Efor Skoru ve Detaylı Açıklama gibi tüm parametreleri pürüzsüzce sunar.

### ⏱️ 6. Geliştirici Zaman Takip Modülü (Time Tracking)
* Geliştirme süreçlerinde hangi projeye ne kadar süre harcandığını takip etmenizi sağlayan entegre kronometre altyapısı.
* Proje bazlı toplam çalışılan saat analizleri ve filtrelenebilir zaman kayıt tablosu.

### 💰 7. Finans & Çift Taraflı Muhasebe Süiti (Double-Entry Ledger)
* **Kasa & Banka Hesapları:** Nakit Kasa ve banka hesap bakiyelerini gerçek zamanlı takip eder, hesaplar arası para transferi (Virman) ve tahsilat/ödeme işlemlerini yönetir.
* **Değiştirilemez Defter-i Kebir (Immutable Ledger):** Muhasebe kayıtları yasal denetim için silinemez veya değiştirilemez. Hatalı işlemler için otomatik ters kayıt üreten "Düzeltme Fişi" mekanizması mevcuttur.
* **Mali Raporlar:** Çift taraflı muhasebe ilkelerine uygun olarak anlık dengelenen **Mizan (Trial Balance)**, **Gelir Tablosu (Income Statement)** ve **Bilanço (Balance Sheet)** mali raporlarını otomatik üretir.

### 👥 8. Ekip Yönetimi & Tek Adımda Yetkilendirme (Team Panel)
* **Hızlı Ekip Ekleme & Giriş Yetkisi:** Yönetici yeni bir ekip üyesi eklerken, aynı form içerisinden tek adımda çalışanına kullanıcı adı ve şifre belirleyebilir.
* **Rol Tabanlı Erişim Kontrolü (RBAC):** Ekip üyeleri (member) sisteme giriş yaptıklarında yalnızca yöneticinin kendilerine izin verdiği sayfaları görüntüleyebilirler. Admin Paneli, Bütçe gibi idari sayfalar sidebar'dan tamamen gizlenir.

### 📈 9. Gelişmiş Performans Raporları
* **Stacked Bar Chart Analizleri:** Her bir ekip üyesinin üstlendiği görevleri durumlarına göre üst üste biriken grafiklerle gösteren gelişmiş performans şemaları.
* **İş Yükü Dağılımı:** Ekip üyeleri ve projeler arasındaki görev yükünü pasta grafikleriyle görselleştirir.

### 🛠️ 10. Teknoloji Portföyü (Tech Stack)
* Projelerde kullanılan kütüphane, framework ve altyapıların (versiyonları ve kullanım amaçlarıyla listelendiği teknik envanter.

### 📑 11. İnteraktif Not Defteri (Developer Notes)
* Proje fikirlerinizi, kod bloklarınızı markdown desteğiyle zenginleştirilmiş hızlı not paneli.

### 🔌 12. Geliştirici API Dokümantasyonu (Developer API & Docs)
* Sistemdeki verileri harici sistemlere aktarmak veya üçüncü parti otomasyon araçlarına bağlamak isteyen geliştiriciler için hazırlanmış **etkileşimli API şeması**.

### ☁️ 13. Google Sheets Cloud Sync (Çoklu Kiracı Uyumlu Yedekleme)
* **İzole Sekmelendirme (No-Collision):** Birden fazla kullanıcının aynı Google Sheets Spreadsheet URL'si üzerinden yaptığı yedeklemelerin birbirinin verisini ezmesi engellenmiştir. 
* **Aktif Kullanıcı Suffix Koruması:** Tüm yedekleme sekmeleri arka planda otomatik olarak aktif kullanıcı adıyla suffikslenir (örn: `Projeler_1denizdeviren` veya `__json_db_demo_erpsim__`). Böylece her kiracının bulut yedekleri aynı dosyada tamamen izole sekmelerde saklanır.

### 🏛️ 14. Çoklu Profil & Yönetim (Admin View)
* **Yönetici Kimlik Maskeleme:** Güvenlik gereği orijinal yönetici giriş bilgileri ve verileri gizlenerek tamamen izole edilmiştir.
* **Simülasyon Modu Kontrolü:** Tanıtım ve canlı deneyim süreçleri için özel olarak oluşturulmuş örnek yönetici hesabı (`demo_erpsim` / `demo123`) alt yapısı.

### 🧾 15. Sekmeli Fatura & Gelir Entegrasyonu (Billing & Invoicing)
* **Profesyonel Fatura Kesme:** Proje bazlı fatura oluşturma, fatura numarası (INV-YYYY-XXXX), KDV oranları, vergi dairesi bilgileri ve alıcı/satıcı detayları ile resmi faturalandırma modülü.
* **Fatura Durum ROI Entegrasyonu:** Faturanın durumu **"Ödendi"** yapıldığında, fatura tutarı anında ilgili projenin **Gelir (Income)** bütçesine aktarılır.

### 📂 16. ERP Arşiv Odası & PDF Görüntüleyici (Archive Room)
* **Dijital Belge Arşivi:** Şirket sözleşmeleri, faturalar, resmi yazışmalar ve PDF formatındaki belgelerin güvenli bir şekilde sunucuya yüklenmesi ve saklanması.
* **Tarayıcı İçi PDF Görüntüleyici:** Streamlit entegrasyonlu PDF okuyucu ile belgeleri indirmeden doğrudan tarayıcı ekranından okuyup inceleme desteği.

### 📊 17. DeDev Findeks Skoru & ERP Portföy Analizi (Findeks Score)
* **Findeks Kredi Notu Entegrasyonu:** Şirketinizin ve projelerinizin finansal performansını, bütçe uyumluluğunu ve zamanında teslimat oranlarını analiz ederek dinamik bir Findeks Kredi Skoru (350 - 1900 puan arası) hesaplayan dairesel gösterge (Gauge Chart).
* **Resmi Raporlama:** Resmi kurumsal raporu tek tıkla MIT Lisanslı ve kurumsal antetli kağıt düzeninde **baskıya hazır HTML/PDF** formatında indirme imkanı.

### 📅 18. İnteraktif Proje Takvimi (Calendar View)
* Proje teslim tarihlerini ve görevlerin termin sürelerini aylık, haftalık veya günlük şık bir takvim görünümü üzerinde organize eden entegre planlama paneli.

---

## 🔒 Güvenlik ve Şifreleme Standartları

DeDev AI Project Command Center, kurumsal düzeyde veri güvenliğini sağlamak için iki aşamalı bir kripto altyapısı kullanır:

1. **PBKDF2-SHA256 Parola Hashing (Kullanıcı Güvenliği):**
   * Kullanıcı parolaları veritabanında asla düz metin (plain text) olarak tutulmaz.
   * Her kullanıcı için özel 16-byte rastgele tuz (salt) üretilir.
   * Parolalar, **100.000 iterasyonlu** `PBKDF2-HMAC-SHA256` kriptografik türetme fonksiyonu kullanılarak hashlenir. Bu sayede Rainbow Table ve Brute Force (kaba kuvvet) saldırılarına karşı tam koruma sağlanır.
   
2. **Projeler İçin Güvenli XOR & SHA-256 Şifreleme (Secret Vault):**
   * Gizli projelerin hassas verileri, SHA-256 ile türetilen simetrik bir anahtar kullanılarak XOR tabanlı şifrelemeyle veritabanına yazılır. Parola girilmeden bellek düzeyinde dahi çözülemez.

---

## ⚖️ Yasal Sorumluluk Reddi (Disclaimer)

> [!IMPORTANT]
> **KULLANICI VE ŞİRKETLER İÇİN ÇOK ÖNEMLİ YASAL BİLDİRİM:**
> 
> 1. **Sadece Simülasyon ve Bilgi Amaçlıdır:** DeDev Command Center uygulaması içerisinde hesaplanan tüm metrikler, Findeks kredi puanları, finansal analizler, yevmiye kayıtları, mizan, gelir tablosu, KDV oranları ve bilanço dengeleri **tamamen simülasyon, eğitim ve genel referans amaçlıdır**. Bu hesaplamaların hiçbirisi resmi, yasal veya profesyonel mali/hukuki/vergi danışmanlığı niteliği taşımamaktadır.
> 
> 2. **Hata Denetim ve Kontrol Sorumluluğu Kullanıcıya Aittir:** Yazılımın doğruluğunun teyit edilmesi, olası sistemsel, matematiksel veya mantıksal hataların (veri kayıpları, hesaplama farklılıkları, yuvarlama hataları vb.) kontrolü ve finansal kararların alınmasından kaynaklanan **tüm idari, mali, operasyonel ve hukuki sorumluluk tamamen sistemi kullanan şirket ve/veya kişilere aittir**. Geliştiricilerin bu konuda hiçbir kontrol yükümlülüğü bulunmamaktadır.
> 
> 3. **Garanti Yoksunluğu (As Is Clause):** Bu yazılım, MIT Lisansı altında, **"OLDUĞU GİBİ" (AS IS)** sunulmakta olup; ticari elverişlilik, belirli bir amaca uygunluk veya ihlal durumlarının bulunmamasına ilişkin garantiler de dahil olmak üzere, doğrudan veya dolaylı olarak **hiçbir garanti verilmemektedir**.
> 
> 4. **Tazminat ve Yükümlülük Sınırı:** Yazarlar veya telif hakkı sahipleri; yazılımla, yazılımın kullanımıyla veya yazılımla yapılan diğer işlemlerle ilgili olarak ortaya çıkan hiçbir sözleşme davası, haksız fiil davası veya diğer taleplerden, hasarlardan veya diğer yükümlülüklerden (kâr kaybı, iş kesintisi, resmi cezalar veya veri kayıpları dahil) **hukuken sorumlu tutulamaz**. 
> 
> **Sisteme giriş yapan, kayıt olan veya modülleri aktif olarak kullanan her kişi ve kurum, yukarıda belirtilen şartları ve yasal sorumluluk sınırlarını kayıtsız şartsız kabul etmiş sayılır.**

---

## 🏗️ Klasör Yapısı & MVVM Mimarisi

Uygulama, kod okunabilirliğini ve genişletilebilirliği en üst düzeyde tutmak amacıyla **MVVM tabanlı modüler bir yapıya** sahiptir:

```text
DeDev-Project-Manager/
│
├── app.py                      # Ana uygulama giriş noktası, Sidebar ve sayfa yönlendirici
├── requirements.txt            # Python kütüphane bağımlılık listesi
├── .gitignore                  # Git filtre dosyası
├── LICENSE                     # MIT Resmi Lisans Belgesi
├── README.md                   # Premium Enterprise Dokümantasyonu
│
├── utils/                      # Yardımcı İşlevler ve Veri Katmanı
│   ├── data_handler.py         # Yerel veri okuma/yazma, PBKDF2 hashleme ve defaults
│   ├── encryption.py           # PBKDF2, XOR şifreleme ve SHA-256 doğrulama algoritmaları
│   └── gsheets_handler.py      # Google Sheets API bağlantısı, flat tablo yazıcı ve yedekleyici
│
└── views/                      # Kullanıcı Arayüzü (Sayfa Görünümleri)
    ├── dashboard.py            # Ana Panel arayüzü ve Aktivite Akışı
    ├── projects_view.py        # Proje yönetimi, düzenleme, silme ve bütçe/bedel alanı
    ├── kanban_view.py          # Görev yönetimi ve hata korumalı Kanban panosu
    ├── timeline.py             # Plotly Gantt zaman çizelgesi şeması ve hover geliştirmeleri
    ├── time_tracking.py        # Geliştirici kronometresi ve zaman kayıt paneli
    ├── finance_view.py         # Bütçe, fatura kesme, gider ve sekmeli finans takip ekranı
    ├── team_view.py            # Ekip üyeleri, iletişim, rol ve tek adımda giriş yetkisi formları
    ├── secret_vault.py         # Kasa arayüzü, şifreleme ve kilit açma mekanizması
    ├── reports.py              # Stacked bar ve pasta grafiklerinden oluşan analiz paneli
    ├── techstack.py            # Teknolojik envanter ve kütüphane takip arayüzü
    ├── notes.py                # Markdown destekli not defteri
    ├── admin_view.py           # Yönetici kontrolleri, simülasyon hesap kılavuzu ve profil seçici
    ├── archive_view.py         # Dijital arşiv odası ve tarayıcı içi PDF okuyucu
    ├── calendar_view.py        # Teslim tarihleri interaktif takvim paneli
    ├── deployments.py          # Canlı sunucu ve DevOps dağıtım takip arayüzü
    ├── portfolio_rating.py     # Findeks kredi skoru göstergesi ve MIT lisanslı resmi rapor indirici
    ├── about_view.py           # Hakkında, metodoloji açıklamaları ve Yasal Disclaimer sayfası
    └── task_details.py         # Görev detayları ve düzenleme modal görünümü
```

---

**👨‍💻 Geliştirici:** Deniz Deviren (Solo Full-Stack Developer & AI Engineer)  
**© 2026 DeDev - Tüm Hakları Saklıdır. Yazılımcılar tarafından yazılımcılar için tasarlandı.**
