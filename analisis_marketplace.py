# =============================================================================
# analisis_marketplace.py
# Program Analisis Statistika Deskriptif – Kelompok 2
# Topik: Analisis Pengeluaran Bulanan dan Tren Berbelanja pada Marketplace
#        Berbasis Statistik Deskriptif
# =============================================================================
# Library yang digunakan:
#   - pandas    : membaca data Excel & menghitung distribusi frekuensi
#   - matplotlib: membuat visualisasi (histogram, diagram batang, pie chart)
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

    # Cari modus (kategori dengan frekuensi tertinggi)
    modus = freq_series.idxmax()
    frek_modus = freq_series.max()

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
    # Tampilkan modus (ukuran pemusatan untuk data kategorik)
    print(f"  >> Modus: {modus} ({frek_modus} responden)")
    print()


# ── Fungsi bantu: buat histogram vertikal (untuk data kelas interval) ────────
def buat_histogram(freq_series, judul, xlabel, ylabel, nama_file, warna="steelblue"):
    """
    Membuat histogram vertikal (batang rapat tanpa celah) untuk data
    berskala interval/ordinal, lalu menyimpannya sebagai PNG.
    Sesuai teori statistika: histogram = batang saling menempel.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    # Label sumbu-x diperpendek agar tidak terpotong
    labels_pendek = []
    for label in freq_series.index.astype(str):
        # Ganti "Rp" prefix dan format agar lebih ringkas di sumbu-x
        labels_pendek.append(label)

    x_pos = range(len(freq_series))

    # Plot bar vertikal TANPA celah (width=1.0) → ciri khas histogram
    bars = ax.bar(
        x_pos,
        freq_series.values,
        width=1.0,          # lebar penuh tanpa celah (ciri histogram)
        color=warna,
        edgecolor="white",
        linewidth=0.8,
        align="center",
    )

    # Tambahkan label nilai di atas setiap batang
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.3,
            f"{int(height)}",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
        )

    ax.set_xticks(x_pos)
    ax.set_xticklabels(labels_pendek, rotation=20, ha="right", fontsize=9)
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.set_title(judul, fontsize=13, fontweight="bold", pad=12)
    ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    plt.tight_layout()

    # Simpan ke file PNG
    path = os.path.join(OUTPUT_DIR, nama_file)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    print(f"   [OK] Chart disimpan: {path}")
    plt.close(fig)


# ── Fungsi bantu: buat diagram batang horizontal (untuk data nominal) ────────
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


# ── Fungsi bantu: buat pie chart (diagram lingkaran) ─────────────────────────
def buat_pie_chart(freq_series, judul, nama_file, warna_map=None):
    """Membuat pie chart (diagram lingkaran) dan menyimpannya sebagai PNG."""
    fig, ax = plt.subplots(figsize=(8, 8))

    # Warna otomatis jika tidak ditentukan
    if warna_map is None:
        warna_map = plt.cm.Set2.colors

    # Format label: kategori + persentase
    total = freq_series.sum()
    labels = [f"{k}\n({v/total*100:.1f}%)" for k, v in freq_series.items()]

    wedges, texts, autotexts = ax.pie(
        freq_series.values,
        labels=None,
        autopct=lambda pct: f"{int(round(pct * total / 100))}",
        colors=warna_map[:len(freq_series)],
        startangle=90,
        pctdistance=0.75,
        wedgeprops={"edgecolor": "white", "linewidth": 1.5},
    )

    # Perbesar font angka di dalam pie
    for autotext in autotexts:
        autotext.set_fontsize(10)
        autotext.set_fontweight("bold")

    # Legend di samping agar label tidak bertumpuk
    ax.legend(
        wedges,
        labels,
        title="Kategori",
        loc="center left",
        bbox_to_anchor=(1.0, 0.5),
        fontsize=9,
    )

    ax.set_title(judul, fontsize=13, fontweight="bold", pad=20)
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

# Visualisasi: HISTOGRAM vertikal (batang rapat, sesuai teori statistika
# karena data berupa kelas interval)
buat_histogram(
    freq_q1,
    judul="Histogram Pengeluaran Bulanan di Marketplace",
    xlabel="Rentang Pengeluaran (Rupiah)",
    ylabel="Frekuensi (Jumlah Responden)",
    nama_file="q1_histogram_pengeluaran.png",
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

# Visualisasi: HISTOGRAM vertikal (batang rapat, data kelas interval)
buat_histogram(
    freq_q2,
    judul="Histogram Frekuensi Transaksi di Marketplace",
    xlabel="Rentang Frekuensi Transaksi",
    ylabel="Frekuensi (Jumlah Responden)",
    nama_file="q2_histogram_frekuensi.png",
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

# Visualisasi: Diagram batang horizontal (data nominal, urut terbanyak)
buat_bar_chart(
    freq_q3,
    judul="Platform Marketplace yang Paling Sering Digunakan\n(responden boleh memilih lebih dari satu)",
    xlabel="Platform",
    ylabel="Jumlah Respon",
    nama_file="q3_diagram_batang_platform.png",
    warna="#e15759",
)

# =============================================================================
# PERTANYAAN 4: Kategori Produk yang Paling Sering Dibeli
# =============================================================================
# Diurutkan dari yang paling banyak ke paling sedikit
freq_q4 = df[q4_col].value_counts().sort_values(ascending=False)

cetak_distribusi("Kategori Produk yang Paling Sering Dibeli", freq_q4, 4)

# Visualisasi 1: Diagram batang horizontal
buat_bar_chart(
    freq_q4,
    judul="Diagram Batang Kategori Produk yang Paling Sering Dibeli",
    xlabel="Kategori Produk",
    ylabel="Jumlah Responden",
    nama_file="q4_diagram_batang_kategori.png",
    warna="#f28e2b",
)

# Visualisasi 2: Pie chart (diagram lingkaran)
buat_pie_chart(
    freq_q4,
    judul="Diagram Lingkaran Kategori Produk\nyang Paling Sering Dibeli",
    nama_file="q4_pie_chart_kategori.png",
)

# =============================================================================
# PERTANYAAN 5: Metode Pembayaran yang Paling Sering Digunakan
# =============================================================================
# Diurutkan dari yang paling banyak ke paling sedikit
freq_q5 = df[q5_col].value_counts().sort_values(ascending=False)

cetak_distribusi("Metode Pembayaran yang Paling Sering Digunakan", freq_q5, 5)

# Visualisasi 1: Diagram batang horizontal
buat_bar_chart(
    freq_q5,
    judul="Diagram Batang Metode Pembayaran yang Paling Sering Digunakan",
    xlabel="Metode Pembayaran",
    ylabel="Jumlah Responden",
    nama_file="q5_diagram_batang_pembayaran.png",
    warna="#76b7b2",
)

# Visualisasi 2: Pie chart (diagram lingkaran)
buat_pie_chart(
    freq_q5,
    judul="Diagram Lingkaran Metode Pembayaran\nyang Paling Sering Digunakan",
    nama_file="q5_pie_chart_pembayaran.png",
)

# ── Ringkasan akhir ─────────────────────────────────────────────────────────
print("\n" + "=" * 72)
print("SELESAI! Semua chart tersimpan di folder:", OUTPUT_DIR)
print("=" * 72)
