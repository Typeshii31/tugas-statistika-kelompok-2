# 📖 Penjelasan Program — Kelompok 2 Statistika
## "Analisis Pengeluaran Bulanan dan Tren Berbelanja pada Marketplace Berbasis Statistik Deskriptif"

> Dokumen ini dibuat agar anggota kelompok mudah memahami program, membuat PPT, dan menjawab pertanyaan dosen saat presentasi.

---

## 1. Tujuan Program

Program ini bertujuan untuk **menganalisis data hasil kuesioner** tentang perilaku belanja mahasiswa di marketplace menggunakan pendekatan **Statistika Deskriptif**. Secara spesifik, program:

- Menghitung **distribusi frekuensi** (jumlah dan persentase) untuk setiap pertanyaan.
- Menentukan **modus** (nilai/kategori yang paling sering muncul) sebagai ukuran pemusatan data.
- Membuat **visualisasi data** berupa histogram, diagram batang, dan diagram lingkaran (pie chart).

---

## 2. Data yang Digunakan

| Aspek | Keterangan |
|-------|-----------|
| **Sumber** | Data primer — kuesioner Google Forms yang disebarkan ke mahasiswa |
| **Jumlah responden** | 52 orang |
| **File** | `KELOMPOK 2 STATISTIKA (Jawaban).xlsx` |
| **Sheet** | `Form Responses 1` |
| **Jumlah pertanyaan** | 5 pertanyaan |

### Daftar Pertanyaan dalam Kuesioner:

| No | Pertanyaan | Skala Data |
|----|-----------|-----------|
| 1 | Rata-rata pengeluaran bulanan di marketplace | **Ordinal** (interval kelas Rupiah) |
| 2 | Frekuensi transaksi dalam 1 bulan terakhir | **Ordinal** (interval kelas jumlah transaksi) |
| 3 | Platform marketplace yang digunakan | **Nominal** (multi-jawaban, boleh pilih lebih dari satu) |
| 4 | Kategori produk yang paling sering dibeli | **Nominal** (pilih satu) |
| 5 | Metode pembayaran yang paling sering digunakan | **Nominal** (pilih satu) |

> **Catatan penting untuk presentasi:** Semua data bersifat **kategorik** (bukan data numerik mentah). Oleh karena itu, ukuran pemusatan yang tepat adalah **modus** (bukan mean/rata-rata atau median).

---

## 3. Library / Pustaka Python yang Digunakan

| Library | Fungsi dalam Program |
|---------|---------------------|
| `pandas` | Membaca file Excel ke dalam DataFrame, menghitung frekuensi tiap kategori (`value_counts()`), mengurutkan data, dan melakukan manipulasi data (seperti `explode()` untuk memecah multi-jawaban). |
| `openpyxl` | Engine/backend yang digunakan oleh `pandas` untuk membaca file berformat `.xlsx`. |
| `matplotlib` | Membuat seluruh visualisasi grafik: histogram, diagram batang horizontal, dan pie chart. Grafik disimpan sebagai file gambar PNG. |
| `os` | Membuat folder `output_chart/` secara otomatis jika belum ada. |

---

## 4. Alur Kerja Program (Step-by-Step)

```
┌─────────────────────────────────┐
│  1. Baca data dari file Excel   │
│     (pandas + openpyxl)         │
└──────────────┬──────────────────┘
               ▼
┌─────────────────────────────────┐
│  2. Untuk setiap pertanyaan:    │
│     - Hitung distribusi         │
│       frekuensi (jumlah &       │
│       persentase)               │
│     - Tentukan modus            │
│     - Cetak tabel ke terminal   │
└──────────────┬──────────────────┘
               ▼
┌─────────────────────────────────┐
│  3. Buat visualisasi:           │
│     - Q1 & Q2 → Histogram      │
│     - Q3 → Diagram batang      │
│     - Q4 & Q5 → Diagram batang │
│       + Pie chart               │
└──────────────┬──────────────────┘
               ▼
┌─────────────────────────────────┐
│  4. Simpan semua grafik ke      │
│     folder output_chart/        │
│     dalam format PNG            │
└─────────────────────────────────┘
```

---

## 5. Penjelasan Detail per Pertanyaan

### Pertanyaan 1 — Pengeluaran Bulanan di Marketplace

- **Kelas interval yang digunakan:**
  - Rp0 – Rp100.000
  - Rp100.001 – Rp200.000
  - Rp200.001 – Rp300.000
  - Rp300.001 – Rp400.000
  - Rp400.001 – Rp500.000
  - Di atas Rp500.000

- **Visualisasi:** Histogram vertikal (batang saling menempel, tanpa celah).
- **Mengapa histogram?** Karena data berskala ordinal berupa kelas interval yang kontinu (batas atas kelas satu = batas bawah kelas berikutnya). Dalam statistika, **histogram digunakan untuk data kontinu/interval**, di mana batangnya saling menempel untuk menunjukkan kesinambungan data.
- **Output file:** `q1_histogram_pengeluaran.png`

---

### Pertanyaan 2 — Frekuensi Transaksi dalam 1 Bulan Terakhir

- **Kelas interval yang digunakan:**
  - 0 – 2 kali
  - 3 – 5 kali
  - 6 – 8 kali
  - 9 – 11 kali
  - 12 kali atau lebih

- **Visualisasi:** Histogram vertikal (batang saling menempel).
- **Alasan sama dengan Q1:** data berupa kelas interval.
- **Output file:** `q2_histogram_frekuensi.png`

---

### Pertanyaan 3 — Platform Marketplace yang Digunakan

- **Cara pengolahan khusus:** Pertanyaan ini **boleh dijawab lebih dari satu** (multi-jawaban). Contoh: seorang responden bisa menjawab "Shopee, Tokopedia, TikTok Shop".
- **Teknik pemrosesan:** Program memecah (split) jawaban yang dipisahkan koma menjadi jawaban individual, lalu menghitung frekuensi masing-masing platform.
- **Konsekuensi:** Total frekuensi bisa **lebih dari 52** (karena satu responden bisa menyumbang lebih dari 1 jawaban).
- **Visualisasi:** Diagram batang horizontal (diurutkan dari yang terbanyak).
- **Mengapa diagram batang (bukan histogram)?** Karena data berskala **nominal** (nama platform = kategori tanpa urutan bawaan). Dalam statistika, **diagram batang (bar chart) digunakan untuk data nominal/kategorik**, dan batangnya **ada celah** untuk menunjukkan bahwa kategori-kategori tersebut saling terpisah.
- **Output file:** `q3_diagram_batang_platform.png`

---

### Pertanyaan 4 — Kategori Produk yang Paling Sering Dibeli

- **Visualisasi 1:** Diagram batang horizontal (urut dari terbanyak).
- **Visualisasi 2:** Pie chart (diagram lingkaran) — menunjukkan proporsi/persentase setiap kategori.
- **Mengapa ada pie chart?** Pie chart efektif untuk menunjukkan **komposisi/proporsi** dari keseluruhan. Cocok karena setiap responden hanya memilih satu jawaban, sehingga totalnya = 100%.
- **Output file:**
  - `q4_diagram_batang_kategori.png`
  - `q4_pie_chart_kategori.png`

---

### Pertanyaan 5 — Metode Pembayaran yang Paling Sering Digunakan

- **Visualisasi 1:** Diagram batang horizontal (urut dari terbanyak).
- **Visualisasi 2:** Pie chart (diagram lingkaran).
- **Output file:**
  - `q5_diagram_batang_pembayaran.png`
  - `q5_pie_chart_pembayaran.png`

---

## 6. Konsep Statistika yang Digunakan

### a. Distribusi Frekuensi
Tabel yang menyajikan **berapa kali** (frekuensi) setiap kategori/kelas muncul dalam data. Program juga menghitung **persentase** setiap kategori terhadap total.

**Rumus persentase:**

$$\text{Persentase} = \frac{\text{Frekuensi kategori}}{\text{Total responden}} \times 100\%$$

### b. Modus
**Modus** adalah nilai/kategori yang **paling sering muncul** (frekuensi tertinggi). Modus merupakan ukuran pemusatan yang tepat untuk **data kategorik/nominal** karena:
- Data kategorik tidak bisa dijumlahkan atau dirata-ratakan (contoh: tidak bisa merata-ratakan "Shopee" dan "Tokopedia").
- Mean (rata-rata) hanya cocok untuk data numerik rasio/interval.
- Median hanya cocok untuk data yang bisa diurutkan (ordinal ke atas).

### c. Histogram vs Diagram Batang (Bar Chart)

| Aspek | Histogram | Diagram Batang |
|-------|-----------|---------------|
| **Jenis data** | Data kontinu / kelas interval | Data kategorik / nominal |
| **Celah antar batang** | **Tidak ada** (batang menempel) | **Ada celah** antar batang |
| **Sumbu-x** | Kelas interval berurutan | Kategori (tanpa urutan bawaan) |
| **Digunakan untuk** | Q1 (pengeluaran), Q2 (frekuensi transaksi) | Q3 (platform), Q4 (kategori produk), Q5 (metode pembayaran) |

### d. Pie Chart (Diagram Lingkaran)
Menunjukkan **proporsi/komposisi** setiap kategori dari keseluruhan data. Setiap "irisan" mewakili persentase kategori tersebut. Digunakan untuk Q4 dan Q5 karena setiap responden hanya memilih satu jawaban.

---

## 7. Penjelasan Kode Program (Ringkas)

### Bagian Import & Konfigurasi (Baris 1–27)
```python
import pandas as pd          # untuk membaca & mengolah data
import matplotlib.pyplot as plt  # untuk membuat grafik
matplotlib.use("Agg")        # mode tanpa GUI (grafik langsung disimpan, tidak ditampilkan di layar)
```
- `matplotlib.use("Agg")` → supaya program bisa jalan di terminal tanpa perlu menampilkan jendela grafik.

### Bagian Membaca Data (Baris 29–39)
```python
df = pd.read_excel(FILE_EXCEL, sheet_name=SHEET_NAME, engine="openpyxl")
```
- Membaca file Excel ke dalam **DataFrame** (tabel data di Python).
- `engine="openpyxl"` → memberitahu pandas untuk pakai library openpyxl sebagai pembaca file `.xlsx`.

### Fungsi `cetak_distribusi()` (Baris 43–64)
- Menerima data frekuensi → mencetak tabel distribusi frekuensi ke terminal.
- Menghitung persentase setiap kategori.
- Menentukan dan menampilkan **modus**.

### Fungsi `buat_histogram()` (Baris 68–120)
- Membuat histogram vertikal dengan `width=1.0` (batang menempel tanpa celah).
- Menambahkan label angka di atas setiap batang.
- Menyimpan grafik ke file PNG.

### Fungsi `buat_bar_chart()` (Baris 124–160)
- Membuat diagram batang horizontal (`barh`).
- Horizontal supaya label kategori yang panjang tetap terbaca jelas.
- Diurutkan dari frekuensi terbanyak.

### Fungsi `buat_pie_chart()` (Baris 164–208)
- Membuat diagram lingkaran dengan legend di samping.
- Menampilkan angka frekuensi di dalam irisan dan persentase di legend.

### Bagian Pengolahan Q1–Q5 (Baris 211–341)
- Setiap pertanyaan: hitung frekuensi → cetak tabel → buat visualisasi.
- Q1 & Q2: data di-*reindex* sesuai urutan kelas interval yang logis (bukan urutan alfabet).
- Q3: jawaban di-*split* koma → `explode()` → dihitung per platform.

---

## 8. Output Program

### Di Terminal:
- 5 tabel distribusi frekuensi (masing-masing menampilkan kategori, frekuensi, persentase, dan modus).

### File Grafik (di folder `output_chart/`):

| No | File | Jenis Grafik |
|----|------|-------------|
| 1 | `q1_histogram_pengeluaran.png` | Histogram vertikal |
| 2 | `q2_histogram_frekuensi.png` | Histogram vertikal |
| 3 | `q3_diagram_batang_platform.png` | Diagram batang horizontal |
| 4 | `q4_diagram_batang_kategori.png` | Diagram batang horizontal |
| 5 | `q4_pie_chart_kategori.png` | Diagram lingkaran |
| 6 | `q5_diagram_batang_pembayaran.png` | Diagram batang horizontal |
| 7 | `q5_pie_chart_pembayaran.png` | Diagram lingkaran |

> **Total: 7 file grafik** yang otomatis terbuat saat program dijalankan.

---

## 9. Pertanyaan yang Mungkin Ditanya Dosen & Jawabannya

### ❓ "Kenapa pakai histogram untuk Q1 dan Q2, tapi bar chart untuk Q3–Q5?"
> **Jawaban:** Karena Q1 dan Q2 datanya berupa **kelas interval** (data kontinu yang sudah dikelompokkan), sehingga menurut teori statistika harus divisualisasikan dengan **histogram** (batang menempel tanpa celah). Sedangkan Q3–Q5 datanya bersifat **nominal/kategorik** (nama platform, kategori produk, metode pembayaran), sehingga menggunakan **diagram batang** (ada celah antar batang).

### ❓ "Kenapa ukuran pemusatannya pakai modus, bukan mean atau median?"
> **Jawaban:** Karena seluruh data kami bersifat **kategorik** (nominal dan ordinal berupa kelas interval). **Mean (rata-rata)** hanya bisa digunakan untuk data numerik berskala rasio atau interval. **Median** membutuhkan data yang bisa diurutkan secara numerik. Untuk data kategorik, satu-satunya ukuran pemusatan yang tepat adalah **modus**, yaitu kategori yang paling sering muncul.

### ❓ "Kenapa total frekuensi di Q3 bisa lebih dari 52?"
> **Jawaban:** Karena pada pertanyaan tentang platform marketplace, responden **boleh memilih lebih dari satu jawaban** (multi-jawaban). Misalnya satu responden bisa menjawab "Shopee, Tokopedia, TikTok Shop" — ini dihitung sebagai 3 respon terpisah. Sehingga total respon bisa lebih dari jumlah responden (52 orang).

### ❓ "Data ini data primer atau sekunder?"
> **Jawaban:** **Data primer**, karena kami mengumpulkan sendiri data ini melalui **kuesioner Google Forms** yang disebarkan langsung kepada mahasiswa.

### ❓ "Kenapa pakai pie chart untuk Q4 dan Q5 tapi tidak untuk Q3?"
> **Jawaban:** Pie chart menunjukkan **komposisi dari keseluruhan (100%)**. Pada Q4 dan Q5, setiap responden hanya memilih satu jawaban, sehingga total = 52 responden = 100%. Pada Q3, karena responden bisa memilih lebih dari satu, totalnya melebihi 52 — sehingga pie chart tidak tepat karena tidak merepresentasikan 100% dari satu keseluruhan.

### ❓ "Apa bedanya `value_counts()` dengan cara hitung manual?"
> **Jawaban:** `value_counts()` adalah fungsi bawaan dari library pandas yang secara otomatis menghitung berapa kali setiap nilai unik muncul dalam kolom data. Hasilnya sama persis dengan menghitung frekuensi secara manual (tally), tetapi lebih efisien dan cepat karena dilakukan oleh komputer.

### ❓ "Library apa saja yang dipakai dan kenapa?"
> **Jawaban:**
> - **pandas**: library standar Python untuk analisis data, digunakan untuk membaca file Excel dan menghitung distribusi frekuensi.
> - **openpyxl**: engine pembaca file Excel berformat `.xlsx`, dibutuhkan oleh pandas.
> - **matplotlib**: library standar Python untuk membuat visualisasi grafik (histogram, diagram batang, pie chart).
> Ketiga library ini adalah yang paling umum dan standar digunakan dalam analisis data dengan Python.

### ❓ "Kenapa grafik disimpan sebagai file PNG, bukan ditampilkan langsung?"
> **Jawaban:** Supaya grafik bisa langsung dipakai di PPT presentasi dan laporan tanpa perlu screenshot. File PNG juga bisa dibuka di mana saja tanpa perlu menjalankan ulang program.

### ❓ "Apakah ada ukuran penyebaran yang dihitung?"
> **Jawaban:** Untuk data kategorik/nominal, ukuran penyebaran seperti standar deviasi atau varians tidak bisa diterapkan karena data tidak bersifat numerik. Yang bisa dilihat adalah **sebaran frekuensi** dari distribusi frekuensi — apakah data terpusat di satu kategori atau tersebar merata di banyak kategori.

---

## 10. Tips untuk Presentasi

1. **Slide pembuka:** Judul, nama kelompok, mata kuliah.
2. **Slide latar belakang:** Jelaskan mengapa topik marketplace dipilih (relevan dengan kehidupan mahasiswa).
3. **Slide metodologi:** Data primer via Google Forms, 52 responden, 5 pertanyaan.
4. **Slide per pertanyaan (5 slide):** Tampilkan grafik + tabel frekuensi + modus + interpretasi singkat.
5. **Slide kesimpulan:** Rangkum temuan utama dari kelima pertanyaan.
6. **Slide demo program (opsional):** Tunjukkan program dijalankan di terminal → tabel muncul + file grafik terbuat.

### Contoh Interpretasi untuk Slide:
- *"Berdasarkan histogram, modus pengeluaran bulanan mahasiswa di marketplace berada pada kelas [kategori tertinggi], yang menunjukkan bahwa sebagian besar mahasiswa menghabiskan [rentang] per bulan untuk berbelanja online."*
- *"Dari diagram batang, platform yang paling banyak digunakan adalah [platform tertinggi], diikuti oleh [platform kedua]."*
