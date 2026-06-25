# =============================================================================
# analisis_marketplace.py
# Program Analisis Statistika Deskriptif – Kelompok 2
# Topik: Analisis Pengeluaran Bulanan dan Tren Berbelanja pada Marketplace
#        Berbasis Statistik Deskriptif (Versi Visualisasi & Dashboard Seaborn)
# =============================================================================

import os
import platform
import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# ── Konfigurasi Folder & File ────────────────────────────────────────────────
FILE_EXCEL = "KELOMPOK 2 STATISTIKA (Jawaban).xlsx"
SHEET_NAME = "Form Responses 1"
OUTPUT_DIR = "output_chart"

# Buat folder output jika belum ada (agar root directory tetap bersih)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── 0. Membaca Data dari File Excel ──────────────────────────────────────────
try:
    df = pd.read_excel(FILE_EXCEL, sheet_name=SHEET_NAME, engine="openpyxl")
except FileNotFoundError:
    print(f"Error: File '{FILE_EXCEL}' tidak ditemukan. Pastikan file berada di folder yang sama.")
    exit()
except Exception as e:
    print(f"Error saat membaca file Excel: {e}")
    exit()

# Rename kolom berdasarkan posisi indeks agar konsisten
mapping_kolom = {
    df.columns[0]: 'Timestamp',
    df.columns[1]: 'Nominal_Pengeluaran',
    df.columns[2]: 'Frekuensi_Checkout',
    df.columns[3]: 'Platform_Marketplace',
    df.columns[4]: 'Kategori_Produk',
    df.columns[5]: 'Metode_Pembayaran'
}
df = df.rename(columns=mapping_kolom)

# Bersihkan spasi liar pada semua kolom kecuali Timestamp
for col in df.columns:
    if col != 'Timestamp':
        df[col] = df[col].astype(str).str.strip()

N = len(df)
print(f"=== BERHASIL MEMBACA DATA: Total {N} Responden ===\n")

# ── Konfigurasi Tema & Gaya Visualisasi (Seaborn) ───────────────────────────
sns.set_theme(style="whitegrid", font="DejaVu Sans")
BLUES  = sns.color_palette("Blues_r", 6)
PASTEL = sns.color_palette("pastel", 10)

# =============================================================================
# 1. STATISTIK DESKRIPTIF – Q1 NOMINAL PENGELUARAN
# =============================================================================
urutan_pengeluaran = [
    'Rp0 \u2013 Rp100.000',
    'Rp100.001 \u2013 Rp200.000',
    'Rp200.001 \u2013 Rp300.000',
    'Rp300.001 \u2013 Rp400.000',
    'Rp400.001 \u2013 Rp500.000',
    'Di atas Rp500.000'
]

# Hitung frekuensi dan reindex agar urutannya logis
freq_p = (df['Nominal_Pengeluaran'].value_counts()
          .reindex(urutan_pengeluaran).fillna(0).reset_index())
freq_p.columns = ['Interval Pengeluaran', 'Frekuensi (f)']
freq_p['Frekuensi Kumulatif (fk)'] = freq_p['Frekuensi (f)'].cumsum()
freq_p['Persentase (%)'] = freq_p['Frekuensi (f)'] / N * 100

print("1. TABEL DISTRIBUSI FREKUENSI NOMINAL PENGELUARAN (Q1):")
print(freq_p.to_string(index=False))
print("-" * 72)

modus_pengeluaran = df['Nominal_Pengeluaran'].mode()[0]
print(f"Modus Pengeluaran Terbanyak: {modus_pengeluaran}")
print("-" * 72 + "\n")

# =============================================================================
# 2. STATISTIK DESKRIPTIF – Q2 FREKUENSI CHECKOUT
# =============================================================================
urutan_freq = [
    '0 \u2013 2 kali',
    '3 \u2013 5 kali',
    '6 \u2013 8 kali',
    '9 \u2013 11 kali',
    '12 kali atau lebih'
]

freq_c = (df['Frekuensi_Checkout'].value_counts()
          .reindex(urutan_freq).fillna(0).reset_index())
freq_c.columns = ['Interval Frekuensi', 'Frekuensi (f)']
freq_c['Frekuensi Kumulatif (fk)'] = freq_c['Frekuensi (f)'].cumsum()
freq_c['Persentase (%)'] = freq_c['Frekuensi (f)'] / N * 100

print("2. TABEL DISTRIBUSI FREKUENSI CHECKOUT (Q2):")
print(freq_c.to_string(index=False))
print("-" * 72)

modus_checkout = df['Frekuensi_Checkout'].mode()[0]
print(f"Modus Frekuensi Checkout: {modus_checkout}")
print("-" * 72 + "\n")

# =============================================================================
# 3. STATISTIK DESKRIPTIF – Q3 PLATFORM MARKETPLACE (Multi-pilihan)
# =============================================================================
PLATFORM_MAP = {
    'shopee'     : 'Shopee',
    'tokopedia'  : 'Tokopedia',
    'tiktok shop': 'TikTok Shop',
    'lazada'     : 'Lazada',
    'blibli'     : 'Blibli',
    'gojek'      : 'Gojek',
    'gopay'      : 'Gopay',
    'facebook'   : 'Facebook',
    'astro'      : 'Astro'
}

platform_list = []
# Gunakan dropna() dan pastikan data bertipe string sebelum memecah koma
for row in df['Platform_Marketplace'].dropna():
    for part in str(row).split(','):
        p = part.strip().lower()
        matched = False
        for key, label in PLATFORM_MAP.items():
            if key in p:
                platform_list.append(label)
                matched = True
                break
        if not matched and p != 'nan' and p != '':
            platform_list.append(part.strip().title())

plat_count = Counter(platform_list)
plat_df = pd.DataFrame(plat_count.most_common(), columns=['Platform', 'Frekuensi'])
plat_df['Persentase (%)'] = plat_df['Frekuensi'] / N * 100

print("3. TABEL DISTRIBUSI PLATFORM MARKETPLACE (Q3 – Multi-pilihan):")
print(plat_df.to_string(index=False))
print("-" * 72)
print(f"Catatan: Total responden memilih {len(platform_list)} platform (karena multi-pilihan).")
print("-" * 72 + "\n")

# =============================================================================
# 4. STATISTIK DESKRIPTIF – Q4 KATEGORI PRODUK
# =============================================================================
KATEGORI_MAP = {
    'fashion'         : 'Fashion / Pakaian',
    'pakaian'         : 'Fashion / Pakaian',
    'gadget'          : 'Gadget / Elektronik / Aksesoris HP',
    'elektronik'      : 'Gadget / Elektronik / Aksesoris HP',
    'aksesoris hp'    : 'Gadget / Elektronik / Aksesoris HP',
    'skincare'        : 'Skincare / Kosmetik / Perawatan Tubuh',
    'kosmetik'        : 'Skincare / Kosmetik / Perawatan Tubuh',
    'perawatan'       : 'Skincare / Kosmetik / Perawatan Tubuh',
    'makanan'         : 'Makanan & Minuman / Camilan',
    'minuman'         : 'Makanan & Minuman / Camilan',
    'camilan'         : 'Makanan & Minuman / Camilan',
    'kebutuhan kuliah': 'Kebutuhan Kuliah / Alat Tulis / Buku',
    'alat tulis'      : 'Kebutuhan Kuliah / Alat Tulis / Buku',
    'buku'            : 'Kebutuhan Kuliah / Alat Tulis / Buku',
    'mainan'          : 'Mainan / Hobi',
    'kucing'          : 'Kebutuhan Hewan Peliharaan',
    'valorant'        : 'Voucher / Top-Up Game',
    'valo'            : 'Voucher / Top-Up Game',
}

def normalise_kategori(raw):
    if pd.isna(raw) or str(raw).lower() == 'nan':
        return "Lainnya"
    r = str(raw).lower()
    for key, label in KATEGORI_MAP.items():
        if key in r:
            return label
    return str(raw).title()

df['Kategori_Norm'] = df['Kategori_Produk'].apply(normalise_kategori)
kat_count = df['Kategori_Norm'].value_counts().reset_index()
kat_count.columns = ['Kategori Produk', 'Frekuensi']
kat_count['Persentase (%)'] = kat_count['Frekuensi'] / N * 100

print("4. TABEL DISTRIBUSI KATEGORI PRODUK (Q4):")
print(kat_count.to_string(index=False))
print("-" * 72)
modus_kategori = df['Kategori_Norm'].mode()[0]
print(f"Modus Kategori Produk: {modus_kategori}")
print("-" * 72 + "\n")

# =============================================================================
# 5. STATISTIK DESKRIPTIF – Q5 METODE PEMBAYARAN
# =============================================================================
data_metode = df['Metode_Pembayaran'].value_counts().reset_index()
data_metode.columns = ['Metode Pembayaran', 'Frekuensi']
data_metode['Persentase (%)'] = data_metode['Frekuensi'] / N * 100

print("5. TABEL DISTRIBUSI METODE PEMBAYARAN (Q5):")
print(data_metode.to_string(index=False))
print("-" * 72)
modus_metode = df['Metode_Pembayaran'].mode()[0]
print(f"Modus Metode Pembayaran Terfavorit: {modus_metode}")
print("-" * 72 + "\n")


# ── FUNGSI BANTU PENYIMPANAN CHART ──────────────────────────────────────────
def simpan_chart(fig, nama_file):
    path = os.path.join(OUTPUT_DIR, nama_file)
    fig.savefig(path, dpi=150, bbox_inches='tight')
    print(f"   [OK] Chart disimpan -> {path}")


# =============================================================================
# VISUALISASI – FIGURE 1: Q1 & Q5
# =============================================================================
fig1, axes1 = plt.subplots(1, 2, figsize=(17, 7))
fig1.suptitle('Analisis Belanja Marketplace – Kelompok 2 Statistika',
              fontsize=15, fontweight='bold')

# Q1 – Histogram horizontal
bars1 = axes1[0].barh(
    freq_p['Interval Pengeluaran'], freq_p['Frekuensi (f)'],
    color=BLUES, edgecolor='white', height=0.6)
axes1[0].set_title('Q1 · Distribusi Nominal Pengeluaran Bulanan\n(Materi Pertemuan 1-2)',
                   fontsize=13, pad=12)
axes1[0].set_xlabel('Jumlah Mahasiswa (Frekuensi)', fontsize=11)
axes1[0].set_ylabel('Interval Pengeluaran', fontsize=11)
for bar, val, pct in zip(bars1, freq_p['Frekuensi (f)'], freq_p['Persentase (%)']):
    axes1[0].text(bar.get_width() + 0.15, bar.get_y() + bar.get_height() / 2,
                  f'{int(val)}  ({pct:.1f}%)', va='center', fontsize=10, fontweight='bold')
axes1[0].set_xlim(0, freq_p['Frekuensi (f)'].max() + 4)

# Q5 – Pie / Donut Chart
metode_series = df['Metode_Pembayaran'].value_counts()
wedges5, _, auto5 = axes1[1].pie(
    metode_series,
    labels=None,
    autopct='%1.1f%%',
    startangle=140,
    colors=PASTEL,
    wedgeprops=dict(width=0.55, edgecolor='white', linewidth=2),
    pctdistance=0.75)
for at in auto5:
    at.set_fontsize(10)
    at.set_fontweight('bold')
axes1[1].set_title('Q5 · Tren Metode Pembayaran Marketplace\n(Analisis Preferensi Sistem Informasi)',
                   fontsize=13, pad=12)
axes1[1].legend(wedges5, metode_series.index, loc='lower center',
                bbox_to_anchor=(0.5, -0.20), ncol=2, fontsize=9, frameon=False)

plt.tight_layout()
simpan_chart(fig1, 'grafik_Q1_Q5.png')


# =============================================================================
# VISUALISASI – FIGURE 2: Q2 Frekuensi Checkout + Ogive
# =============================================================================
fig2, axes2 = plt.subplots(1, 2, figsize=(17, 6))
fig2.suptitle('Q2 · Frekuensi Checkout di Marketplace (1 Bulan Terakhir)',
              fontsize=14, fontweight='bold')

colors_c = sns.color_palette("rocket_r", len(urutan_freq))

# Bar chart frekuensi
b2 = axes2[0].bar(
    freq_c['Interval Frekuensi'], freq_c['Frekuensi (f)'],
    color=colors_c, edgecolor='white', width=0.6)
axes2[0].set_title('Distribusi Frekuensi Checkout', fontsize=12)
axes2[0].set_xlabel('Kelompok Frekuensi', fontsize=11)
axes2[0].set_ylabel('Jumlah Mahasiswa', fontsize=11)
axes2[0].tick_params(axis='x', rotation=20)
for bar, val, pct in zip(b2, freq_c['Frekuensi (f)'], freq_c['Persentase (%)']):
    axes2[0].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2,
                  f'{int(val)}\n({pct:.1f}%)', ha='center', va='bottom',
                  fontsize=10, fontweight='bold')

# Ogive – Frekuensi Kumulatif
x_pos = range(len(freq_c))
axes2[1].plot(x_pos, freq_c['Frekuensi Kumulatif (fk)'],
              marker='o', color='steelblue', linewidth=2.5,
              markersize=8, markerfacecolor='white', markeredgewidth=2)
axes2[1].fill_between(x_pos, freq_c['Frekuensi Kumulatif (fk)'],
                       alpha=0.15, color='steelblue')
axes2[1].set_xticks(x_pos)
axes2[1].set_xticklabels(freq_c['Interval Frekuensi'], rotation=20, ha='right')
axes2[1].set_title('Ogive – Frekuensi Kumulatif Checkout', fontsize=12)
axes2[1].set_xlabel('Kelompok Frekuensi', fontsize=11)
axes2[1].set_ylabel('Frekuensi Kumulatif', fontsize=11)
for x, fk in zip(x_pos, freq_c['Frekuensi Kumulatif (fk)']):
    axes2[1].annotate(f'{int(fk)}', (x, fk), textcoords="offset points",
                      xytext=(0, 8), ha='center', fontsize=10, fontweight='bold')

plt.tight_layout()
simpan_chart(fig2, 'grafik_Q2.png')


# =============================================================================
# VISUALISASI – FIGURE 3: Q3 Platform Marketplace
# =============================================================================
fig3, ax3 = plt.subplots(figsize=(11, 6))
colors_p = sns.color_palette("Set2", len(plat_df))
b3 = ax3.barh(plat_df['Platform'], plat_df['Frekuensi'],
              color=colors_p, edgecolor='white', height=0.6)
ax3.set_title('Q3 · Platform Marketplace yang Paling Sering Digunakan\n'
              '(Multi-pilihan; persentase dari total responden)',
              fontsize=13, pad=12)
ax3.set_xlabel('Jumlah Responden yang Memilih', fontsize=11)
ax3.set_ylabel('Platform', fontsize=11)
for bar, val, pct in zip(b3, plat_df['Frekuensi'], plat_df['Persentase (%)']):
    ax3.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height() / 2,
             f'{int(val)}  ({pct:.1f}%)', va='center', fontsize=10, fontweight='bold')
ax3.set_xlim(0, plat_df['Frekuensi'].max() + 8)
ax3.invert_yaxis()

plt.tight_layout()
simpan_chart(fig3, 'grafik_Q3.png')


# =============================================================================
# VISUALISASI – FIGURE 4: Q4 Kategori Produk
# =============================================================================
colors_k = sns.color_palette("tab10", len(kat_count))
fig4, axes4 = plt.subplots(1, 2, figsize=(18, 7))
fig4.suptitle('Q4 · Kategori Produk yang Paling Sering Dibeli di Marketplace',
              fontsize=14, fontweight='bold')

# Bar vertikal
b4 = axes4[0].bar(
    range(len(kat_count)), kat_count['Frekuensi'],
    color=colors_k, edgecolor='white', width=0.6)
axes4[0].set_xticks(range(len(kat_count)))
axes4[0].set_xticklabels(
    [k[:20] + '…' if len(k) > 20 else k for k in kat_count['Kategori Produk']],
    rotation=35, ha='right', fontsize=9)
axes4[0].set_title('Distribusi Kategori Produk', fontsize=12)
axes4[0].set_ylabel('Jumlah Mahasiswa', fontsize=11)
for bar, val, pct in zip(b4, kat_count['Frekuensi'], kat_count['Persentase (%)']):
    axes4[0].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                  f'{int(val)}\n({pct:.1f}%)', ha='center', va='bottom',
                  fontsize=9, fontweight='bold')

# Donut pie
wedges4, _, auto4 = axes4[1].pie(
    kat_count['Frekuensi'],
    labels=None,
    autopct='%1.1f%%',
    startangle=90,
    colors=colors_k,
    wedgeprops=dict(width=0.55, edgecolor='white', linewidth=2),
    pctdistance=0.78)
for at in auto4:
    at.set_fontsize(9)
    at.set_fontweight('bold')
axes4[1].set_title('Proporsi Kategori Produk', fontsize=12)
axes4[1].legend(wedges4, kat_count['Kategori Produk'], loc='lower center',
                bbox_to_anchor=(0.5, -0.28), ncol=2, fontsize=8, frameon=False)

plt.tight_layout()
simpan_chart(fig4, 'grafik_Q4.png')


# =============================================================================
# VISUALISASI – FIGURE 5: DASHBOARD RINGKASAN (semua Q dalam 1 gambar)
# =============================================================================
fig5 = plt.figure(figsize=(22, 14))
fig5.suptitle('DASHBOARD RINGKASAN – KELOMPOK 2 STATISTIKA\n'
              'Perilaku Belanja Mahasiswa di Marketplace',
              fontsize=16, fontweight='bold', y=0.99)

gs = fig5.add_gridspec(2, 3, hspace=0.50, wspace=0.38)
ax_q1 = fig5.add_subplot(gs[0, 0])
ax_q2 = fig5.add_subplot(gs[0, 1])
ax_q3 = fig5.add_subplot(gs[0, 2])
ax_q4 = fig5.add_subplot(gs[1, 0:2])
ax_q5 = fig5.add_subplot(gs[1, 2])

# Mini Q1
ax_q1.barh(freq_p['Interval Pengeluaran'], freq_p['Frekuensi (f)'],
           color=BLUES, edgecolor='white', height=0.6)
ax_q1.set_title('Q1 · Nominal Pengeluaran', fontsize=11, fontweight='bold')
ax_q1.set_xlabel('Frekuensi', fontsize=9)
for i, (v, p) in enumerate(zip(freq_p['Frekuensi (f)'], freq_p['Persentase (%)'])):
    ax_q1.text(v + 0.1, i, f'{int(v)} ({p:.0f}%)', va='center', fontsize=8)
ax_q1.set_xlim(0, freq_p['Frekuensi (f)'].max() + 5)
ax_q1.tick_params(axis='y', labelsize=8)

# Mini Q2
ax_q2.bar(freq_c['Interval Frekuensi'], freq_c['Frekuensi (f)'],
          color=sns.color_palette("rocket_r", len(urutan_freq)),
          edgecolor='white', width=0.6)
ax_q2.set_title('Q2 · Frekuensi Checkout', fontsize=11, fontweight='bold')
ax_q2.set_ylabel('Frekuensi', fontsize=9)
ax_q2.tick_params(axis='x', rotation=25, labelsize=7)
for bar, v in zip(ax_q2.patches, freq_c['Frekuensi (f)']):
    ax_q2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
               str(int(v)), ha='center', fontsize=9, fontweight='bold')

# Mini Q3
ax_q3.barh(plat_df['Platform'], plat_df['Frekuensi'],
           color=sns.color_palette("Set2", len(plat_df)),
           edgecolor='white', height=0.6)
ax_q3.set_title('Q3 · Platform Marketplace', fontsize=11, fontweight='bold')
ax_q3.set_xlabel('Dipilih oleh (orang)', fontsize=9)
ax_q3.invert_yaxis()
ax_q3.tick_params(axis='y', labelsize=8)
for bar, v in zip(ax_q3.patches, plat_df['Frekuensi']):
    ax_q3.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2,
               str(int(v)), va='center', fontsize=9, fontweight='bold')

# Mini Q4
ax_q4.bar(range(len(kat_count)), kat_count['Frekuensi'],
          color=colors_k, edgecolor='white', width=0.6)
ax_q4.set_xticks(range(len(kat_count)))
ax_q4.set_xticklabels(
    [k[:22] + '…' if len(k) > 22 else k for k in kat_count['Kategori Produk']],
    rotation=30, ha='right', fontsize=9)
ax_q4.set_title('Q4 · Kategori Produk yang Dibeli', fontsize=11, fontweight='bold')
ax_q4.set_ylabel('Frekuensi', fontsize=9)
for bar, v in zip(ax_q4.patches, kat_count['Frekuensi']):
    ax_q4.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
               str(int(v)), ha='center', fontsize=9, fontweight='bold')

# Mini Q5
ax_q5.pie(metode_series, labels=None, autopct='%1.1f%%', startangle=140,
          colors=PASTEL,
          wedgeprops=dict(width=0.55, edgecolor='white', linewidth=1.5),
          pctdistance=0.75, textprops={'fontsize': 8})
ax_q5.set_title('Q5 · Metode Pembayaran', fontsize=11, fontweight='bold')
ax_q5.legend(metode_series.index, loc='lower center',
             bbox_to_anchor=(0.5, -0.32), ncol=1, fontsize=7, frameon=False)

plt.tight_layout()
simpan_chart(fig5, 'grafik_DASHBOARD.png')

# ── TAMPILKAN SEMUA GRAFIK SECARA INTERAKTIF ────────────────────────────────
try:
    print("\nMenampilkan grafik interaktif...")
    print("Silakan lihat jendela grafik yang muncul. Tutup semua jendela untuk mengakhiri program.")
    
    # Buka folder output otomatis di file explorer (khusus Windows) agar user/dosen bisa langsung lihat hasil file fisiknya
    path_folder = os.path.abspath(OUTPUT_DIR)
    if platform.system() == "Windows":
        os.startfile(path_folder)
        
    plt.show()
except Exception as e:
    print(f"\n[Info] Tidak dapat menampilkan pop-up grafik secara otomatis: {e}")

print("\n" + "=" * 72)
print(f"SELESAI! Semua grafik visualisasi tersimpan di folder: {OUTPUT_DIR}/")
print("=" * 72)
