````markdown
# Braves Board Backend

Backend API untuk aplikasi manajemen tugas (Task Tracker) Braves Board. Dibangun menggunakan arsitektur modern berkinerja tinggi berbasis *Domain-Driven Design* (DDD) yang dirancang agar kompatibel dengan lingkungan Serverless Google Cloud Platform (GCP).

## Teknologi Utama

* **Framework:** FastAPI (Python 3.11)
* **Database Relasional:** PostgreSQL 15 (via asyncpg & SQLAlchemy 2.0)
* **In-Memory Database / Cache:** Redis 7 (Untuk manajemen *hot data* seperti pelacakan durasi Timer hibrida)
* **Cloud Storage:** Google Cloud Storage (GCS) untuk lampiran file
* **Migrasi Database:** Alembic (Asynchronous)
* **Observability:** Prometheus & Grafana
* **Kontainerisasi:** Docker & Docker Compose

---

## Persyaratan Sistem (Prerequisites)

Sebelum memulai, pastikan Anda telah menginstal aplikasi berikut di mesin lokal Anda:

1. Docker Desktop (atau Docker Engine & Docker Compose)
2. Git

*(Catatan: Anda tidak perlu menginstal Python atau PostgreSQL secara lokal di OS Anda karena semuanya sudah diisolasi di dalam Docker).*

---

## Struktur Proyek Utama

Proyek ini telah direstrukturisasi agar lebih modular dan mudah dipelihara:

* `deploy/` : Berisi konfigurasi infrastruktur (Dockerfile, Docker Compose untuk Dev/Prod/Staging).
* `src/backend/app/api/` : Direktori utama kode sumber yang dipisahkan berdasarkan domain/fitur (auth, board, task, time_tracking, dll).
* `src/backend/app/config/` : Tempat menyimpan *environment variables* (`.env`) dan kredensial JSON.
* `src/backend/db_migrations/` : Folder konfigurasi dan riwayat migrasi Alembic.

---

## Cara Menjalankan Proyek di Lokal

### 1. Kloning Repositori & Setup Environment

Kloning repositori ini ke mesin lokal Anda:

```bash
git clone <url-repositori-anda>
cd braves-board-backend
````

Buat file baru bernama `development.env` di dalam folder `src/backend/app/config/env/` dan salin variabel berikut ke dalamnya:

```env
# APP CONFIGURATION
APP_ENV=development
PORT=8000

# DATABASE CONFIGURATION
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=braves_board_db
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/braves_board_db

# REDIS CONFIGURATION
REDIS_URL=redis://redis:6379/0

# JWT & SECURITY
# Gunakan perintah `openssl rand -hex 32` di terminal untuk menghasilkan secret key
JWT_SECRET=isi_dengan_string_acak_yang_aman
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7
INTERNAL_CRON_SECRET=isi_dengan_string_acak_yang_aman_untuk_scheduler

# GOOGLE OAUTH 2.0 (Dapatkan dari Google Cloud Console)
GOOGLE_CLIENT_ID=client_id_anda
GOOGLE_CLIENT_SECRET=client_secret_anda
GOOGLE_REDIRECT_URI=http://localhost:8000/api/v1/auth/google/callback

# GOOGLE CLOUD STORAGE (Untuk Lampiran Tugas)
GCS_BUCKET_NAME=nama_bucket_gcs_anda
# Path absolut di dalam kontainer Docker
GOOGLE_APPLICATION_CREDENTIALS=/app/app/config/credentials/gcp-service-account.json

# FRONTEND URL
FRONTEND_URL=http://localhost:3000
```

**Penting:** Jika Anda menggunakan fitur *Upload File*, pastikan Anda meletakkan file kredensial Service Account GCP Anda di `src/backend/app/config/credentials/gcp-service-account.json`.

---

### 2. Jalankan Kontainer Docker

Karena file `docker-compose` berada di folder `deploy/compose/`, Anda harus menggunakan *flag* `-f` untuk menunjuk ke file yang benar saat menjalankannya.

Jalankan perintah berikut di root repositori:

```bash
docker-compose -f deploy/compose/docker-compose.dev.yml up -d --build
```

Tunggu beberapa saat hingga proses *build* dan instalasi *dependencies* Python selesai.

---

### 3. Verifikasi Layanan (Akses URL)

Jika semua kontainer berstatus "Up", Anda bisa mengakses berbagai layanan berikut melalui browser:

* **API Swagger UI (Docs):** http://localhost:8000/docs
* **API ReDoc:** http://localhost:8000/redoc
* **pgAdmin (Manajemen Database):** http://localhost:8080

  * *Email:* [admin@bangunindo.com](mailto:admin@bangunindo.com)
  * *Password:* admin
  * *(Hubungkan server DB dengan Host: `db`, Username: `postgres`, Password: `postgres`)*
* **RedisInsight (Manajemen Redis):** http://localhost:5540
* **Grafana (Monitoring Metrics):** http://localhost:3000 (User/Pass: admin/admin)

---

## Manajemen Database (Alembic Migrations)

**PENTING:** Karena aplikasi berjalan di dalam kontainer, seluruh perintah Alembic harus dieksekusi **di dalam kontainer `api`**. Jangan menjalankan perintah alembic langsung dari terminal OS host Anda. Gunakan awalan `docker-compose -f ... exec api`.

---

### 1. Daftarkan Model Baru di `env.py`

Setiap kali Anda membuat model baru di `src/backend/app/models/`, Anda WAJIB mengimpornya ke dalam file `src/backend/db_migrations/env.py` agar terdeteksi oleh Alembic:

```python
from app.models.nama_file_baru import NamaModelBaru
```

---

### 2. Membuat File Migrasi Baru

Setelah model didaftarkan atau diubah, jalankan perintah berikut di root proyek untuk meng-generate skrip migrasi:

```bash
docker-compose -f deploy/compose/docker-compose.dev.yml exec api alembic revision --autogenerate -m "nama_perubahan_anda"
```

---

### 3. Menerapkan Migrasi ke Database (Upgrade)

Lakukan ini untuk mengeksekusi file migrasi agar struktur tabel di PostgreSQL diperbarui:

```bash
docker-compose -f deploy/compose/docker-compose.dev.yml exec api alembic upgrade head
```

---

### 4. Membatalkan Migrasi Terakhir (Downgrade)

```bash
docker-compose -f deploy/compose/docker-compose.dev.yml exec api alembic downgrade -1
```

---

## Perintah Operasional Docker Lainnya

**Melihat Log Aplikasi Backend (Real-time):**

```bash
docker-compose -f deploy/compose/docker-compose.dev.yml logs -f api
```

**Restart Hanya Backend (Misal setelah merubah .env):**

```bash
docker-compose -f deploy/compose/docker-compose.dev.yml restart api
```

**Mematikan Seluruh Kontainer:**

```bash
docker-compose -f deploy/compose/docker-compose.dev.yml down
```

**Mematikan Kontainer & Menghapus Semua Data (Hard Reset Database & Redis):**

```bash
docker-compose -f deploy/compose/docker-compose.dev.yml down -v
```

*(Hati-hati: Perintah ini akan menghapus seluruh data lokal di PostgreSQL, Redis, dan Grafana Anda yang ada di Docker Volume).*

```
```
