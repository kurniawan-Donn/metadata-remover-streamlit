# 🛡️ Metadata Remover

**✨ Bersihkan Jejak Digital Anda dengan Satu Klik! 🥷**

[![Live Demo](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://metadata-remover-app-dk.streamlit.app)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)

🔗 **Live Demo:** [metadata-remover-app-dk.streamlit.app](https://metadata-remover-app-dk.streamlit.app)

Aplikasi berbasis Streamlit untuk menganalisis dan **menghapus metadata sensitif** dari berbagai jenis file — melindungi privasi Anda sebelum file dibagikan ke publik.

> Setiap file yang Anda bagikan dapat menyimpan "rahasia" di balik
> layarnya. Mulai dari lokasi GPS pada foto, nama pembuat dokumen,
> hingga informasi perangkat yang digunakan.
>
> **Metadata Remover** adalah aplikasi web berbasis **Streamlit** untuk
> membantu menganalisis, mengklasifikasikan, dan membersihkan metadata
> dari berbagai jenis file sebelum file dibagikan kepada pihak lain.

------------------------------------------------------------------------

## 📌 Daftar Isi

-   [✨ Fitur Unggulan](#-fitur-unggulan)
-   [🔄 Alur Kerja Aplikasi](#-alur-kerja-aplikasi)
-   [📁 Format File yang Didukung](#-format-file-yang-didukung)
-   [🚀 Cara Menjalankan](#-cara-menjalankan)
-   [🐳 Deployment dengan Docker](#-deployment-dengan-docker)
-   [🔔 Konfigurasi Webhook](#-konfigurasi-webhook)
-   [🛠️ Teknologi](#️-teknologi)
-   [📂 Struktur Direktori](#-struktur-direktori)
-   [🔐 Privasi dan Keamanan](#-privasi-dan-keamanan)
-   [🧪 Testing](#-testing)
-   [🤝 Contributing](#-contributing)
-   [🐛 Bug Report](#-bug-report)
-   [💡 Feature Request](#-feature-request)
-   [🚀 Roadmap](#-roadmap)
-   [📄 Lisensi](#-lisensi)

------------------------------------------------------------------------

# ✨ Fitur Unggulan

## 📂 All-in-One Multi-Format Support

Mendukung berbagai jenis file melalui handler khusus:

  Kategori          Format
  ----------------- ----------------------
  🖼️ Gambar         JPG, JPEG, PNG, WebP
  📄 Dokumen        PDF, DOCX
  📊 Spreadsheet    XLSX
  📑 Presentation   PPTX
  🎵 Audio          MP3

------------------------------------------------------------------------

## 🚦 Tier-Based Threat Analysis

Metadata diklasifikasikan berdasarkan tingkat sensitivitas:

  Tier            Level            Contoh
  --------------- ---------------- -----------------------------------------
  🔴 **Tier 1**   **Bahaya**       GPS, lokasi, author, informasi sensitif
  🟡 **Tier 2**   **Peringatan**   Model perangkat, software, versi OS
  🟢 **Tier 3**   **Aman**         Resolusi, bitrate, informasi teknis

------------------------------------------------------------------------

## 📦 Batch Processing

Pengguna dapat memproses beberapa file sekaligus.

Alurnya:

1.  📥 Upload file
2.  🔍 Analisis metadata
3.  🚦 Klasifikasi metadata
4.  🧹 Pembersihan metadata
5.  📄 Membuat file hasil
6.  📦 Mengemas hasil ke ZIP

------------------------------------------------------------------------

## ✏️ Custom Output Naming

File hasil dapat diberi nama baru.

Contoh:

``` text
foto-liburan.jpg
        ↓
foto-liburan_clean.jpg
```

------------------------------------------------------------------------

## ⏱️ Progress Tracking

Proses batch dapat menampilkan status dan perkembangan pemrosesan
sehingga pengguna dapat mengetahui file yang sedang diproses.

------------------------------------------------------------------------

## 🔔 Webhook Notifications

Aplikasi menyediakan integrasi webhook untuk notifikasi proses melalui:

-   💬 Discord
-   💼 Slack

URL webhook disimpan melalui environment variable sehingga tidak perlu
ditulis langsung di source code.

------------------------------------------------------------------------

## 🌙 Dark Mode

Tampilan aplikasi mendukung konfigurasi tema dan preferensi tampilan
yang nyaman digunakan dalam waktu lama.

------------------------------------------------------------------------

# 🔄 Alur Kerja Aplikasi

Secara umum, proses Metadata Remover:

``` text
┌─────────────────────┐
│     User Upload     │
│   One / Multiple    │
│        Files        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   File Validation   │
│ Type / Extension    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Metadata Extraction │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Threat Classification│
│       Tier 1-3      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Metadata Sanitizing │
│      / Removal      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│    Clean Output     │
└──────────┬──────────┘
           │
      ┌────┴────┐
      ▼         ▼
┌──────────┐ ┌──────────┐
│Single File│ │ ZIP File │
└──────────┘ └─────┬────┘
                   │
                   ▼
            ┌──────────────┐
            │    Webhook   │
            │ Discord/Slack│
            └──────────────┘
```

### Tahapan

**1. Upload**\
Pengguna mengunggah satu atau beberapa file.

**2. Validation**\
Aplikasi menentukan format file dan handler yang sesuai.

**3. Metadata Extraction**\
Handler membaca metadata yang tersedia.

**4. Classification**\
Metadata dikategorikan berdasarkan tingkat risiko.

**5. Sanitization**\
Metadata yang didukung dibersihkan.

**6. Output**\
File hasil diberikan kepada pengguna atau dikemas menjadi ZIP untuk
batch processing.

**7. Notification**\
Jika webhook dikonfigurasi, aplikasi dapat mengirimkan notifikasi
proses.

------------------------------------------------------------------------

# 📁 Format File yang Didukung

  Format             Handler              Library
  ------------------ -------------------- -------------
  `.jpg` / `.jpeg`   `image_handler.py`   Pillow
  `.png`             `image_handler.py`   Pillow
  `.webp`            `image_handler.py`   Pillow
  `.pdf`             `pdf_handler.py`     pikepdf
  `.docx`            `Docx_handler.py`    python-docx
  `.xlsx`            `Xlsx_handler.py`    openpyxl
  `.pptx`            `Pptx_handler.py`    python-pptx
  `.mp3`             `audio_handler.py`   mutagen

> ⚠️ Kemampuan pembersihan metadata bergantung pada karakteristik
> masing-masing format dan implementasi handler.

------------------------------------------------------------------------

# 🚀 Cara Menjalankan

## 1. Clone Repository

``` bash
git clone https://github.com/kurniawan-Donn/metadata-remover-streamlit.git
cd metadata-remover-streamlit
```

## 2. Buat Virtual Environment

### Windows

``` bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

``` bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install Dependencies

``` bash
pip install -r requirements.txt
```

## 4. Jalankan Aplikasi

``` bash
streamlit run app.py
```

Buka:

``` text
http://localhost:8501
```

------------------------------------------------------------------------

# 🐳 Deployment dengan Docker

Metadata Remover dapat dijalankan di dalam container Docker.

## 📦 Build Image

``` bash
docker build -t metadata-remover .
```

## ▶️ Docker Run

``` bash
docker run -d \
  --name metadata-remover \
  -p 8501:8501 \
  metadata-remover
```

Aplikasi dapat diakses melalui:

``` text
http://localhost:8501
```

## 🔔 Docker Run dengan Webhook

``` bash
docker run -d \
  --name metadata-remover \
  -p 8501:8501 \
  -e DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..." \
  -e SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..." \
  metadata-remover
```

## 🧱 Contoh Dockerfile

``` dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
```

------------------------------------------------------------------------

# 🔔 Konfigurasi Webhook

Webhook menggunakan environment variable.

## 💬 Discord

``` env
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK
```

## 💼 Slack

``` env
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR_WEBHOOK
```

## 📄 `.env.example`

Sediakan file `.env.example`:

``` env
# Discord
DISCORD_WEBHOOK_URL=

# Slack
SLACK_WEBHOOK_URL=
```

Kemudian buat `.env` sendiri untuk environment lokal.

### 🔐 Jangan Hardcode Secret

❌ Hindari:

``` python
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/REAL_SECRET"
```

✅ Gunakan:

``` python
import os

discord_webhook = os.getenv("DISCORD_WEBHOOK_URL")
slack_webhook = os.getenv("SLACK_WEBHOOK_URL")
```

Tambahkan ke `.gitignore`:

``` gitignore
.env
*.env
```

------------------------------------------------------------------------

# 🛠️ Teknologi

  Komponen       Teknologi     Kegunaan
  -------------- ------------- -----------------------
  🌐 Framework   Streamlit     Web UI
  📄 PDF         pikepdf       Pemrosesan PDF
  🖼️ Image       Pillow        Pemrosesan gambar
  📝 DOCX        python-docx   Pemrosesan Word
  📊 XLSX        openpyxl      Pemrosesan Excel
  📑 PPTX        python-pptx   Pemrosesan PowerPoint
  🎵 Audio       mutagen       Pemrosesan ID3
  🌐 HTTP        requests      Webhook
  📦 Archive     zipfile       ZIP batch output
  🐳 Container   Docker        Deployment

------------------------------------------------------------------------

# 📂 Struktur Direktori

Struktur berdasarkan proyek **Metadata_del**:

``` text
Metadata_del/
│
├── handlers/
│   ├── .streamlit/
│   │   └── config.toml
│   ├── __init__.py
│   ├── audio_handler.py
│   ├── Docx_handler.py
│   ├── image_handler.py
│   ├── pdf_handler.py
│   ├── Pptx_handler.py
│   └── Xlsx_handler.py
│
├── sortable_component/
│   └── index.html
│
├── .streamlit/
│   └── config.toml
│
├── tests/
│   ├── audio/
│   ├── image/
│   └── office/
│
├── .gitignore
├── app.py
├── batch_handler.py
├── cek.py
├── components.py
├── file_config.py
├── handler_router.py
├── hapus.py
├── icons.py
├── metadata_tiers.py
├── progress_tracker.py
├── README.md
├── requirements.txt
├── sortable_list.py
├── styles.py
├── theme.py
└── webhook.py
```

### 🧩 Komponen Utama

  File / Folder              Fungsi
  -------------------------- ------------------------------------
  `app.py`                   🚀 Entry point aplikasi Streamlit
  `handlers/`                🧹 Handler berdasarkan format file
  `audio_handler.py`         🎵 Handler metadata audio
  `image_handler.py`         🖼️ Handler metadata gambar
  `pdf_handler.py`           📄 Handler metadata PDF
  `Docx_handler.py`          📝 Handler metadata DOCX
  `Pptx_handler.py`          📑 Handler metadata PPTX
  `Xlsx_handler.py`          📊 Handler metadata XLSX
  `handler_router.py`        🔀 Routing file ke handler
  `batch_handler.py`         📦 Batch processing
  `file_config.py`           ⚙️ Konfigurasi file
  `metadata_tiers.py`        🚦 Klasifikasi metadata
  `progress_tracker.py`      ⏱️ Progress processing
  `components.py`            🧩 Komponen UI
  `styles.py`                🎨 Styling
  `theme.py`                 🌙 Theme configuration
  `icons.py`                 🎯 Icon
  `sortable_list.py`         ↕️ Sortable file list
  `sortable_component/`      🖥️ Komponen sortable frontend
  `webhook.py`               🔔 Discord / Slack webhook
  `tests/`                   🧪 Test project
  `requirements.txt`         📦 Python dependencies
  `.streamlit/config.toml`   ⚙️ Konfigurasi Streamlit

> 💡 `venv/` dan `__pycache__/` adalah environment/cache lokal dan
> sebaiknya tidak di-commit ke repository.

------------------------------------------------------------------------

# 🏗️ Arsitektur Aplikasi

``` text
                    ┌─────────────────┐
                    │     app.py      │
                    │   Streamlit UI  │
                    └────────┬────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ handler_router.py   │
                  │   File Detection    │
                  └──────────┬──────────┘
                             │
             ┌───────────────┼───────────────┐
             ▼               ▼               ▼
       ┌──────────┐    ┌──────────┐    ┌──────────┐
       │  Image   │    │  Office  │    │   PDF    │
       │ Handler  │    │ Handlers │    │ Handler  │
       └────┬─────┘    └────┬─────┘    └────┬─────┘
            │               │               │
            └───────────────┼───────────────┘
                            ▼
                 ┌────────────────────┐
                 │ metadata_tiers.py  │
                 │ Threat Analysis    │
                 └─────────┬──────────┘
                           │
                           ▼
                 ┌────────────────────┐
                 │ Metadata Removal   │
                 └─────────┬──────────┘
                           │
                           ▼
                 ┌────────────────────┐
                 │  batch_handler.py  │
                 │    ZIP / Output    │
                 └─────────┬──────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  webhook.py │
                    │Discord/Slack│
                    └─────────────┘
```

------------------------------------------------------------------------

# 🔐 Privasi dan Keamanan

Metadata Remover dibuat dengan fokus pada privasi file pengguna.

Praktik keamanan yang direkomendasikan:

-   🔒 Jangan menyimpan file pengguna lebih lama dari yang diperlukan.
-   🚫 Jangan memasukkan isi file pengguna ke dalam log.
-   🔑 Simpan webhook dan secret melalui environment variable.
-   🧹 Hapus temporary file setelah proses selesai.
-   📦 Jangan commit file pengguna ke repository.
-   🔍 Validasi tipe dan ekstensi file.
-   🔐 Jangan commit credential atau API key.

## ⚠️ Catatan Penting

Metadata removal tidak selalu berarti seluruh informasi tersembunyi
dalam sebuah file berhasil dihapus.

File dapat memiliki:

``` text
File
├── Metadata
│   ├── EXIF
│   ├── GPS
│   ├── Author
│   ├── Software
│   └── Timestamp
│
└── Content
    ├── Text
    ├── Image
    ├── Comment
    └── Embedded Object
```

Untuk file yang sangat sensitif, selalu lakukan pemeriksaan ulang
terhadap file hasil sanitasi.

------------------------------------------------------------------------

# 🧪 Testing

Test project tersedia pada:

``` text
tests/
├── audio/
├── image/
└── office/
```

Jika project menggunakan `pytest`, jalankan:

``` bash
pytest
```

Test berdasarkan kategori:

``` bash
pytest tests/image
```

``` bash
pytest tests/audio
```

``` bash
pytest tests/office
```

------------------------------------------------------------------------

# 🤝 Contributing

Kontribusi sangat terbuka dan dihargai. ❤️

## 1. Fork Repository

Fork repository melalui GitHub.

## 2. Clone Repository

``` bash
git clone https://github.com/YOUR_USERNAME/metadata-remover-streamlit.git
cd metadata-remover-streamlit
```

## 3. Buat Branch

``` bash
git checkout -b feature/nama-fitur
```

Contoh:

``` text
feature/add-new-format
fix/pdf-metadata
refactor/handler
docs/update-readme
test/image-handler
```

## 4. Lakukan Perubahan

Pastikan perubahan:

-   ✅ Tidak merusak fitur yang sudah ada.
-   ✅ Mengikuti struktur proyek.
-   ✅ Tidak memasukkan secret.
-   ✅ Tidak memasukkan file pribadi.
-   ✅ Memiliki test jika diperlukan.
-   ✅ Memperbarui dokumentasi jika diperlukan.

## 5. Jalankan Test

``` bash
pytest
```

## 6. Commit

Gunakan commit message yang jelas:

``` bash
git add .
git commit -m "feat: add support for new metadata format"
```

Prefix yang direkomendasikan:

  Prefix        Penggunaan
  ------------- ---------------
  `feat:`       Fitur baru
  `fix:`        Perbaikan bug
  `docs:`       Dokumentasi
  `refactor:`   Refactoring
  `test:`       Testing
  `chore:`      Maintenance

## 7. Push

``` bash
git push origin feature/nama-fitur
```

## 8. Pull Request

Buat Pull Request dan jelaskan:

-   Apa yang diubah?
-   Mengapa perubahan diperlukan?
-   Bagaimana cara melakukan testing?
-   Apakah ada perubahan dependency?
-   Apakah ada perubahan konfigurasi?

------------------------------------------------------------------------

# 🐛 Bug Report

Jika menemukan bug, buat Issue dengan informasi:

``` text
### Description

Jelaskan masalah.


### Steps to Reproduce

1. Upload file ...
2. Klik ...
3. Masalah terjadi ...


### Expected Behavior

Jelaskan hasil yang diharapkan.


### Actual Behavior

Jelaskan hasil yang terjadi.


### Environment

OS:
Python:
Browser:
Docker:
Streamlit:
```

> ⚠️ Jangan mengunggah file pribadi atau file yang mengandung data
> sensitif ke issue publik.

------------------------------------------------------------------------

# 💡 Feature Request

Punya ide fitur baru?

Beberapa pengembangan yang dapat dipertimbangkan:

-   🖼️ Dukungan format gambar tambahan
-   📄 Dukungan format dokumen tambahan
-   🔍 Metadata scanner yang lebih detail
-   📊 Export laporan metadata
-   🔐 Local-only processing mode
-   🧪 Automated security testing
-   📈 Processing analytics
-   🔄 Background processing
-   📋 Detailed sanitization report
-   ⚙️ Configurable sanitization rules

Silakan buat Issue terlebih dahulu agar fitur dapat didiskusikan sebelum
implementasi.

------------------------------------------------------------------------

# 🚀 Roadmap

``` text
[x] Multi-format metadata analysis
[x] Metadata classification
[x] Batch processing
[x] ZIP output
[x] Webhook integration
[x] Dark mode
[ ] Docker support
[ ] Expanded automated test coverage
[ ] CI/CD pipeline
[ ] Additional file formats
[ ] Advanced metadata inspection
[ ] Configurable sanitization rules
[ ] Detailed sanitization report
```

> Roadmap dapat berubah berdasarkan kebutuhan proyek dan kontribusi
> komunitas.

------------------------------------------------------------------------

# 📄 Lisensi

Proyek ini dirilis menggunakan **MIT License**.

Dengan lisensi MIT, pengguna diperbolehkan untuk:

-   ✅ Menggunakan proyek
-   ✅ Menyalin proyek
-   ✅ Memodifikasi proyek
-   ✅ Mengembangkan proyek
-   ✅ Menggunakan untuk kebutuhan komersial
-   ✅ Mendistribusikan ulang proyek

Lihat file [`LICENSE`](LICENSE) untuk informasi lengkap.

------------------------------------------------------------------------

# ❤️ Support

Jika proyek ini bermanfaat:

⭐ Berikan **Star** pada repository.

🐛 Laporkan bug.

💡 Ajukan feature request.

🤝 Berkontribusi melalui Pull Request.

📢 Bagikan proyek kepada orang lain.

------------------------------------------------------------------------

---

## 📄 Lisensi

Project ini dilisensikan di bawah **MIT License**.

Anda bebas untuk:
- ✅ Menggunakan secara komersial
- ✅ Memodifikasi
- ✅ Mendistribusikan
- ✅ Menggunakan secara privat

Dengan syarat mencantumkan copyright notice dan license notice asli.

Lihat file [LICENSE](LICENSE) untuk detail lengkap.

---

## 🙏 Kredit

Dibuat oleh [kurniawan-donn](https://github.com/kurniawan-Donn).

Ikon oleh [Lucide Icons](https://lucide.dev) (ISC License).

---

## ⭐ Dukung Project

Kalau project ini bermanfaat, berikan ⭐ di [GitHub](https://github.com/kurniawan-Donn/metadata-remover-streamlit)!

::: {align="center"}
## 🛡️ Metadata Remover

### Clean Your Files. Protect Your Privacy.

Made with ❤️ and Python 🐍

⭐ **If this project helps you, don't forget to star the repository!**
:::
