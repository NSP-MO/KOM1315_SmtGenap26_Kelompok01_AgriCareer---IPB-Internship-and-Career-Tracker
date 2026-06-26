# AgriCareer Tracker

AgriCareer Tracker adalah platform sistem informasi yang dibangun untuk memonitor dan melacak perkembangan karir, lowongan, dan lamaran kerja (khususnya bagi mahasiswa/alumni). Proyek ini berfokus pada penyediaan *backend* API yang tangguh, aman, dan dapat diandalkan untuk melayani berbagai *endpoint* kebutuhan aplikasi.

---

## Fitur Keamanan (Security Features)

Sistem ini didesain dengan memprioritaskan keamanan data pengguna, terutama dalam hal otentikasi dan perlindungan kredensial. Berikut adalah sorotan utama fitur keamanan yang diimplementasikan:

1. **Hashing \& Salting (Standar Industri)**
   - Semua *password* pengguna tidak pernah disimpan dalam bentuk *plaintext*.
   - Menggunakan pustaka `passlib` dengan skema **`sha256_crypt`** yang sangat aman.
   - **Dynamic Salting**: Setiap *password* secara otomatis disisipkan nilai *salt* yang unik dan diacak (misal: `$5$rounds=535000$<salt_unik>$<hash>`). Hal ini mencegah secara efektif ancaman peretasan menggunakan *Rainbow Table* atau *Dictionary Attack*.

2. **JSON Web Token (JWT) Authorization**
   - Otentikasi sesi dikelola menggunakan standar JWT Bearer Token.
   - Saat pengguna berhasil *login* melalui endpoint `/auth/login`, sistem mengembalikan token unik yang memuat hak akses (Role-Based Access) dengan batas waktu (*expiration*) tertentu.

3. **Verifikasi Email Terintegrasi**
   - Terdapat sistem *barrier* di mana akun baru yang mendaftar via `/auth/register` akan diblokir dari akses masuk (`HTTP 403 Forbidden`) hingga status email diverifikasi (`is_verified = True`).

4. **Integration Testing Keamanan**
   - Terdapat modul pengujian khusus `PBL/03_Source_Code/database/auth_hashing.py` yang memvalidasi langsung siklus pendaftaran, *hashing*, dan *login* ke *endpoint* API secara langsung menggunakan FastAPI `TestClient`.

---

## Panduan Instalasi (Installation Guide)

Ikuti langkah-langkah di bawah ini untuk menjalankan *backend* AgriCareer Tracker di komputer lokal Anda:

### 1. Prasyarat (*Prerequisites*)
Pastikan sistem Anda sudah terinstal:
- Python 3.9+ 
- `pip` (Python package manager)
- (Opsional) Redis server (jika fitur *caching* aktif)

### 2. Persiapan Lingkungan Virtual
Sangat disarankan untuk menggunakan *Virtual Environment* (v-env) agar tidak konflik dengan *package* Python lain di komputer Anda.
```bash
# Buka terminal dan arahkan ke root proyek (backend)
cd AgriCareer-Tracker-Progress-/backend

# Buat virtual environment
python -m venv venv

# Aktivasi venv (Windows)
venv\Scripts\activate

# Aktivasi venv (macOS/Linux)
source venv/bin/activate
```

### 3. Instalasi Dependensi
Instal seluruh paket yang dibutuhkan melalui file `requirements.txt`.
```bash
pip install -r requirements.txt
```

### 4. Konfigurasi Lingkungan (*Environment Variables*)
Buat sebuah file `.env` di dalam folder `backend/` dan isi dengan konfigurasi rahasia Anda (Token rahasia, kredensial email, dsb).
Contoh:
```env
SECRET_KEY=kunci_rahasia_jwt_anda
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Menjalankan Server
Jalankan aplikasi FastAPI menggunakan server Uvicorn.
```bash
uvicorn app.main:app --reload
```
Aplikasi backend kini berjalan di: `http://localhost:8000`
- Dokumentasi interaktif (Swagger UI) dapat diakses di: `http://localhost:8000/docs`

---

## Menguji Fitur Keamanan
Untuk memvalidasi sistem otentikasi (seperti *hashing* dan *salting*), Anda dapat menjalankan skrip integrasi yang telah kami siapkan di dalam direktori PBL:

```bash
# Pastikan Anda berada di root direktori
python PBL/03_Source_Code/database/auth_hashing.py
```
Skrip ini akan mensimulasikan *request* `/auth/register` dan `/auth/login`, serta secara transparan membedah komponen algoritma, *rounds*, dan *salt* yang tertanam di dalam *database* SQLite (`app.db`).
