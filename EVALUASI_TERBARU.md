# Laporan Evaluasi Riset Scalping Otomatis
- **Diperbarui:** 2026-11-28 10:38:58 WIB
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
Berikut adalah analisis evaluasi riset scalping otomatis (XAUUSD & EURUSD, lot 0.01):

### 1. Evaluasi Profit vs Rugi
* **Profit & Win Rate:** Total trade sebanyak 123 dengan win rate cukup baik di angka **62.6%** (77 win, 46 loss). Namun, secara akumulatif menghasilkan net profit negatif **-$74.42** akibat dominasi kategori `RUGI_BESAR` (38 trade) yang menggerus hasil dari kategori `UNTUNG_BESAR` (28 trade).
* **Puncak & Erosi Profit:** *Peak profit* tercatat di angka **$5.48**, dengan tingkat erosi yang sangat ekstrem mencapai **1,458.03%** (-$79.9), memicu aktifnya fitur pengaman *rem tangan 30%*.
* **Auto-Cut vs SL:** Mekanisme *auto-cut* (seperti `PROFIT_CUT_10_15_PCT`) efektif mengamankan profit kecil-menengah secara instan, namun ketika posisi berbalik arah, ukuran *Stop Loss (SL)* terlalu lebar atau terlambat dipangkas, sehingga menghasilkan nominal rugi per trade yang jauh lebih besar daripada rata-rata profit yang dikumpulkan.

### 2. Evaluasi Durasi Tahan (Holding Time)
* **Ke TP:** Rata-rata durasi **13.19 menit**, menunjukkan target profit wajar untuk timeframe M5+M15.
* **Ke SL:** Rata-rata durasi **9.38 menit**. Durasi ini mengindikasikan bahwa posisi yang terkena SL cenderung bertahan terlalu lama di zona merah sebelum akhirnya tersenggol batas risiko maksimal.
* **Auto-Cut (Tanpa TP/SL):** Rata-rata durasi sangat cepat yaitu **2.9 menit**, membuktikan bahwa sistem bereaksi sangat baik dalam memotong posisi tidak stabil di awal durasi.

### 3. Evaluasi Blok 10 Entry & Pola Kesalahan (`error_memory`)
* **Performa Blok:** Performa sangat fluktuatif. Blok awal hingga tengah sempat mencetak hasil positif (misal: Entry #101-#110 profit $35.42), namun performa merosot tajam di blok-blok akhir, terutama pada 3 entry terakhir (#121-#123) yang mencatat rugi -$24.44 dengan durasi bengkak hingga 35 menit.
* **Pola Kesalahan:** Berdasarkan *error_memory*, masalah utama terkonsentrasi pada `rugi_skor_tinggi_ge_75` (tercatat 37 kali). Hal ini mengindikasikan bahwa skor indikator teknikal (M5+M15) yang tinggi (>75) masih sering terjebak *fakeout* atau pembalikan tren mendadak pada instrumen volatil seperti XAUUSD.

### 4. Saran Penyetelan Parameter Konkret
1. **Perketat Jarak Stop Loss (SL):** Pangkas batas risiko maksimal per trade (turunkan parameter SL) untuk menghindari kerugian besar (`RUGI_BESAR`) yang saat ini merusak rasio *Risk-to-Reward*.
2. **Optimalkan Filter Skor Tinggi (>75):** Tambahkan konfirmasi volume atau indikator momentum tambahan (seperti RSI/ADX) pada sinyal dengan skor $\ge 75$ untuk menekan angka kegagalan pada *entry* bernilai probabilitas tinggi.
3. **Perpendek Batas Waktu Tahan (Max Holding Time):** Batasi durasi maksimal posisi terbuka (misal *hard cut* di bawah 10 menit jika tidak bergerak ke arah TP) guna mencegah fenomena posisi minus yang dibiarkan terlalu lama (seperti kasus durasi 35 menit pada entry akhir).