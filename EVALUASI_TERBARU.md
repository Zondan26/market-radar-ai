# Laporan Evaluasi Riset Scalping Otomatis
- **Diperbarui:** 2026-11-27 10:23:31 WIB
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
Berikut adalah analisis evaluasi riset scalping otomatis berdasarkan data yang tersedia:

**1. Evaluasi Profit vs Rugi**
*   **Performa Keseluruhan:** Meskipun *Win Rate* cukup tinggi di angka 62.6% (77 WIN vs 46 LOSS), sistem mencatatkan *Net Profit* negatif sebesar -$74.42. 
*   **Puncak Profit & Erosi:** Puncak profit (*peak profit*) tercatat di angka $5.48, namun mengalami erosi yang sangat ekstrem sebesar $79.9 atau setara dengan **1458.03%**. Hal ini memicu fungsi pengaman (*rem tangan*) 30% aktif.
*   **Auto-Cut vs SL:** Sistem terlalu sering melakukan *auto-cut* profit kecil (kategori *CUT_UNTUNG_TIDAK_STABIL* sebanyak 24 kali), yang nilainya langsung tergerus telak oleh ukuran kekalahan saat *Stop Loss* (SL) tersentuh (tercatat 38 kali *RUGI_BESAR*). 

**2. Evaluasi Durasi Tahan**
*   **Ke TP (Take Profit):** Rata-rata durasi 13.19 menit, menunjukkan sistem cukup sabar saat tren searah target.
*   **Ke SL (Stop Loss):** Rata-rata durasi 9.38 menit. Durasi ini terlalu lama untuk ukuran scalping, mengindikasikan posisi rugi dibiarkan terlalu lama berharap berbalik arah sebelum akhirnya kena SL yang dalam.
*   **Auto-Cut:** Rata-rata durasi sangat cepat yaitu 2.9 menit, menunjukkan respons keluar cepat saat kondisi tidak stabil.

**3. Evaluasi Blok 10 Entry & Pola Kesalahan**
*   **Blok 10 Entry:** Performa sangat tidak konsisten. Blok awal hingga tengah sempat stabil (misal: Entry #31-#50 untung), namun memburuk drastis pada blok akhir (#61-#90 dan #111-#123) dengan dominasi blok rugi dan penutupan trade terakhir (#121-#123) yang minus -$24.44.
*   **Pola Kesalahan (*Error Memory*):** Dominasi kesalahan terbesar berada pada kategori `rugi_skor_tinggi_ge_75` (37 kejadian) dan `rugi_tahan_lama_ge_10_menit` (10 kejadian). Ini membuktikan bahwa skor sinyal tinggi (di atas 75) tidak menjamin kemenangan jika volatilitas XAUUSD melawan arah posisi *SELL*.

**4. Saran Penyetelan Parameter Konkret**
1.  **Perketat Filter Sinyal & Naikkan Probabilitas:** Tingkatkan `min_probabilitas` dari 63% menjadi >70% dan pastikan `wajib_kompak_m15` lebih ketat untuk menghindari jebakan sinyal palsu ber-skor tinggi pada XAUUSD.
2.  **Perpendek Batas Waktu Hold Loss (Time-based SL):** Batasi maksimal durasi posisi rugi (misal: auto-cut jika posisi minus dalam waktu >5 menit) guna memangkas durasi tahan SL rata-rata 9.38 menit yang terbukti menggerus modal.
3.  **Optimalisasi Rasio Risk-to-Reward:** Sesuaikan aturan *cut profit* agar tidak terlalu kecil di bawah nilai rata-rata kekalahan *SL* (perbaiki rasio *Win/Loss payout* agar $1 kemenangan tidak kalah besar dibanding $1 kekalahan).