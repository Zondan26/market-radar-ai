# Laporan Evaluasi Riset Scalping Otomatis
- **Diperbarui:** 2026-11-26 18:51:52 WIB
- **Koneksi Gemini API:** `TERSAMBUNG` — Berhasil terhubung ke Gemini API (models/gemini-flash-lite-latest) | models=[models/gemini-2.5-flash, models/gemini-2.5-pro, models/gemini-2.5-flash-preview-tts, models/gemini-2.5-pro-preview-tts, models/gemma-4-26b-a4b-it, models/gemma-4-31b-it].
- **Total Entry:** 123 | **Win Rate:** 62.6% | **Net P/L:** $-74.42 | **Puncak Profit:** $5.48 (Erosi: 1458.03%)

## Perintah Aktif untuk MT5 (`strategy_command.json`)
- **Mode:** `CAUTIOUS` | **Min Peluang:** `63%` | **Cut Profit:** `10.0% - 15.0%` | **Max Posisi (Lot 0.01):** `500`
- **Aturan Saldo:** Jeda `60 menit` jika saldo turun `>=10.0%` dari saldo tertinggi, lalu lanjut entry otomatis
- **Jarak Tambah ATR:** `0.35` | **Auto-Cut Goyah:** `AKTIF`
- **Alasan Arahan:** Cut profit 10%-15% | Entry terbuka selama sinyal candle memenuhi | Jeda 1 jam bila saldo turun >=10% puncak | Mode CAUTIOUS (Entry #111 - #120: $-7.78, Net=$-74.42, RugiBesar=38): min peluang 63%, ATR 0.35.

## Memori & Pembelajaran Kesalahan (`error_memory.json`)
- **Evaluasi Ke-:** 1 | **Streak Evaluasi Rugi:** 1
- **Pola Rugi Terekam:** Tahan >=10m: `10` | Skor Tinggi (>=75): `37` | Cut Tidak Stabil: `0`

## Klasifikasi Tiap Entry
- Untung Besar: 28
- Untung Kecil: 25
- Rugi Kecil: 8
- Rugi Besar: 38
- Auto-Cut Untung (Chart/Berita Tidak Stabil): 24
- Auto-Cut Rugi (Chart/Berita Tidak Stabil): 0

## Rata-Rata Jeda Waktu / Durasi Tahan
- Entry ke TP: 13.19 menit
- Entry ke SL: 9.38 menit
- Entry ke Auto-Cut (Tanpa TP/SL): 2.9 menit

## Rekap Tiap 10 Kali Entry
- **Entry #1 - #10:** RUGI ($-2.68) | 9W / 1L | Rata-rata durasi: 1.83 menit
- **Entry #11 - #20:** RUGI ($-33.89) | 2W / 8L | Rata-rata durasi: 17.46 menit
- **Entry #21 - #30:** RUGI ($-19.63) | 4W / 6L | Rata-rata durasi: 1.2 menit
- **Entry #31 - #40:** UNTUNG ($18.58) | 9W / 1L | Rata-rata durasi: 2.18 menit
- **Entry #41 - #50:** UNTUNG ($16.02) | 9W / 1L | Rata-rata durasi: 1.84 menit
- **Entry #51 - #60:** RUGI ($-15.01) | 5W / 5L | Rata-rata durasi: 2.15 menit
- **Entry #61 - #70:** RUGI ($-26.55) | 3W / 7L | Rata-rata durasi: 2.09 menit
- **Entry #71 - #80:** RUGI ($-0.41) | 7W / 3L | Rata-rata durasi: 6.17 menit
- **Entry #81 - #90:** RUGI ($-17.79) | 6W / 4L | Rata-rata durasi: 7.82 menit
- **Entry #91 - #100:** UNTUNG ($3.74) | 6W / 4L | Rata-rata durasi: 6.42 menit
- **Entry #101 - #110:** UNTUNG ($35.42) | 10W / 0L | Rata-rata durasi: 2.4 menit
- **Entry #111 - #120:** RUGI ($-7.78) | 6W / 4L | Rata-rata durasi: 5.61 menit
- **Entry #121 - #123:** RUGI ($-24.44) | 1W / 2L | Rata-rata durasi: 24.14 menit

## Analisis Evaluasi AI
Berikut adalah analisis singkat, padat, dan tuntas berdasarkan data evaluasi riset scalping otomatis:

### 1. Evaluasi Profit vs Rugi
* **Kinerja Keseluruhan:** Meskipun tingkat kemenangan (*win rate*) tergolong baik di angka **62.6%** (77 Win / 46 Loss), total bersih (*net profit*) masih mencatat kerugian sebesar **-$74.42 USD**.
* **Puncak Profit & Erosi:** Puncak profit (*peak profit*) tercatat di **$5.48 USD**, namun mengalami erosi parah sebesar **$79.9 USD** atau setara dengan **1458.03%** dari puncak akibat akumulasi kerugian besar.
* **Auto-Cut vs SL:** Rata-rata *auto-cut* tanpa TP/SL sangat cepat (2.9 menit), yang efektif mengamankan profit kecil. Namun, sistem gagal meredam *drawdown* dalam kategori `RUGI_BESAR` (38 trade) di mana *Stop Loss* (SL) terseret hingga memakan sebagian besar profit dari *win streak* sebelumnya.

### 2. Evaluasi Durasi Tahan
* **Ke TP (Take Profit):** Rata-rata durasi **13.19 menit**, menunjukkan posisi yang dibiarkan mencapai target penuh membutuhkan waktu lebih lama.
* **Ke SL (Stop Loss):** Rata-rata durasi **9.38 menit**, menandakan posisi rugi dipotong lebih cepat daripada TP rata-rata, tetapi nominal kerugian per-trade masih terlalu besar dibanding rata-rata profit.
* **Auto-Cut:** Rata-rata durasi **2.9 menit**, menunjukkan mekanisme potong cepat berfungsi dengan baik untuk mengeliminasi ketidakpastian pasar jangka pendek.

### 3. Evaluasi Blok 10 Entry & Pola Kesalahan (`error_memory`)
* **Performa Blok:** Performa sangat fluktuatif. Blok awal hingga tengah (Entry #31-#50) sangat dominan profit. Namun, kemunduran signifikan terjadi pada blok akhir (Entry #61-#120), puncaknya pada **Entry #121 - #123** di mana terjadi *net loss* **-$24.44 USD** dengan durasi membengkak hingga **24.14 menit**.
* **Pola Kesalahan:** Berdasarkan *error_memory*, masalah utama adalah **`rugi_skor_tinggi_ge_75` (37x)** dan **`rugi_tahan_lama_ge_10_menit` (10x)**. Ini mengindikasikan bahwa sistem sering masuk pada sinyal dengan skor teknikal tinggi (M5/M15) yang ternyata berbalik arah, dan gagal melakukan *cut loss* dini saat durasi melebihi 10 menit.

### 4. Saran Penyetelan Parameter Konkret
1. **Perketat Filter Sinyal & Skor Minimum (`min_probabilitas`):** Naikkan ambang batas skor minimum dari 63% menjadi **70%–75%** untuk menyaring sinyal palsu yang menyumbang dominasi `rugi_skor_tinggi`.
2. **Implementasikan *Time-Based Stop* (Batas Waktu Tahan):** Tambahkan aturan paksa tutup posisi (*hard time-cut*) maksimal pada menit ke-8 jika posisi belum menyentuh TP/SL, guna memutus tren `rugi_tahan_lama_ge_10_menit` (seperti yang terjadi pada Entry #122 & #123).
3. **Optimasi Rasio Risiko (*Risk-to-Reward Ratio*):** Perketat jarak *Stop Loss* (pangkas jarak ATR) atau percepat ambang batas *cut profit* bawah menjadi **8%-10%** guna memastikan nilai *Win* mampu menutupi besarnya nilai *Loss* dari 38 kategori `RUGI_BESAR`.