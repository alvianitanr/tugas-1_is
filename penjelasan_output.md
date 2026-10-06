# Penjelasan Output - API Data Mahasiswa v2.0.0

Dokumen ini berisi penjelasan lengkap seluruh output project untuk bahan
presentasi.

---

## 1. Gambaran Umum

| Komponen | Keterangan |
|---|---|
| Nama project | API Data Mahasiswa |
| Versi | 2.0.0 |
| Framework | FastAPI |
| Server ASGI | Uvicorn |
| Validasi data | Pydantic v2 (metode `model_dump()`) |
| Database | In-memory (`dict` Python), reset saat server restart |
| Dokumentasi | Swagger UI kustom di `/docs`, spec di `/openapi.json` |
| Tema tampilan | Pink lembut, ringkas, dan bersih (bukan tema gelap) |
| URL server | `http://127.0.0.1:8000` |

### Cara menjalankan

```bash
python -m venv env
env\Scripts\pip install fastapi uvicorn
env\Scripts\python -m uvicorn main:app --reload
```

Buka `http://127.0.0.1:8000/docs` untuk dokumentasi interaktif.

### Struktur file

| File | Fungsi |
|---|---|
| `main.py` | Logika aplikasi: model `Item`, database in-memory, 4 endpoint CRUD |
| `swagger_ui.py` | Desain tampilan `/docs` (CSS, banner, parameter Swagger UI) |
| `penjelasan_output.md` | Dokumen ini, penjelasan semua output untuk presentasi |
| `requirements.txt` | Dependensi: `fastapi`, `uvicorn` |
| `env/` | Virtual environment Python |

---

## 2. Penjelasan Elemen Halaman `/docs`

### Banner (sticky di atas)

Banner `dev-banner` menempel di atas halaman, isinya dibuat minim:

| Elemen | Isi | Makna |
|---|---|---|
| Titik aksen | Bulatan kecil warna pink `#e0559a` | Penanda visual halus |
| Judul | `API Data Mahasiswa` | Nama API yang didokumentasikan |
| Pill | `Dokumentasi` | Menandai halaman ini halaman dokumentasi, bukan halaman lain |

Banner memakai latar putih transparan dengan efek blur, garis pemisah
tipis warna pink muda, dan tanpa badge versi agar tampilan tetap ringan.

### Informasi judul dan deskripsi

Bagian info berasal dari konfigurasi `FastAPI(...)` di `main.py`:

```python
app = FastAPI(
    title="API Data Mahasiswa",
    description=("CRUD data mahasiswa (nama, alamat, ipk, semester, hobi) "
                 "dengan database in-memory. Status error: 404, 409, 422."),
    version="2.0.0",
    docs_url=None,
)
```

| Field | Isi | Fungsi di `/docs` |
|---|---|---|
| `title` | API Data Mahasiswa | Menjadi judul besar di halaman docs |
| `description` | 2 kalimat singkat | Menjelaskan cakupan API dan daftar status error |
| `version` | 2.0.0 | Hanya untuk `/openapi.json`; stamp versi dan stamp OAS sengaja disembunyikan dari tampilan `/docs` lewat CSS |

### Warna tombol method

| Method | Warna tombol | Kode hex | Makna |
|---|---|---|---|
| GET | Hijau lembut | `#2f9e6f` | Operasi baca, aman/idempoten |
| POST | Pink | `#e0559a` | Operasi tulis/tambah data, warna utama tema |
| PUT | Oranye lembut | `#e79035` | Operasi ubah data |
| DELETE | Merah lembut | `#dc4a5b` | Operasi hapus, destruktif |

Border kiri tiap kartu operasi (5px) memakai warna yang sama, dan latar
kartu di-tint sangat ringan (`#f4fbf8`, `#fff3f9`, `#fffaf2`, `#fff5f6`),
sehingga jenis operasi langsung terbaca sekilas.


### Fungsi tombol

| Tombol | Fungsi |
|---|---|
| `Try it out` | Membuka mode edit pada endpoint tersebut: field body menjadi bisa diisi dan tombol `Execute` muncul |
| `Execute` | Mengirim request sungguhan ke server lalu menampilkan hasilnya pada panel response |
| `Cancel` | Membatalkan mode `Try it out` dan mengembalikan form ke keadaan baca-saja |
| `Authorize` | Membuka dialog autentikasi; project ini tidak memakai auth sehingga dialog hanya bersifat informatif |

---

## 3. Panel Output Setelah `Execute`

Setelah `Execute` ditekan, Swagger UI menampilkan panel berikut:

| Bagian | Isi | Penjelasan |
|---|---|---|
| `Request URL` | `http://127.0.0.1:8000/items/1` | URL lengkap yang benar-benar dipanggil, termasuk host, port, dan path parameter |
| `Request Headers` | `accept: application/json`, `Content-Type: application/json` | Header yang dikirim klien; `Content-Type` wajib ada agar FastAPI membaca body JSON |
| `Response Body` | JSON sesuai format endpoint | Isi respons dari server; untuk error berupa objek `detail` |
| `Response Code` | `200`, `404`, `409`, atau `422` | Kode status HTTP hasil request |
| `Response Headers` | `content-type: application/json`, `date`, `server: uvicorn`, `content-length` | Header balasan server; `content-type: application/json` menandakan respons berupa JSON |

Urutan pembacaan yang disarankan: baca `Response Code` dahulu, lalu
`Response Body`, lalu cocokkan dengan `Request URL` untuk memastikan
endpoint yang dituju benar.

---

## 4. Tabel Daftar Endpoint

| Method | Request URL | Fungsi | Sukses | Error |
|---|---|---|---|---|
| POST | `/items/{item_id}` | Tambah data baru | 200 | 409 id sudah ada, 422 tipe data salah |
| GET | `/items/{item_id}` | Ambil 1 data | 200 | 404 id tidak ada |
| PUT | `/items/{item_id}` | Ubah data | 200 | 404 id tidak ada, 422 tipe data salah |
| DELETE | `/items/{item_id}` | Hapus data | 200 | 404 id tidak ada |

`item_id` bertipe `integer`. Jika `item_id` bukan angka, FastAPI
mengembalikan 422 sebelum handler sempat berjalan.

---

## 5. Detail Tiap Endpoint

Semua contoh di bawah diambil dari output server yang berjalan.

### 5.1 POST `/items/{item_id}` - Tambah data

- Request URL: `http://127.0.0.1:8000/items/1`
- Request body JSON:

```json
{
  "nama": "Budi Santoso",
  "alamat": "Jl. Merdeka No. 10",
  "ipk": 3.75,
  "semester": 5,
  "hobi": "Bersepeda"
}
```

- Perintah curl:

```bash
curl -X POST "http://127.0.0.1:8000/items/1" \
  -H "Content-Type: application/json" \
  -d "{\"nama\":\"Budi Santoso\",\"alamat\":\"Jl. Merdeka No. 10\",\"ipk\":3.75,\"semester\":5,\"hobi\":\"Bersepeda\"}"
```

- Response sukses (200):

```json
{
  "message": "Item created successfully",
  "item": {
    "nama": "Budi Santoso",
    "alamat": "Jl. Merdeka No. 10",
    "ipk": 3.75,
    "semester": 5,
    "hobi": "Bersepeda"
  }
}
```

- Response id duplikat (409):

```json
{"detail": "Item already exists"}
```

- Response tipe data salah (422), `ipk` diisi teks:

```json
{
  "detail": [
    {
      "type": "float_parsing",
      "loc": ["body", "ipk"],
      "msg": "Input should be a valid number, unable to parse string as a number",
      "input": "bukan-angka"
    }
  ]
}
```

### 5.2 GET `/items/{item_id}` - Ambil 1 data

- Request URL: `http://127.0.0.1:8000/items/1`
- Request body: tidak ada (GET tidak mengirim body)
- Perintah curl:

```bash
curl "http://127.0.0.1:8000/items/1"
```

- Response sukses (200):

```json
{
  "item_id": 1,
  "item": {
    "nama": "Budi Santoso",
    "alamat": "Jl. Merdeka No. 10",
    "ipk": 3.75,
    "semester": 5,
    "hobi": "Bersepeda"
  }
}
```

- Response id tidak ada (404):

```json
{"detail": "Item not found"}
```

### 5.3 PUT `/items/{item_id}` - Ubah data

- Request URL: `http://127.0.0.1:8000/items/1`
- Request body JSON:

```json
{
  "nama": "Budi Santoso",
  "alamat": "Jl. Merdeka No. 10",
  "ipk": 3.8,
  "semester": 6,
  "hobi": "Bersepeda"
}
```

- Perintah curl:

```bash
curl -X PUT "http://127.0.0.1:8000/items/1" \
  -H "Content-Type: application/json" \
  -d "{\"nama\":\"Budi Santoso\",\"alamat\":\"Jl. Merdeka No. 10\",\"ipk\":3.8,\"semester\":6,\"hobi\":\"Bersepeda\"}"
```

- Response sukses (200):

```json
{
  "message": "Item updated successfully",
  "item": {
    "nama": "Budi Santoso",
    "alamat": "Jl. Merdeka No. 10",
    "ipk": 3.8,
    "semester": 6,
    "hobi": "Bersepeda"
  }
}
```

- Response id tidak ada (404):

```json
{"detail": "Item not found"}
```

- Response tipe data salah (422), `semester` diisi teks:

```json
{
  "detail": [
    {
      "type": "int_parsing",
      "loc": ["body", "semester"],
      "msg": "Input should be a valid integer, unable to parse string as an integer",
      "input": "lima"
    }
  ]
}
```

### 5.4 DELETE `/items/{item_id}` - Hapus data

- Request URL: `http://127.0.0.1:8000/items/1`
- Request body: tidak ada
- Perintah curl:

```bash
curl -X DELETE "http://127.0.0.1:8000/items/1"
```

- Response sukses (200):

```json
{
  "message": "Item deleted successfully",
  "deleted_item": {
    "nama": "Budi Santoso",
    "alamat": "Jl. Merdeka No. 10",
    "ipk": 3.8,
    "semester": 6,
    "hobi": "Bersepeda"
  }
}
```

- Response diulang lagi setelah data terhapus (404):

```json
{"detail": "Item not found"}
```

---

## 6. Makna Tiap Field Response Body

### Field umum

| Field | Tipe | Makna |
|---|---|---|
| `message` | string | Konfirmasi operasi berhasil (POST, PUT, DELETE) |
| `item_id` | integer | Id yang diminta pada path (khusus GET) |
| `item` | object | Data mahasiswa hasil simpan/baca/ubah |
| `deleted_item` | object | Salinan data yang dihapus, dikembalikan agar bisa dicek atau diinput ulang |
| `detail` | string atau array | Pesan error; berupa string untuk 404/409 dan berupa array untuk 422 |

### Field objek `item`

| Field | Tipe | Makna |
|---|---|---|
| `nama` | string atau null | Nama mahasiswa |
| `alamat` | string atau null | Alamat mahasiswa |
| `ipk` | number atau null | IPK dalam bentuk desimal |
| `semester` | integer atau null | Semester berjalan |
| `hobi` | string atau null | Hobi mahasiswa |

Semua field bersifat opsional, sehingga request yang tidak mengirim suatu
field akan menyimpan `null` pada field tersebut.

### Field error `detail` (array 422)

| Field | Makna |
|---|---|
| `type` | Jenis kegagalan, misal `float_parsing`, `int_parsing` |
| `loc` | Lokasi data salah, `["body", "<nama_field>"]` berarti pada body request |
| `msg` | Penjelasan kegagalan dalam bahasa Inggris |
| `input` | Nilai asli yang dikirim pengguna |

---

## 7. Tabel Kode Status HTTP

| Kode | Nama | Kapan muncul | Pesan `detail` |
|---|---|---|---|
| 200 | OK | Operasi berhasil (create, read, update, delete) | Tidak ada, respons berisi `message` + `item` / `item_id` |
| 404 | Not Found | `item_id` tidak ada di database untuk GET, PUT, DELETE | `Item not found` |
| 409 | Conflict | POST dengan `item_id` yang sudah terdaftar | `Item already exists` |
| 422 | Unprocessable Entity | Tipe data body salah, atau `item_id` bukan angka | Array `detail` berisi `type`, `loc`, `msg`, `input` |

Contoh cepat membedakan status:

```bash
# 200 - id baru
curl -X POST "http://127.0.0.1:8000/items/1" -H "Content-Type: application/json" -d "{\"nama\":\"Budi\",\"ipk\":3.75}"
# 409 - id sama
curl -X POST "http://127.0.0.1:8000/items/1" -H "Content-Type: application/json" -d "{\"nama\":\"Budi\"}"
# 404 - id belum pernah ada
curl "http://127.0.0.1:8000/items/99"
# 422 - ipk bukan angka
curl -X POST "http://127.0.0.1:8000/items/2" -H "Content-Type: application/json" -d "{\"ipk\":\"bukan-angka\"}"
```

---

## 8. Penjelasan `/openapi.json`

`/openapi.json` adalah spesifikasi OpenAPI 3.1 berformat JSON yang menjadi
sumber data Swagger UI. Halaman `/docs` hanya membaca file ini lalu
merendernya.

### Bagian `info`

```json
{
  "title": "API Data Mahasiswa",
  "version": "2.0.0",
  "description": "CRUD data mahasiswa (nama, alamat, ipk, semester, hobi) dengan database in-memory. Status error: 404, 409, 422."
}
```

`info.title` menjadi judul halaman docs dan `info.description` menjadi
paragraf penjelasan singkat di bagian atas `/docs`. `info.version` tetap
ada di file JSON, tetapi stamp versi dan stamp OAS tidak ditampilkan di
`/docs` karena disembunyikan lewat CSS.

### Bagian `paths`

```json
{
  "paths": {
    "/items/{item_id}": ["post", "get", "put", "delete"]
  }
}
```

Hanya ada satu path dengan empat operasi. Inilah yang membuat `/docs`
menampilkan empat kartu operasi saja, sesuai batasan project.

### Bagian `components.schemas.Item`

```json
{
  "components": {
    "schemas": {
      "Item": {
        "type": "object",
        "title": "Item",
        "properties": {
          "nama": {"anyOf": [{"type": "string"}, {"type": "null"}]},
          "alamat": {"anyOf": [{"type": "string"}, {"type": "null"}]},
          "ipk": {"anyOf": [{"type": "number"}, {"type": "null"}]},
          "semester": {"anyOf": [{"type": "integer"}, {"type": "null"}]},
          "hobi": {"anyOf": [{"type": "string"}, {"type": "null"}]}
        }
      }
    }
  }
}
```

Schema `Item` berasal dari class Pydantic dan menjadi acuan:

- Menentukan isi form `Request body` pada `/docs`.
- Menentukan panel `Schemas` di bagian bawah `/docs`.
- Menentukan validasi yang menghasilkan error 422.
- Karena semua field punya opsi `null`, semua field tampil sebagai
  opsional di Swagger UI.

---

## 9. Alur Presentasi yang Disarankan

1. Tunjukkan struktur file dan sebutkan pembagian tanggung jawab:
   `main.py` untuk logika, `swagger_ui.py` untuk tampilan.
2. Jalankan server, buka `http://127.0.0.1:8000/docs`.
3. Jelaskan banner (judul + pill `Dokumentasi`) dan info `title` serta
   `description` yang dibuat singkat.
4. Jelaskan tabel warna method dan artinya (hijau baca, pink tulis,
   oranye ubah, merah hapus).
5. Buka endpoint POST, klik `Try it out`, isi body dengan data Budi
   Santoso, klik `Execute`. Perlihatkan `Request URL`, `Response Body`,
   dan `Response Code` 200.
6. Ulangi POST dengan id yang sama untuk memperlihatkan 409.
7. GET pada id yang sudah dibuat (200), lalu GET pada id yang tidak ada
   untuk memperlihatkan 404.
8. PUT untuk mengubah IPK, lalu PUT pada id kosong untuk 404.
9. Kirim `ipk` berupa teks untuk memperlihatkan 422 dan penjelasan
   `type`, `loc`, `msg`, `input`.
10. DELETE data, tampilkan `deleted_item`, lalu DELETE lagi untuk 404.
11. Buka `http://127.0.0.1:8000/openapi.json` dan hubungkan isi `info`,
    `paths`, dan `components.schemas.Item` dengan tampilan `/docs`.
12. Tutup dengan catatan teknis di bagian 10.

---

## 10. Catatan Teknis

| No | Catatan |
|---|---|
| 1 | Database in-memory berupa `dict` (`items_db`) dan **reset saat server restart** karena tidak ada penyimpanan ke disk. |
| 2 | Serialisasi memakai `item.model_dump()` (Pydantic v2), bukan `.dict()` yang sudah deprecated. |
| 3 | Desain CSS dan banner dipisah ke `swagger_ui.py`, sehingga `main.py` tetap bersih dari HTML/CSS. |
| 4 | `docs_url=None` mematikan route `/docs` bawaan FastAPI, lalu diganti route kustom lewat `app.add_route`. |
| 5 | Handler docs wajib menerima parameter `request: Request`, jika tidak muncul error `takes 0 positional arguments but 1 was given`. |
| 6 | Semua handler CRUD memakai `async def` karena seluruh operasi hanya memanipulasi dict (tanpa blocking I/O). |
| 7 | Error dibangkitkan dengan `HTTPException`, sehingga format respons otomatis `{"detail": "..."}` dengan status yang sesuai, bukan 200. |
| 8 | Field opsional bertipe `Optional[...]` membuat request parsial diperbolehkan; field yang tidak dikirim bernilai `null`. |
| 9 | Stamp versi (`2.0.0`) dan stamp OAS (`3.1.0`) disembunyikan dari `/docs` lewat CSS `.info .title span`, tetapi `version` tetap ada di `/openapi.json`. |
| 10 | Deskripsi API dibuat singkat (2 kalimat) agar halaman `/docs` ringkas dan mudah dibaca saat presentasi. |
| 9 | Tidak ada autentikasi, tidak ada database sungguhan, dan tidak ada endpoint selain empat operasi CRUD, sesuai batasan project. |
