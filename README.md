# Braves Board Backend

Backend API untuk aplikasi manajemen tugas (Task Tracker) Braves Board. Dibangun menggunakan arsitektur modern berkinerja tinggi yang dirancang agar kompatibel dengan lingkungan Serverless Google Cloud Platform (GCP).

## Teknologi Utama

* Framework: FastAPI (Python 3.11)
* Database Relasional: PostgreSQL 15 (via asyncpg & SQLAlchemy 2.0)
* In-Memory Database / Cache: Redis 7 (Untuk manajemen hot data seperti pelacakan durasi Timer)
* Migrasi Database: Alembic (Asynchronous)
* Kontainerisasi: Docker & Docker Compose

---

## Persyaratan Sistem (Prerequisites)

Sebelum memulai, pastikan Anda telah menginstal aplikasi berikut di mesin lokal Anda:
1. Docker Desktop (atau Docker Engine & Docker Compose)
2. Git

(Catatan: Anda tidak perlu menginstal Python atau PostgreSQL secara lokal di OS Anda karena semuanya sudah diisolasi di dalam Docker).

---

## Cara Menjalankan Proyek di Lokal

### 1. Kloning Repositori & Setup Environment
Kloning repositori ini ke mesin lokal Anda, lalu buat file konfigurasi environment.

    git clone <url-repositori-anda>
    cd braves-board-backend

Buat file baru bernama `.env` di root direktori proyek dan salin variabel berikut ke dalamnya:

    # APP CONFIGURATION
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
    ACCESS_TOKEN_EXPIRE_MINUTES=15
    INTERNAL_CRON_SECRET=isi_dengan_string_acak_yang_aman

    # GOOGLE OAUTH 2.0 (Dapatkan dari Google Cloud Console)
    GOOGLE_CLIENT_ID=
    GOOGLE_CLIENT_SECRET=
    GOOGLE_REDIRECT_URI=http://localhost:8000/api/v1/auth/google/callback

    # FRONTEND URL
    FRONTEND_URL=http://localhost:3000

### 2. Jalankan Kontainer Docker
Gunakan Docker Compose untuk membangun image dan menjalankan seluruh infrastruktur (Backend, Database, Redis, dan pgAdmin) di latar belakang.

    docker-compose up -d --build

Tunggu beberapa saat hingga proses instalasi library Python selesai.

### 3. Verifikasi Layanan (Akses URL)
Jika semua kontainer berstatus "Up", Anda bisa mengakses layanan berikut melalui browser:
* API Swagger UI (Docs): http://localhost:8000/docs
* API ReDoc: http://localhost:8000/redoc
* pgAdmin (Manajemen Database): http://localhost:8080
  * Email: admin@bangunindo.com
  * Password: admin
  * (Hubungkan ke server DB dengan Host: db, Username: postgres, Password: postgres)

---

## Manajemen Database (Alembic Migrations)

PENTING: Karena aplikasi berjalan di dalam kontainer Docker, seluruh perintah Alembic harus dieksekusi di dalam kontainer api. Jangan menjalankan perintah alembic langsung dari terminal OS Anda.

1. Daftarkan Model Baru di env.py
Setiap kali Anda membuat atau mengubah file model di folder `app/models/`, Anda WAJIB mengimpornya ke dalam file `migrations/env.py` agar terdeteksi oleh Alembic. Tambahkan baris import di bagian atas file:
`from app.models.nama_file import NamaModel`

2. Membuat File Migrasi Baru
Setelah model didaftarkan, jalankan perintah berikut untuk meng-generate file migrasi:

    docker-compose exec api alembic revision --autogenerate -m "nama_perubahan_anda"

3. Menerapkan Migrasi ke Database (Upgrade)
(Lakukan ini untuk mengeksekusi tabel ke dalam PostgreSQL)

    docker-compose exec api alembic upgrade head

4. Membatalkan Migrasi Terakhir (Downgrade)

    docker-compose exec api alembic downgrade -1

---

## Perintah Umum Lainnya

Melihat Log Aplikasi (Real-time):

    docker-compose logs -f api

Mematikan Seluruh Kontainer:

    docker-compose down

Mematikan Kontainer dan Menghapus Data (Reset Database & Redis):

    docker-compose down -v

(Hati-hati: Perintah ini akan menghapus seluruh data lokal di PostgreSQL dan Redis Anda).