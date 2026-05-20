# 🚀 DeDev AI Project Command Center (V2.8)

<p align="center">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Google%20Sheets-34A853?style=for-the-badge&logo=google-sheets&logoColor=white" alt="Google Sheets">
  <img src="https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white" alt="Plotly">
</p>

**DeDev AI Project Command Center**, solo yazılım geliştiricileri ve yapay zeka mühendisleri için özel olarak tasarlanmış, **premium dark-glassmorphism** arayüzüne sahip, modüler ve yüksek güvenlikli bir proje yönetim merkezidir. Yerel veritabanı (`data.json`) ile **Google Sheets Bulut Senkronizasyonunu** asenkron multi-threading ile birleştirerek veri kayıplarını tamamen engeller.

---

## 💎 Temel Özellikler & Modüller

### 📊 1. Komuta Merkezi (Dashboard)
* Proje durumları, aktif geliştirme ilerlemeleri ve tamamlanma oranlarına kuşbakışı genel bakış.
* Son etkinlikleri şık emojiler ve renk kodlarıyla gösteren interaktif aktivite akışı.
* Proje türlerine göre otomatik filtrelenen dinamik metrik kartları.

### 🔒 2. Gizli Kasa (Secret Vault)
* Hassas projelerin açıklamalarını ve teknolojilerini güçlü **XOR / SHA-256 kriptolama** yöntemiyle veri tabanında şifreli olarak saklar.
* İki aşamalı şifre doğrulama ve anında şifre çözme sistemi.
* Kasa içinde deşifre edilen projeleri tek tıkla genel listeye geri gönderebilme (Genelleştirme) desteği.

### 📋 3. Dinamik Kanban Panosu
* Sürükle-bırak hissiyatı sunan premium görev yönetim sütunları (To Do, In Progress, Done).
* **Güvenlik Koruyucu Maskeleme:** Kasa şifresi girilmedikçe gizli görevlerin başlıkları sabit uzunlukta `🔒 ***************` şeklinde maskelenir ve görev taşıma paneli devre dışı bırakılır.

### 📅 4. İnteraktif Zaman Tüneli (Timeline)
* Projelerin başlangıç ve bitiş tarihlerini Plotly Gantt şemasıyla canlı olarak çizer.
* Milestone (kilometre taşları) entegrasyonu ile projelerinizin kritik adımlarını görsel olarak takip etmenizi sağlar.

### 📈 5. Performans Raporları & Analizler
* Projelerinizin ilerleme grafiklerinin yanı sıra solo geliştiriciler veya ekipler için özel iş yükü pastası.
* **YENİ:** Her ekip üyesinin görev aşamalarını üst üste biriktirerek gösteren **📊 Ekip Görev Tamamlama ve Durum Analizi** (Stacked Bar Chart) grafiği.
* Raporlar sayfasında dinamik şifre çözme kutusuyla gizli projelerin grafiklere anında dahil edilmesi.

### ☁️ 6. Google Sheets Bulut Senkronizasyonu (Cloud Sync)
* **Sıfır Gecikme (Multi-Threading):** Kaydet butonuna bastığınızda uygulama donmaz; veri yerel diske yazıldıktan sonra arka planda bir daemon thread ile Google Sheets'e asenkron olarak yedeklenir.
* **NoSQL Tarzı Depolama:** Veritabanının hiyerarşik ve iç içe geçmiş yapısı bozulmadan `__json_db__` sekmesinde güvenle saklanır.
* **Okunabilir Görünümler:** E-Tablo içinde otomatik olarak **`Projeler`** ve **`Görevler`** sekmeleri oluşturulur ve gözle okunabilir tablolara dönüştürülür.
* **Otomatik Bulut Kurtarma (Cloud Restore):** Streamlit Cloud gibi geçici depolama sunan platformlarda, uygulama sıfırdan başladığında doğrudan son bulut yedeğini çekerek sistemi otomatik kurar.

---

## 🛠️ Kurulum & Yerel Çalıştırma

Aşağıdaki adımları takip ederek projeyi yerel bilgisayarınızda anında çalıştırabilirsiniz:

```bash
# 1. Depoyu klonlayın
git clone <sizin-github-repo-urlniz>
cd DeDev-Project-Manager

# 2. Python Sanal Ortamı oluşturun ve aktifleştirin
python -m venv venv
# Windows için:
.\venv\Scripts\activate
# Linux/Mac için:
source venv/bin/activate

# 3. Bağımlılıkları yükleyin
pip install -r requirements.txt
pip install gspread oauth2client toml

# 4. Uygulamayı başlatın
streamlit run app.py
```

---

## 🔒 Güvenlik & secrets.toml Yapılandırması

Uygulamanın Google Sheets senkronizasyonunu aktifleştirmek için `.streamlit/secrets.toml` dosyası oluşturulmalıdır. Bu dosya `.gitignore` içinde tanımlı olduğu için GitHub'a push yaparken **asla sızdırılmaz**.

`.streamlit/secrets.toml` içeriği şu formatta olmalıdır:

```toml
[connections.gsheets]
spreadsheet = "https://docs.google.com/spreadsheets/d/ETABLO_URL_VEYA_ID"
type = "service_account"
project_id = "your-gcp-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\nyour-long-multiline-private-key-with-escaped-newlines\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/your-cert-url"
universe_domain = "googleapis.com"
```

---

## 🌐 Streamlit Cloud'a Dağıtım (Deployment)

1. Deponuzu GitHub'a push edin.
2. [Streamlit Share](https://share.streamlit.io/) sitesine giriş yapıp GitHub hesabınızı bağlayın.
3. Deponuzu, dalınızı (branch) ve **`app.py`** dosyasını seçin.
4. Sol alttaki **Advanced Settings** butonuna tıklayın.
5. **Secrets** kutusuna yerel `.streamlit/secrets.toml` dosyanızın içeriğini aynen kopyalayıp yapıştırın.
6. **Deploy** butonuna tıklayın! Uygulamanız birkaç dakika içinde canlıda! 🚀

---

**👨‍💻 Geliştirici:** Deniz Deviren (Solo Full-Stack Developer & AI Engineer)  
**© 2026 DeDev - Tüm Hakları Saklıdır.**
