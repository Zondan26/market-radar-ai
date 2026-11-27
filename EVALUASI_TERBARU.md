# Laporan Evaluasi Riset Scalping Otomatis
- **Diperbarui:** 2026-11-28 04:44:45 WIB
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
Berikut adalah analisis evaluasi riset scalping otomatis berdasarkan data yang diberikan:

### 1. Evaluasi Profit vs Rugi
* **Performa Keseluruhan:** Meskipun tingkat kemenangan (*Win Rate*) cukup baik di angka **62.6%** (77 Win vs 46 Loss), net profit keseluruhan masih bernilai negatif **-$74.42**. Hal ini menunjukkan asimetri risiko di mana ukuran kerugian (*Rugi Besar* sebanyak 38 trade) jauh menggerus akumulasi kemenangan kecil.
* **Puncak Profit & Erosi:** *Peak profit* tercatat sebesar **$5.48**, namun mengalami erosi yang sangat ekstrem sebesar **1,458.03%** (-$79.9), memicu aktifnya *rem tangan 30%*.
* **Auto-Cut vs SL:** Mekanisme *auto-cut* berhasil mengamankan profit melalui skema seperti `PROFIT_CUT_10_15_PCT`, namun sistem gagal membatasi kerugian secara dini sebelum menyentuh Stop Loss (`SL_HIT`), menghasilkan kerugian per trade yang relatif besar (mencapai -$14.54).

### 2. Evaluasi Durasi Tahan (Holding Time)
* **Ke TP:** Rata-rata durasi mencapai TP adalah **13.19 menit**, menunjukkan posisi yang menang membutuhkan waktu lebih lama untuk matang.
* **Ke SL:** Rata-rata durasi ke SL adalah **9.38 menit**, yang mengindikasikan bahwa posisi yang salah cenderung bertahan terlalu lama di pasar alih-alih terpotong lebih awal (terkonfirmasi pada memori kesalahan: 10 kasus rugi tahan lama $\ge$ 10 menit).
* **Auto-Cut Tanpa TP/SL:** Rata-rata durasi sangat cepat yaitu **2.9 menit**, efektif mengamankan posisi saat kondisi tidak stabil terdeteksi.

### 3. Evaluasi Blok 10 Entry & Pola Kesalahan (`error_memory`)
* **Performa Per Blok:** Performa sangat fluktuatif. Blok awal hingga tengah (seperti #31-#50 dan #101-#110) sangat impresif dengan profit bersih yang baik dan win rate tinggi. Namun, tren memburuk drastis pada blok-blok akhir (khususnya #61-#70 dan #121-#123) akibat lonjakan *SL_HIT*.
* **Pola Kesalahan:** Berdasarkan `error_memory`, masalah utama terkonsentrasi pada **`rugi_skor_tinggi_ge_75` (37 kejadian)**. Artinya, sinyal dengan skor probabilitas tinggi (>75) kerap memberikan hasil *falsely confident* yang berujung pada kerugian besar, ditambah masalah durasi tahan posisi rugi yang lewat dari batas ideal.

### 4. Saran Penyetelan Parameter Konkret
1. **Perketat Sinyal Skor Tinggi & Filter Tren:** Evaluasi ulang formula skor M5 dan M15 karena skor $\ge 75$ masih menghasilkan banyak *false signal*. Wajibkan konfirmasi arah tren yang lebih ketat sebelum eksekusi untuk menekan 37 kasus rugi skor tinggi.
2. **Percepat Cut Loss / Time-Based Stop:** Batasi maksimal durasi tahan posisi rugi (misalnya maksimal 5 menit). Jika posisi belum bergerak sesuai arah dalam waktu tersebut, paksakan *auto-cut* untuk menghindari kerugian besar ($>$ -$10) seperti yang terjadi pada entry #122 dan #123.
3. **Optimasi Jarak ATR & Rasio Risk/Reward:** Sesuaikan `jarak_tambah_atr` (saat ini 0.35) atau perketat *Trailing Stop* / *Hard SL* agar ukuran kekalahan (*Rugi Besar*) tidak lebih besar daripada rata-rata *Untung Besar* yang bisa diraih.