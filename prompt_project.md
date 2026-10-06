# Prompt: Buat Project API Data Mahasiswa v2.0 (FastAPI + Swagger UI Kustom)

Gunakan file ini sebagai prompt/instruksi lengkap di folder lain untuk
membuat project yang sama persis. Ikuti seluruh bagian di bawah ini
tanpa mengubah struktur, nama file, endpoint, maupun desain.

---

## 1. Ringkasan Project

Bangun REST API CRUD sederhana bernama **API Data Mahasiswa** versi
**2.0.0** menggunakan FastAPI, dengan ciri khusus:

1. Database simulasi in-memory (dictionary Python), tanpa database sungguhan.
2. Model data mahasiswa: `nama`, `alamat`, `ipk`, `semester`, `hobi`.
3. Endpoint `/items/{item_id}` untuk operasi CREATE, READ, UPDATE, DELETE.
4. Status error sesuai standar REST: **404** (tidak ada), **409** (duplikat),
   **422** (validasi gagal) - bukan 200.
5. Dokumentasi Swagger UI di `/docs` **didesain kustom** (light theme, banner
   versi) dan kodenya **dipisah ke file sendiri** (`swagger_ui.py`).
6. Ada file markdown penjelasan semua output (`penjelasan_output.md`) untuk
   bahan presentasi.

---

## 2. Lingkungan & Setup

- OS: Windows, Python 3.14 (atau versi modern lain).
- Buat virtual environment bernama `env`:

```bash
python -m venv env
env\Scripts\pip install fastapi uvicorn
```

- Jalankan server:

```bash
env\Scripts\python -m uvicorn main:app --reload
```

- URL: `http://127.0.0.1:8000` (docs: `/docs`, spec: `/openapi.json`).

### Struktur folder yang wajib ada

```
project-folder/
  main.py                 # logika aplikasi (model + endpoint CRUD)
  swagger_ui.py           # desain Swagger UI (terpisah dari main.py)
  penjelasan_output.md    # penjelasan semua output untuk presentasi
  requirements.txt        # fastapi, uvicorn
```

---

## 3. Spesifikasi `main.py`

### 3.1 Konfigurasi aplikasi

```python
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from swagger_ui import setup_swagger_ui

app = FastAPI(
    title="API Data Mahasiswa",
    description=(...),   # deskripsi CRUD + catatan iterasi pengembangan v2.0
    version="2.0.0",
    docs_url=None,       # docs default dimatikan, diganti route kustom
)
setup_swagger_ui(app)
```

### 3.2 Model data

Semua field **opsional** (tanpa validasi tambahan):

```python
class Item(BaseModel):
    nama: Optional[str] = None
    alamat: Optional[str] = None
    ipk: Optional[float] = None
    semester: Optional[int] = None
    hobi: Optional[str] = None
```

### 3.3 Database simulasi

```python
items_db = {}   # key: item_id (int), value: dict hasil item.model_dump()
```

### 3.4 Endpoint (4 buah, path wajib persis seperti ini)

| Method | Path | Fungsi | Sukses | Error |
|---|---|---|---|---|
| POST | `/items/{item_id}` | Tambah data | 200 | 409 jika id sudah ada, 422 jika tipe data salah |
| GET | `/items/{item_id}` | Ambil 1 data | 200 | 404 jika id tidak ada |
| PUT | `/items/{item_id}` | Ubah data | 200 | 404 jika id tidak ada, 422 jika tipe data salah |
| DELETE | `/items/{item_id}` | Hapus data | 200 | 404 jika id tidak ada |

Aturan implementasi:

- Semua handler memakai `async def`.
- Serialisasi model memakai **`item.model_dump()`** (Pydantic v2), bukan
  `.dict()` yang deprecated.
- Error memakai `raise HTTPException(status_code=..., detail=...)`
  (format respons error otomatis `{"detail": "..."}`), **bukan** return dict
  error dengan status 200.
- Variabel hasil pop pada DELETE dinamai `deleted_item` (jangan menimpa
  nama fungsi endpoint).

### 3.5 Bentuk respons (wajib sama)

**POST sukses - 200:**

```json
{
  "message": "Item created successfully",
  "item": {"nama": "Budi Santoso", "alamat": "Jl. Merdeka No. 10", "ipk": 3.75, "semester": 5, "hobi": "Bersepeda"}
}
```

**GET sukses - 200:**

```json
{
  "item_id": 1,
  "item": {"nama": "Budi Santoso", "alamat": "Jl. Merdeka No. 10", "ipk": 3.75, "semester": 5, "hobi": "Bersepeda"}
}
```

**PUT sukses - 200:**

```json
{
  "message": "Item updated successfully",
  "item": { ...data terbaru... }
}
```

**DELETE sukses - 200:**

```json
{
  "message": "Item deleted successfully",
  "deleted_item": { ...data yang dihapus... }
}
```

**Error 404 / 409:**

```json
{"detail": "Item not found"}
{"detail": "Item already exists"}
```

**Error 422 (tipe data salah, misal ipk diisi teks):**

```json
{
  "detail": [
    {"type": "float_parsing", "loc": ["body", "ipk"], "msg": "Input should be a valid number, unable to parse string as a number", "input": "bukan-angka"}
  ]
}
```

---

## 4. Spesifikasi `swagger_ui.py` (Desain Dokumentasi)

File ini **terpisah** dari `main.py`. Isinya hanya urusan tampilan `/docs`.

### 4.1 Struktur file

```python
from fastapi import FastAPI, Request
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse

SWAGGER_UI_PARAMETERS = { ... }
CUSTOM_STYLE = """<style> ... </style>"""
BANNER = """<div class="dev-banner"> ... </div>"""

def setup_swagger_ui(app: FastAPI) -> None:
    async def custom_swagger_ui_html(request: Request) -> HTMLResponse:
        response = get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title="API Data Mahasiswa v2.0 - Swagger UI",
            oauth2_redirect_url=None,
            swagger_ui_parameters=SWAGGER_UI_PARAMETERS,
        )
        html = response.body.decode("utf-8")
        html = html.replace("</head>", CUSTOM_STYLE + "\n</head>")
        html = html.replace("<body>", "<body>" + BANNER)
        return HTMLResponse(html)

    app.add_route("/docs", custom_swagger_ui_html, include_in_schema=False)
```

Penting: parameter handler **wajib menerima `request: Request`**, jika tidak
akan error `takes 0 positional arguments but 1 was given`.

### 4.2 Konfigurasi Swagger UI

```python
SWAGGER_UI_PARAMETERS = {
    "docExpansion": "none",
    "filter": True,
    "persistAuthorization": True,
    "tryItOutEnabled": True,
    "displayRequestDuration": True,
    "tagsSorter": "alpha",
    "operationsSorter": "alpha",
    "defaultModelsExpandDepth": 1,
    "showCommonExtensions": True,
    "showExtensions": True,
    "deepLinking": True,
}
```

### 4.3 Aturan desain (wajib)

- **Tema terang dan clean**, bukan gelap: background halaman `#f6f8fa`,
  kartu/panel putih `#ffffff`, teks utama `#1f2328`, border `#d0d7de`.
- **Tanpa emoji sama sekali** di banner, favicon, maupun teks lain.
- Banner sticky di atas berisi:
  - Judul: `API Data Mahasiswa`
  - Badge: `v2.0 - Iterasi Pengembangan` (latar `#0969da`, teks putih,
    bentuk pill/rounded)
  - Catatan kanan: `Fitur baru: dokumentasi Swagger UI kustom (light theme), status error REST 404 / 409`
- Warna tombol method harus tegas dan berbeda, plus border-left kartu 5px
  sewarna:

| Method | Warna tombol | Kode hex |
|---|---|---|
| GET | Hijau | `#1a7f37` |
| POST | Biru | `#0969da` |
| PUT | Oranye | `#bc4c00` |
| DELETE | Merah | `#cf222e` |

- Latar kartu operasi di-tint sangat ringan sewarna method
  (misal GET `#f6fbf7`, POST `#f3f8fd`, PUT `#fffbf1`, DELETE `#fff8f7`).
- Tombol `Execute`/`Try it out` hijau `#1a7f37` teks putih; tombol biasa
  putih/abu terang; `Authorize` ungu `#8250df`.
- Input fokus: border `#0969da` + shadow halus `rgba(9, 105, 218, 0.15)`.
- Judul info, tag, tabel, dan schema dibuat kontras rapi (terang, bersih,
  modern - meniru gaya GitHub light).
- CSS diinjeksi ke HTML Swagger via `replace("</head>", CUSTOM_STYLE + "</head>")`
  dan banner via `replace("<body>", "<body>" + BANNER)`.

---

## 5. Spesifikasi `penjelasan_output.md`

Buat file markdown berisi penjelasan lengkap semua output project untuk
bahan presentasi ke dosen. Wajib memuat bagian:

1. **Gambaran umum**: framework, versi, cara menjalankan, tabel struktur file.
2. **Penjelasan elemen halaman `/docs`**: arti banner versi, arti info
   title/version/description, tabel warna method beserta maknanya, fungsi
   tombol `Try it out`, `Execute`, `Cancel`, `Authorize`.
3. **Panel output setelah Execute**: penjelasan `Request URL`,
   `Request Headers`, `Response Body`, `Response Code`, `Response Headers`.
4. **Tabel daftar endpoint** (method, request URL, fungsi, status sukses/error).
5. **Detail tiap endpoint**: request URL, request body JSON, **perintah
   curl**, response body sukses, response body error (semua contoh output
   nyata seperti di bagian 3.5).
6. **Makna tiap field response body** (tabel).
7. **Tabel kode status HTTP** yang dipakai: 200, 404, 409, 422 beserta
   kapan muncul dan pesannya.
8. **Penjelasan `/openapi.json`**: bagian `info`, `paths`,
   `components.schemas.Item` dan hubungannya dengan tampilan `/docs`.
9. **Alur presentasi yang disarankan** (langkah demo untuk dosen).
10. **Catatan teknis**: database in-memory reset saat restart,
    `model_dump()` Pydantic v2, pemisahan file desain.

Contoh blok curl yang harus ada:

```bash
curl -X POST "http://127.0.0.1:8000/items/1" \
  -H "Content-Type: application/json" \
  -d "{\"nama\":\"Budi Santoso\",\"alamat\":\"Jl. Merdeka No. 10\",\"ipk\":3.75,\"semester\":5,\"hobi\":\"Bersepeda\"}"
```

---

## 6. Kriteria Penerimaan (Acceptance Criteria)

Project dianggap benar jika semua poin berikut terpenuhi:

- [ ] `env\Scripts\python -c "import warnings; warnings.simplefilter('error', DeprecationWarning); import main"` berjalan tanpa error (tidak ada warning deprecated).
- [ ] POST id baru → 200; POST id duplikat → 409 dengan `{"detail": "Item already exists"}`.
- [ ] GET id ada → 200 dengan `item_id` + `item`; GET id kosong → 404.
- [ ] PUT id ada → 200; PUT id kosong → 404.
- [ ] DELETE id ada → 200 dengan `deleted_item`; DELETE lagi → 404.
- [ ] Kirim `ipk` berupa teks → 422 dengan array `detail` berisi `type`, `loc`, `msg`, `input`.
- [ ] `/docs` mengembalikan 200, memuat banner `dev-banner`, badge
      `v2.0 - Iterasi Pengembangan`, warna `#f6f8fa` (terang), dan
      **tidak** memuat emoji.
- [ ] `/openapi.json` menunjukkan `version: 2.0.0`, path `/items/{item_id}`,
      dan schema `Item` berisi `nama, alamat, ipk, semester, hobi`.
- [ ] Kode desain Swagger UI berada di `swagger_ui.py` (bukan di `main.py`).
- [ ] File `penjelasan_output.md` ada dan memuat semua bagian di bagian 5.

### Cara tes cepat

```bash
# terminal 1
env\Scripts\python -m uvicorn main:app --port 8000

# terminal 2
curl -X POST "http://127.0.0.1:8000/items/1" -H "Content-Type: application/json" -d "{\"nama\":\"Budi Santoso\",\"ipk\":3.75,\"semester\":5}"
curl "http://127.0.0.1:8000/items/1"
curl "http://127.0.0.1:8000/items/99"
curl -I "http://127.0.0.1:8000/docs"
```

---

## 7. Batasan (Jangan Dilakukan)

- Jangan membuat endpoint lain selain 4 endpoint CRUD + `/docs`
  (root `/` boleh dikomentari saja).
- Jangan memakai database sungguhan (SQLite/Postgres) - cukup dict.
- Jangan menambahkan autentikasi/jwt.
- Jangan memakai tema gelap untuk `/docs`.
- Jangan menaruh CSS/HTML desain di dalam `main.py`.
- Jangan memakai emoji di file mana pun.
