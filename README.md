# Videoplayer App

Aplikasi ini menggabungkan backend FastAPI dengan frontend Vue 3 untuk membuat videoplayer.

## Prasyarat
- Python 3.10+ (disarankan 3.11)
- Node.js 20.19 atau 22.12 ke atas (mengikuti batasan di `frontend/package.json`)
- npm 10+

## Instalasi Dependensi

### Backend
1. Masuk ke folder backend:
   ```bash
   cd backend
   ```
2. (Opsional) Buat environment virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```
3. Instal dependensi:
   ```bash
   pip install -r requirements.txt
   ```

### Frontend
1. Masuk ke folder frontend:
   ```bash
   cd frontend
   ```
2. Instal dependensi npm:
   ```bash
   npm install
   ```

## Menjalankan Aplikasi

### Backend (FastAPI)
1. Masuk ke folder backend:
   ```bash
   cd backend
   ```
2. Dari direktori backend:
```bash
uvicorn app:app --reload
```
Backend akan melayani API di `http://127.0.0.1:8000`.

3. Rubah url untuk qr code di api/qr-data:
```bash
    async def get_qr_data():
        return {
            "url": "https://ngobrolinhpv.com/",
            "title": "Scan untuk mengunjungi website"
        }
```
4. Tambahkan video di directori backend/static/videos/
```bash
    masukan video yg sudah anda download ke dalam folder videos
```

### Frontend (Vite)
1. Jalankan server pengembangan Vite dari dalam folder `frontend`:
   ```bash
   npm run dev
   ```
2. Buka URL yang ditampilkan (biasanya `http://127.0.0.1:5173`).

## Struktur Direktori
```
backend/   # FastAPI
frontend/  # Aplikasi Vue 3 dengan Vite
```

## Catatan Tambahan
- Untuk produksi, build frontend dengan `npm run build` dan layani hasilnya melalui server pilihan Anda.
