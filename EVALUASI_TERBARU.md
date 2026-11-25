# Laporan Evaluasi Riset Scalping Otomatis
- **Diperbarui:** 2026-11-25 21:47:01 WIB
- **Koneksi Gemini API:** `TERSAMBUNG` — Berhasil terhubung ke Gemini API (models/gemini-flash-lite-latest) | models=[models/gemini-2.5-flash, models/gemini-2.5-pro, models/gemini-2.5-flash-preview-tts, models/gemini-2.5-pro-preview-tts, models/gemma-4-26b-a4b-it, models/gemma-4-31b-it].
- **Total Entry:** 109 | **Win Rate:** 63.3% | **Net P/L:** $-46.82 | **Puncak Profit:** $5.48 (Erosi: 954.38%)

## Perintah Aktif untuk MT5 (`strategy_command.json`)
- **Mode:** `CAUTIOUS` | **Min Peluang:** `63%` | **Cut Profit:** `10.0% - 15.0%` | **Max Posisi (Lot 0.01):** `500`
- **Aturan Saldo:** Jeda `60 menit` jika saldo turun `>=10.0%` dari saldo tertinggi, lalu lanjut entry otomatis
- **Jarak Tambah ATR:** `0.35` | **Auto-Cut Goyah:** `AKTIF`
- **Alasan Arahan:** Cut profit 10%-15% | Entry terbuka selama sinyal candle memenuhi | Jeda 1 jam bila saldo turun >=10% puncak | Mode CAUTIOUS (Entry #91 - #100: $3.74, Net=$-46.82, RugiBesar=32): min peluang 63%, ATR 0.35.

## Memori & Pembelajaran Kesalahan (`error_memory.json`)
- **Evaluasi Ke-:** 1 | **Streak Evaluasi Rugi:** 1
- **Pola Rugi Terekam:** Tahan >=10m: `7` | Skor Tinggi (>=75): `31` | Cut Tidak Stabil: `0`

## Klasifikasi Tiap Entry
- Untung Besar: 28
- Untung Kecil: 25
- Rugi Kecil: 8
- Rugi Besar: 32
- Auto-Cut Untung (Chart/Berita Tidak Stabil): 16
- Auto-Cut Rugi (Chart/Berita Tidak Stabil): 0

## Rata-Rata Jeda Waktu / Durasi Tahan
- Entry ke TP: 13.19 menit
- Entry ke SL: 7.99 menit
- Entry ke Auto-Cut (Tanpa TP/SL): 2.82 menit

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
- **Entry #101 - #109:** UNTUNG ($30.8) | 9W / 0L | Rata-rata durasi: 2.52 menit

## Analisis Evaluasi AI
Berikut adalah analisis evaluasi riset scalping otomatis secara singkat, padat, dan tuntas:

### 1. Evaluasi Profit vs Rugi
* **Kinerja Keseluruhan:** Meskipun *win rate* tergolong baik di angka **63.3%** (69 win / 40 loss), total net PnL masih bernilai negatif **-$46.82**. 
* **Puncak Profit & Erosi:** *Peak profit* tercatat sangat rendah di **$5.48**, namun mengalami erosi masif sebesar **954.38%** (-$52.3) akibat besarnya nominal *loss* per posisi.
* **Auto-Cut vs SL:** Mekanisme *auto-cut* efektif mengamankan profit kecil secara cepat, namun tidak sebanding dengan kerugian dari *Stop Loss* (SL Hit) dan kategori `RUGI_BESAR` (tercatat 32 kejadian) yang menggerus akumulasi kemenangan.

### 2. Evaluasi Durasi Tahan (Holding Time)
* **Ke TP (Rata-rata 13.19 menit):** Durasi menuju *Take Profit* relatif ideal untuk menangkap momentum tren pendek di M5+M15.
* **Ke SL (Rata-rata 7.99 menit):** Waktu tahan saat salah arah cukup cepat, namun ukuran risiko (*lot/distance*) tampaknya terlalu berat terhadap margin profit.
* **Auto-Cut Tanpa TP/SL (Rata-rata 2.82 menit):** Sangat efisien dan responsif dalam memotong posisi yang tidak stabil atau menghindari pembalikan arah mendadak.

### 3. Evaluasi Blok 10 Entry & Pola Kesalahan (`error_memory`)
* **Performa Blok:** Terjadi performa yang tidak konsisten. Blok awal hingga tengah (`#11` s.d. `#90`) didominasi hasil **RUGI** akibat tekanan *drawdown* yang dalam. Namun, sistem menunjukkan pemulihan signifikan pada blok akhir (`#91` s.d. `#109`), khususnya pada blok `#101 - #109` yang sukses mencetak *win rate* 100% ($+$30.8 USD).
* **Pola Kesalahan:** *Error memory* mendeteksi masalah utama pada kategori `rugi_skor_tinggi_ge_75` (terjadi 31 kali). Artinya, sistem sering masuk posisi dengan keyakinan skor tinggi (>75) namun tetap terkena SL, mengindikasikan adanya *false signal* saat volatilitas tinggi di XAUUSD.

### 4. Saran Penyetelan Parameter Konkret
1. **Perketat Filter Skor & Konfirmasi M15:** Naikkan batas minimum probabilitas/skor dari 63 menjadi minimal **70-75**, serta pastikan `wajib_kompak_m15` benar-benar memfilter arah tren secara ketat untuk meredam kasus `rugi_skor_tinggi_ge_75`.
2. **Optimalisasi Risk-to-Reward Ratio (RRR):** Sesuaikan jarak SL atau percepat *trailing stop* karena saat ini 1 kali *loss* besar mampu memakan hasil 4-5 kali *win* kecil.
3. **Pertahankan Mode Cautious & Jeda Saldo:** Pertahankan aturan *pause* otomatis saat saldo turun $\ge 10\%$ untuk memutus *losing streak* psikologis dan teknis seperti yang terbukti sukses membalikkan performa di blok akhir.