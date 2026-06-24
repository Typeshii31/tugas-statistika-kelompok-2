# =============================================================================
# analisis_marketplace.py
# Program Analisis Statistika Deskriptif – Kelompok 2
# Topik: Perilaku Belanja Mahasiswa di Marketplace
# =============================================================================
# Library yang digunakan:
#   - pandas    : membaca data Excel & menghitung distribusi frekuensi
#   - matplotlib: membuat visualisasi (diagram batang)
#   - openpyxl  : engine untuk membaca file .xlsx
#   - os        : membuat folder output
# =============================================================================

import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # backend non-interaktif, agar bisa jalan di terminal tanpa GUI
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ── Konfigurasi umum ─────────────────────────────────────────────────────────
FILE_EXCEL = "KELOMPOK 2 STATISTIKA (Jawaban).xlsx"
SHEET_NAME = "Form Responses 1"
OUTPUT_DIR = "output_chart"

# Buat folder output jika belum ada
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Membaca data dari file Excel ─────────────────────────────────────────────
df = pd.read_excel(FILE_EXCEL, sheet_name=SHEET_NAME, engine="openpyxl")
print(f"Data berhasil dimuat: {df.shape[0]} responden, {df.shape[1]} kolom.\n")

# Ambil nama-nama kolom pertanyaan (kolom ke-1 sampai ke-5, index 1–5)
kolom = df.columns.tolist()
q1_col = kolom[1]  # Pengeluaran bulanan (rentang nominal Rupiah)
q2_col = kolom[2]  # Frekuensi transaksi (rentang kali)
q3_col = kolom[3]  # Platform marketplace (multi-jawaban, dipisah koma)
q4_col = kolom[4]  # Kategori produk
q5_col = kolom[5]  # Metode pembayaran


# ── Fungsi bantu: cetak distribusi frekuensi ke terminal ─────────────────────
def cetak_distribusi(nama_pertanyaan, freq_series, nomor):
    """Mencetak tabel distribusi frekuensi (jumlah & persentase) ke terminal."""
    total = freq_series.sum()
    print("=" * 72)
    print(f"PERTANYAAN {nomor}: {nama_pertanyaan}")
    print("=" * 72)
    print(f"{'Kategori':<45} {'Frekuensi':>9} {'Persentase':>10}")
    print("-" * 72)
    for kategori, jumlah in freq_series.items():
        persen = jumlah / total * 100
        print(f"{kategori:<45} {jumlah:>9} {persen:>9.1f}%")
    print("-" * 72)
    print(f"{'TOTAL':<45} {total:>9} {'100.0%':>10}")
    print()


# ── Fungsi bantu: buat & simpan diagram batang ───────────────────────────────
def buat_bar_chart(freq_series, judul, xlabel, ylabel, nama_file, warna="steelblue"):
    """Membuat bar chart horizontal dan menyimpannya sebagai PNG."""
    fig, ax = plt.subplots(figsize=(10, max(4, len(freq_series) * 0.6)))

    # Plot horizontal bar chart (barh) agar label kategori terbaca jelas
    bars = ax.barh(
        freq_series.index.astype(str),
        freq_series.values,
        color=warna,
        edgecolor="white",
        linewidth=0.5,
    )

    # Tambahkan label nilai di ujung setiap batang
    for bar in bars:
        width = bar.get_width()
        ax.text(
            width + 0.3,
            bar.get_y() + bar.get_height() / 2,
            f"{int(width)}",
            va="center",
            fontsize=9,
            fontweight="bold",
        )

    ax.set_xlabel(ylabel, fontsize=11)  # sumbu-x = frekuensi (karena barh)
    ax.set_ylabel(xlabel, fontsize=11)
    ax.set_title(judul, fontsize=13, fontweight="bold", pad=12)
    ax.invert_yaxis()  # kategori pertama di atas
    ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    plt.tight_layout()

    # Simpan ke file PNG
    path = os.path.join(OUTPUT_DIR, nama_file)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    print(f"   [OK] Chart disimpan: {path}")
    plt.close(fig)


# =============================================================================
# PERTANYAAN 1: Rata-rata Pengeluaran Bulanan di Marketplace (Rentang Rupiah)
# =============================================================================
# Urutan kelas interval yang logis (dari kecil ke besar)
urutan_pengeluaran = [
    "Rp0 \u2013 Rp100.000",
    "Rp100.001 \u2013 Rp200.000",
    "Rp200.001 \u2013 Rp300.000",
    "Rp300.001 \u2013 Rp400.000",
    "Rp400.001 \u2013 Rp500.000",
    "Di atas Rp500.000",
]

# Hitung frekuensi dan urutkan sesuai kelas interval
freq_q1 = df[q1_col].value_counts()
freq_q1 = freq_q1.reindex(urutan_pengeluaran).fillna(0).astype(int)

cetak_distribusi("Rata-rata Pengeluaran Bulanan di Marketplace", freq_q1, 1)
buat_bar_chart(
    freq_q1,
    judul="Distribusi Pengeluaran Bulanan di Marketplace",
    xlabel="Rentang Pengeluaran",
    ylabel="Jumlah Responden",
    nama_file="q1_pengeluaran.png",
    warna="#4e79a7",
)

# =============================================================================
# PERTANYAAN 2: Frekuensi Transaksi dalam 1 Bulan Terakhir
# =============================================================================
# Urutan kelas interval yang logis (dari sedikit ke banyak)
urutan_frekuensi = [
    "0 \u2013 2 kali",
    "3 \u2013 5 kali",
    "6 \u2013 8 kali",
    "9 \u2013 11 kali",
    "12 kali atau lebih",
]

freq_q2 = df[q2_col].value_counts()
freq_q2 = freq_q2.reindex(urutan_frekuensi).fillna(0).astype(int)

cetak_distribusi("Frekuensi Transaksi dalam 1 Bulan Terakhir", freq_q2, 2)
buat_bar_chart(
    freq_q2,
    judul="Distribusi Frekuensi Transaksi di Marketplace",
    xlabel="Rentang Frekuensi Transaksi",
    ylabel="Jumlah Responden",
    nama_file="q2_frekuensi_transaksi.png",
    warna="#59a14f",
)

# =============================================================================
# PERTANYAAN 3: Platform Marketplace yang Digunakan (Multi-Jawaban)
# =============================================================================
# Pecah jawaban yang dipisah koma, lalu hitung frekuensi masing-masing platform
semua_platform = (
    df[q3_col]
    .dropna()                          # buang jika ada NaN
    .str.split(",")                    # pecah berdasarkan koma
    .explode()                         # satu baris per platform
    .str.strip()                       # hapus spasi di awal/akhir
)
freq_q3 = semua_platform.value_counts().sort_values(ascending=False)

cetak_distribusi("Platform Marketplace yang Digunakan", freq_q3, 3)
buat_bar_chart(
    freq_q3,
    judul="Platform Marketplace yang Paling Sering Digunakan\n(responden boleh memilih lebih dari satu)",
    xlabel="Platform",
    ylabel="Jumlah Respon",
    nama_file="q3_platform.png",
    warna="#e15759",
)

# =============================================================================
# PERTANYAAN 4: Kategori Produk yang Paling Sering Dibeli
# =============================================================================
# Diurutkan dari yang paling banyak ke paling sedikit
freq_q4 = df[q4_col].value_counts().sort_values(ascending=False)

cetak_distribusi("Kategori Produk yang Paling Sering Dibeli", freq_q4, 4)
buat_bar_chart(
    freq_q4,
    judul="Kategori Produk yang Paling Sering Dibeli di Marketplace",
    xlabel="Kategori Produk",
    ylabel="Jumlah Responden",
    nama_file="q4_kategori_produk.png",
    warna="#f28e2b",
)

# =============================================================================
# PERTANYAAN 5: Metode Pembayaran yang Paling Sering Digunakan
# =============================================================================
# Diurutkan dari yang paling banyak ke paling sedikit
freq_q5 = df[q5_col].value_counts().sort_values(ascending=False)

cetak_distribusi("Metode Pembayaran yang Paling Sering Digunakan", freq_q5, 5)
buat_bar_chart(
    freq_q5,
    judul="Metode Pembayaran yang Paling Sering Digunakan",
    xlabel="Metode Pembayaran",
    ylabel="Jumlah Responden",
    nama_file="q5_metode_pembayaran.png",
    warna="#76b7b2",
)

# ── Ringkasan akhir ─────────────────────────────────────────────────────────
print("\n" + "=" * 72)
print("SELESAI! Semua chart tersimpan di folder:", OUTPUT_DIR)
print("=" * 72)
