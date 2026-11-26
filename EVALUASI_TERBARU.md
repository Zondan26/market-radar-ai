# Laporan Evaluasi Riset Scalping Otomatis
- **Diperbarui:** 2026-11-27 03:43:33 WIB
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
* **Performa Keseluruhan:** Meskipun *Win Rate* cukup tinggi di angka 62.6% (77 WIN dari 123 trade), total Net PnL masih bernilai negatif sebesar -$74.42. 
* **Puncak & Erosi Profit:** *Peak Profit* tercatat pada angka $5.48, namun mengalami erosi yang sangat masif sebesar 1,458.03% (-$79.9) akibat akumulasi kerugian besar.
* **Auto-Cut vs SL:** Kategori `RUGI_BESAR` mendominasi dengan 38 kejadian, jauh melampaui `RUGI_KECIL` (8 kejadian). Hal ini menunjukkan bahwa sistem *Stop Loss* (SL) kurang efektif menahan risiko dibandingkan mekanisme *Auto-Cut* profit (tercatat 24 kali *cut* profit tidak stabil), di mana besar kerugian per trade individual (-$11 hingga -$14) menggerus hasil dari banyak trade WIN kecil.

**2. Evaluasi Durasi Tahan**
* **Ke TP:** Rata-rata durasi mencapai target profit adalah 13.19 menit.
* **Ke SL:** Rata-rata durasi terkena *Stop Loss* adalah 9.38 menit, dengan beberapa trade terakhir (seperti entry #122-#123) bahkan tertahan hingga 35 menit sebelum kena SL. Durasi ini terlalu lama untuk gaya scalping.
* **Auto-Cut Tanpa TP/SL:** Rata-rata durasi yang sangat cepat (2.9 menit) menunjukkan efektivitas sistem dalam mengamankan posisi cepat saat kondisi pasar berbalik.

**3. Evaluasi Blok 10 Entry & Pola Kesalahan**
* **Blok Entry:** Performa sangat fluktuatif. Blok awal (#31-#50) sangat produktif, namun performa merosot tajam pada blok #61-#70 (-$26.55) dan memburuk secara signifikan pada akhir sesi (#121-#123 dengan net -$24.44 dari 3 entry saja).
* **Pola Kesalahan (*Error Memory*):** Dominasi terbesar ada pada kategori `rugi_skor_tinggi_ge_75` (37 kejadian) dan `rugi_tahan_lama_ge_10_menit` (10 kejadian). Ini mengindikasikan bahwa skor sinyal tinggi (di atas 75) tidak menjamin ke akuratan jika durasi tahan dibiarkan terlalu lama (>10 menit) di instrumen XAUUSD.

**4. Saran Penyetelan Parameter Konkret**
1. **Perketat Time-Based Stop Loss (Max Holding Time):** Batasi maksimal durasi tahan posisi scalping hingga 5-7 menit saja. Jika dalam waktu tersebut posisi belum mencapai TP atau *auto-cut*, paksa sistem untuk menutup posisi guna menghindari lonjakan kerugian seperti pada entry #122 dan #123 (tertolak di 35 menit).
2. **Revisi Rasio Risiko/Reward (Risk-to-Reward Ratio):** Besaran kerugian per *SL Hit* (-$11 s.d. -$14) terlampau besar dibandingkan rata-rata profit hasil *Auto-Cut* atau TP. Perketat jarak SL atau naikkan ambang batas *min_probabilitas* (dari 63% menjadi minimal 70%) untuk menyaring sinyal palsu ber-skor tinggi.
3. **Optimasi Algoritma Cut Profit & Jeda:** Pertahankan mode `CAUTIOUS` dengan mempercepat aktivasi jeda 1 jam (`balance_drop_pause_pct`) jika terjadi *drawdown* beruntun pada rentang 5 entry terakhir, guna memutus rantai *streak rugi*.