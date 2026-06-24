# 📊 Analisis Statistika Deskriptif — Kelompok 2
## Perilaku Belanja Mahasiswa di Marketplace

Program Python untuk menganalisis hasil kuesioner perilaku belanja mahasiswa di marketplace menggunakan metode **Statistika Deskriptif** (Distribusi Frekuensi & Visualisasi Data).

---

## 📁 Struktur File

```
tugas-statistika-kelompok-2/
├── analisis_marketplace.py          # Script utama program analisis
├── KELOMPOK 2 STATISTIKA (Jawaban).xlsx  # Data hasil kuesioner (52 responden)
├── requirements.txt                 # Daftar library Python yang dibutuhkan
├── .gitignore                       # File pengecualian Git
└── README.md                        # Panduan ini
```

---

## 🔍 Deskripsi Program

Program ini membaca data dari file Excel hasil kuesioner Google Forms dan melakukan analisis untuk **5 pertanyaan**:

| No | Pertanyaan | Jenis Visualisasi |
|----|-----------|-------------------|
| 1 | Rata-rata pengeluaran bulanan di marketplace (Rupiah) | Bar Chart (urut kelas interval) |
| 2 | Frekuensi transaksi dalam 1 bulan terakhir | Bar Chart (urut kelas interval) |
| 3 | Platform marketplace yang digunakan *(multi-jawaban)* | Bar Chart (urut terbanyak) |
| 4 | Kategori produk yang paling sering dibeli | Bar Chart (urut terbanyak) |
| 5 | Metode pembayaran yang paling sering digunakan | Bar Chart (urut terbanyak) |

---

## ⚙️ Cara Menjalankan Program

### 1. Pastikan Python sudah terinstall
Download Python di [python.org](https://python.org) jika belum ada. Saat install, **centang** opsi `Add Python to PATH`.

### 2. Install library yang dibutuhkan
Buka terminal/CMD di folder ini, lalu jalankan:
```bash
pip install -r requirements.txt
```

### 3. Jalankan program
```bash
python analisis_marketplace.py
```

### 4. Cek hasilnya
- **Terminal**: Tabel distribusi frekuensi (jumlah & persentase) untuk setiap pertanyaan.
- **Folder `output_chart/`**: 5 file grafik PNG yang otomatis terbuat.

---

## 📦 Library yang Digunakan

| Library | Fungsi |
|---------|--------|
| `pandas` | Membaca data Excel & menghitung distribusi frekuensi |
| `openpyxl` | Engine untuk membaca file `.xlsx` |
| `matplotlib` | Membuat visualisasi grafik/chart |

---

## 👥 Kelompok 2 — Mata Kuliah Statistika
