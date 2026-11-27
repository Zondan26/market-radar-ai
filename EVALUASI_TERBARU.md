# Laporan Evaluasi Riset Scalping Otomatis
- **Diperbarui:** 2026-11-27 19:53:44 WIB
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
* **Kinerja Keseluruhan:** Meskipun tingkat kemenangan (*win rate*) cukup baik di angka **62.6%** (77 WIN / 46 LOSS), sistem mencatatkan net profit negatif **-$74.42**. Hal ini disebabkan oleh dominasi kategori `RUGI_BESAR` (38 trade) yang menggerus hasil dari 28 `UNTUNG_BESAR` dan 25 `UNTUNG_KECIL`.
* **Puncak Profit & Erosi:** Puncak profit (*peak profit*) tercatat sebesar **$5.48**, namun mengalami erosi masif sebesar **$79.9** atau setara dengan **1458.03%**. Rem tangan 30% aktif menunjukkan sistem gagal mengamankan profit sebelum berbalik arah.
* **Auto-Cut vs SL:** Mekanisme auto-cut (*basket/profit cut*) efektif mengamankan profit kecil secara cepat (tercatat 24 trade `CUT_UNTUNG_TIDAK_STABIL`), namun ketika posisi salah arah, *Stop Loss* (SL) memakan porsi kerugian yang terlalu besar per eksekusi dibandingkan rata-rata profit yang dikumpulkan.

### 2. Evaluasi Durasi Tahan (Holding Time)
* **Ke TP (Take Profit):** Rata-rata durasi **13.19 menit**, menunjukkan TP tercapai secara wajar untuk gaya scalping M5+M15.
* **Ke SL (Stop Loss):** Rata-rata durasi **9.38 menit**. Durasi ini relatif terlalu lama untuk ukuran scalping, mengindikasikan adanya indikasi *hope trading* (menahan posisi rugi terlalu lama berharap harga berbalik).
* **Auto-Cut Tanpa TP/SL:** Rata-rata durasi sangat cepat yaitu **2.9 menit**, membuktikan bahwa algoritma pemotong otomatis berfungsi agresif pada fase awal entry.

### 3. Evaluasi Blok 10 Entry & Pola Kesalahan (`error_memory`)
* **Blok 10 Entry:** Performa sangat fluktuatif. Blok awal hingga tengah sempat sangat produktif (contoh: Entry #101-#110 net profit +$35.42), namun memburuk drastis pada blok akhir (Entry #121-#123 mencatatkan net -$24.44 dengan durasi bengkak hingga 24+ menit).
* **Pola Kesalahan:** Memori kesalahan mencatat **37 kasus** pada kategori `rugi_skor_tinggi_ge_75` dan 10 kasus `rugi_tahan_lama_ge_10_menit`. Ironisnya, entry dengan skor teknikal tinggi (M5/M15 di atas 75-80) justru kerap berujung pada kerugian besar, menandakan sinyal indikator rentan terhadap *fake breakout* di instrumen XAUUSD.

### 4. Saran Penyetelan Parameter Konkret
1. **Perketat Filter Sinyal (Min Probabilitas & Skor):** Naikkan ambang batas `min_probabilitas` dari 63% menjadi minimal **70%-75%** dan wajibkan konfirmasi tren kuat pada M15 untuk mengurangi frekuensi `rugi_skor_tinggi`.
2. **Perpendek Batas Waktu Tahan Rugi (Max Holding Time / Time-based SL):** Terapkan aturan *time-based stop* maksimal 5 menit untuk scalping. Jika dalam 5 menit posisi tidak bergerak sesuai arah, lakukan *forced cut loss* guna memangkas durasi tahan rugi yang saat ini mencapai rata-rata 9+ menit.
3. **Optimasi Jarak ATR & Rasio Risk-to-Reward:** Sesuaikan `jarak_tambah_atr` dan perkecil level *Stop Loss* absolut atau aktifkan *Trailing Stop* yang lebih agresif untuk mencegah erosi profit ekstrem (1458%) terulang kembali.