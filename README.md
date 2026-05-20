# 🚀 DeDev AI Project Command Center (V2.8)

<p align="center">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Google%20Sheets-34A853?style=for-the-badge&logo=google-sheets&logoColor=white" alt="Google Sheets">
  <img src="https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white" alt="Plotly">
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS Custom">
  <img src="https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge" alt="License">
</p>

**DeDev AI Project Command Center**, solo yazılım geliştiricileri ve yapay zeka mühendisleri için özel olarak tasarlanmış, **premium dark-glassmorphism** arayüzüne sahip, modüler, tam kapsamlı ve yüksek güvenlikli bir proje yönetim komuta merkezidir. 

Proje, yerel kararlılık sunan `data.json` veritabanı ile **Google Sheets Bulut Senkronizasyonunu** asenkron multi-threading altyapısıyla birleştirerek, ücretsiz sunucularda bile sıfır veri kaybı ve sıfır arayüz gecikmesi (lag) ile çalışır.

---

## 💎 Tasarım Felsefesi & Arayüz Deneyimi

Uygulamanın görsel tasarımı sıradan tablolardan veya basit formlardan tamamen farklıdır. **Modern Web Standartları (Premium UX)** göz önünde bulundurularak sıfırdan geliştirilen CSS yapısı şu özellikleri içerir:
* **Glassmorphism Arayüzü:** Yarı saydam arka planlar, ince degrade kenarlıklar (borders), bulanıklık (backdrop-filter) efektleri ve yumuşak gölgelerle derinlik hissi yaratılmıştır.
* **Canlı Renk Paleti:** Koyu mod (dark mode) üzerinde parlayan neon mavi, zümrüt yeşili, canlı turuncu ve derin mor renk tonları ile kullanıcıyı yormayan profesyonel bir kontrast sağlanmıştır.
* **Mikro-Animasyonlar:** Fare ile üzerine gelindiğinde (hover) yumuşak bir şekilde büyüyen kartlar, pürüzsüz geçişler ve etkileşimli bileşenler.
* **Tam Responsive Düzen:** Büyük ekran monitörlerden tablet ve mobil cihazlara kadar mükemmel uyum sağlayan esnek grid yapıları.

---

## 🧭 Kapsamlı Modül Rehberi (Uygulama Neler Sunuyor?)

DeDev Command Center, bir projenin fikirden üretime (production) kadar olan tüm süreçlerini tek noktadan yönetebilmeniz için 12 adet birbiriyle entegre modül sunar:

### 📊 1. Ana Komuta Merkezi (Dashboard)
* **Dinamik Metrik Kartları:** Toplam proje sayısı, aktif görevler, tamamlanan işler ve genel bitirilme oranlarını yansıtan görsel kartlar.
* **Aktivite Akışı (Activity Feed):** Sistemde yapılan son ekleme, silme, güncelleme ve bulut senkronizasyonu işlemlerini şık zaman damgaları ve durum emojileriyle kronolojik olarak gösteren canlı günlük.
* **Hızlı Durum Analizleri:** Devam eden ve bekleyen projelerin hızlı listesi.

### 🔒 2. Gizli Kasa (Secret Vault)
Hassas ticari projelerinizi veya gizli fikirlerinizi üçüncü gözlerden tamamen korumak amacıyla tasarlanmış kripto odası:
* **XOR & SHA-256 Şifreleme:** Kasa içerisine eklenen veya kasaya gönderilen projelerin açıklamaları ve teknolojileri, veritabanına doğrudan kaydedilmez. Belirlediğiniz güçlü bir parola ile anında şifrelenir.
* **Çift Aşamalı Güvenlik:** Kasa kilitlendiğinde, gizli projeler tüm arayüzlerde, grafiklerde ve hatta Google Sheets yedeklerinde `🔒 [ŞİFRELİ - GİZLİ KASA]` olarak maskelenir. Parola doğru girilmeden verilerin ham hali asla belleğe yüklenmez.
* **Tek Tıkla Genelleştirme:** Kasa şifresi çözüldüğünde, projeleri tekrar genel listeye geri gönderme desteği sunar.

### 📋 3. Dinamik Kanban Panosu
* **Sürükle-Seç Görev Yönetimi:** Görevleri durumlarına göre (`Yapılacaklar`, `Geliştiriliyor`, `Tamamlandı`) ayıran, görev detaylarını ve öncelik derecelerini (Düşük, Orta, Yüksek) kart halinde gösteren premium pano.
* **Kasa Koruma Kilidi:** Gizli projelere ait görevlerin başlıkları ve açıklamaları, kasa kilidi açılmadığı sürece Kanban panosunda `🔒 ***************` şeklinde maskelenir ve taşınamaz.

### 📅 4. İnteraktif Zaman Tüneli (Timeline)
* **Plotly Gantt Grafiği:** Projelerin başlangıç ve bitiş tarihlerini, ilerleme oranlarını ve öncelik renklerini interaktif bir Gantt şeması üzerinde canlı olarak çizer.
* **Milestone (Kilometre Taşları):** Projelerin altındaki kritik teslim tarihlerini ve aşamaları zaman çizelgesi üzerinde konumlandırır.

### ⏱️ 5. Zaman Takip Modülü (Time Tracking)
* Geliştirme süreçlerinde hangi projeye ne kadar süre harcandığını takip etmenizi sağlayan entegre kronometre altyapısı.
* Proje bazlı toplam çalışılan saat analizleri ve tarih aralıklarına göre filtrelenebilir zaman kayıt tablosu.

### 💰 6. Finans Yönetimi (Finances)
* Proje bütçelerini, harcanan miktarları ve saatlik geliştirici ücretlerini yöneten finansal takip paneli.
* Bütçe aşımı durumunda kırmızıya dönen akıllı bütçe tüketim göstergeleri.

### 👥 7. Ekip ve Rol Yönetimi (Team Panel)
* Projede yer alan yazılımcıların, tasarımcıların ve yöneticilerin iletişim bilgilerini, uzmanlık alanlarını ve rollerini yöneten modül.
* Ekip üyelerinin aktif iş yükü oranlarının otomatik hesaplanması.

### 📈 8. Gelişmiş Performans Raporları
* **stacked Bar Chart Analizleri:** Her bir ekip üyesinin üstlendiği görevleri durumlarına göre üst üste biriken grafiklerle gösteren gelişmiş performans şemaları.
* **İş Yükü Dağılımı:** Ekip üyeleri ve projeler arasındaki görev yükünü pasta grafikleriyle görselleştirir.
* **Akıllı Kasa Entegrasyonu:** Raporlar sayfasındaki şifre çözme paneli ile, kasa şifresi çözüldüğü anda gizli projelerin verileri de grafiklere gerçek zamanlı olarak yansır.

### 🛠️ 9. Teknoloji Portföyü (Tech Stack)
* Projelerde kullanılan kütüphane, framework ve altyapıların (Örn: Python, React, TensorFlow, PostgreSQL) versiyonları ve kullanım amaçlarıyla listelendiği teknik envanter.

### 📑 10. İnteraktif Not Defteri (Developer Notes)
* Proje fikirlerinizi, kod bloklarınızı veya anlık yapılacak iş notlarınızı markdown desteğiyle zenginleştirilmiş metin kutularında saklamanızı sağlayan hızlı not paneli.

### 🔌 11. Geliştirici API Dokümantasyonu (Developer API & Docs)
* Sistemdeki verileri harici sistemlere aktarmak veya üçüncü parti otomasyon araçlarına bağlamak isteyen geliştiriciler için hazırlanmış **etkileşimli API şeması**.
* Proje ve Görev modellerinin JSON çıktı yapılarını, alan açıklamalarını ve tiplerini şık JSON blokları halinde sunar.

### ☁️ 12. Google Sheets Cloud Sync (Asenkron Bulut Entegrasyonu)
* **Sıfır Gecikme (Multi-Threading):** Uygulamada bir kayıt oluşturulduğunda sistem önce yerel `data.json` dosyasına anında yazarak arayüzün kilitlenmesini engeller. Ardından asenkron bir arka plan thread'i başlatarak verileri Google Sheets'e yükler. Arayüzde en ufak bir takılma hissetmezsiniz.
* **Okunabilir Görünümler:** Google E-Tablo dosyasını açtığınızda verilerinizi rahatça görebilmeniz için **`Projeler`** ve **`Görevler`** sekmeleri otomatik olarak insan tarafından okunabilir flat tablo biçiminde oluşturulur.
* **Otomatik Veri Kurtarma (Cloud Restore):** Streamlit Cloud sunucuları yeniden başlatıldığında yerel `data.json` dosyanız silinse bile, uygulama ilk açılışta Google Sheets yedeğini tespit eder ve sistem verilerini otomatik olarak geri yükler.

---

## 🏗️ Yazılım Mimarisi & Klasör Yapısı

Uygulama, kod okunabilirliğini ve genişletilebilirliği en üst düzeyde tutmak amacıyla **MVVM tabanlı modüler bir yapıya** sahiptir:

```text
DeDev-Project-Manager/
│
├── app.py                      # Ana uygulama giriş noktası, Sidebar ve sayfa yönlendirici
├── data.json                   # Yüksek performanslı yerel NoSQL veritabanı dosyası
├── requirements.txt            # Python kütüphane bağımlılık listesi
├── .gitignore                  # GitHub'a gönderilmeyecek özel dosyaları koruyan filtre
│
├── utils/                      # Yardımcı İşlevler ve Veri Katmanı
│   ├── data_handler.py         # Yerel veri okuma/yazma ve threading tetikleyicisi
│   ├── encryption.py           # Kasa için XOR şifreleme ve SHA-256 doğrulama algoritmaları
│   └── gsheets_handler.py      # Google Sheets API bağlantısı, flat tablo yazıcı ve yedekleyici
│
└── views/                      # Kullanıcı Arayüzü (Sayfa Görünümleri)
    ├── dashboard.py            # Ana Panel arayüzü ve Aktivite Akışı
    ├── projects_view.py        # Proje ekleme, düzenleme, silme ve detay görünümleri
    ├── kanban_view.py          # Görev yönetimi ve Kanban panosu
    ├── timeline.py             # Plotly Gantt zaman çizelgesi şeması
    ├── time_tracking.py        # Geliştirici kronometresi ve zaman kayıt paneli
    ├── finance_view.py         # Bütçe, gider ve finans takip ekranı
    ├── team_view.py            # Ekip üyeleri, iletişim ve rol yönetimi
    ├── secret_vault.py         # Kasa arayüzü, şifreleme ve kilit açma mekanizması
    ├── reports.py              # Stacked bar ve pasta grafiklerinden oluşan analiz paneli
    ├── techstack.py            # Teknolojik envanter ve kütüphane takip arayüzü
    ├── notes.py                # Markdown destekli not defteri
    └── api_docs.py             # JSON şemalı interaktif API rehberi
```

---

**👨‍💻 Geliştirici:** Deniz Deviren (Solo Full-Stack Developer & AI Engineer)  
**© 2026 DeDev - Tüm Hakları Saklıdır. Yazılımcılar tarafından yazılımcılar için tasarlandı.**
