# Laporan Evaluasi Riset Scalping Otomatis
- **Diperbarui:** 2026-11-25 13:52:06 WIB
- **Koneksi Gemini API:** `TERSAMBUNG` — Berhasil terhubung ke Gemini API (models/gemini-flash-lite-latest) | models=[models/gemini-2.5-flash, models/gemini-2.5-pro, models/gemini-2.5-flash-preview-tts, models/gemini-2.5-pro-preview-tts, models/gemma-4-26b-a4b-it, models/gemma-4-31b-it].
- **Total Entry:** 73 | **Win Rate:** 58.9% | **Net P/L:** $-56.5 | **Puncak Profit:** $5.48 (Erosi: 1131.02%)

## Perintah Aktif untuk MT5 (`strategy_command.json`)
- **Mode:** `CAUTIOUS` | **Min Peluang:** `63%` | **Max ADX Entry:** `28.0` | **Max Posisi (Lot 0.01):** `40`
- **Jarak Tambah ATR:** `0.35` | **Auto-Cut Goyah:** `AKTIF`
- **Alasan Arahan:** Rem tangan ADX>28 aktif karena kerugian besar (Entry #61 - #70: $-26.55, Net=$-56.5, RugiBesar=24): mode CAUTIOUS, min peluang 63%, max posisi 40, ATR 0.35.

## Memori & Pembelajaran Kesalahan (`error_memory.json`)
- **Evaluasi Ke-:** 1 | **Streak Evaluasi Rugi:** 1
- **Pola Rugi Terekam:** ADX Kuat (>=28): `27` | ADX Lemah (<20): `0` | Tahan >=10m: `5` | Skor Tinggi (>=75): `21`

## Klasifikasi Tiap Entry
- Untung Besar: 20
- Untung Kecil: 16
- Rugi Kecil: 6
- Rugi Besar: 24
- Auto-Cut Untung (Chart/Berita Tidak Stabil): 7
- Auto-Cut Rugi (Chart/Berita Tidak Stabil): 0

## Rata-Rata Jeda Waktu / Durasi Tahan
- Entry ke TP: 38.23 menit
- Entry ke SL: 7.66 menit
- Entry ke Auto-Cut (Tanpa TP/SL): 2.21 menit

## Rekap Tiap 10 Kali Entry
- **Entry #1 - #10:** RUGI ($-2.68) | 9W / 1L | Rata-rata durasi: 1.83 menit
- **Entry #11 - #20:** RUGI ($-33.89) | 2W / 8L | Rata-rata durasi: 17.46 menit
- **Entry #21 - #30:** RUGI ($-19.63) | 4W / 6L | Rata-rata durasi: 1.2 menit
- **Entry #31 - #40:** UNTUNG ($18.58) | 9W / 1L | Rata-rata durasi: 2.18 menit
- **Entry #41 - #50:** UNTUNG ($16.02) | 9W / 1L | Rata-rata durasi: 1.84 menit
- **Entry #51 - #60:** RUGI ($-15.01) | 5W / 5L | Rata-rata durasi: 2.15 menit
- **Entry #61 - #70:** RUGI ($-26.55) | 3W / 7L | Rata-rata durasi: 2.09 menit
- **Entry #71 - #73:** UNTUNG ($6.66) | 2W / 1L | Rata-rata durasi: 13.45 menit

## Analisis Evaluasi AI
Berikut adalah analisis evaluasi riset scalping otomatis (XAUUSD & EURUSD, lot 0.01, M5+M15) secara singkat, padat, dan tuntas:

### 1. Evaluasi Profit vs Rugi
* **Kinerja Keseluruhan:** Meskipun tingkat kemenangan (*win rate*) tampak moderat di angka **58.9%** (43 win / 30 loss), sistem mencatatkan net profit negatif **-$56.5 USD**. 
* **Erosi Profit:** Terjadi anomali ekstrem pada pengelolaan profit. Sistem sempat mencapai puncak keuntungan (*peak profit*) sebesar **$5.48 USD**, namun mengalami erosi parah sebesar **-$61.98 USD** atau setara dengan **1,131.02%**.
* **Perbandingan Auto-Cut vs SL:** Kategori `RUGI_BESAR` mendominasi (24 kejadian) yang sebagian besar dieksekusi melalui *Stop Loss (SL_HIT)* dengan nilai kerugian per trade yang konstan di kisaran -$5.9 hingga -$6.5 USD. Sebaliknya, *auto-cut* (`BASKET_PROFIT_CUT`) sering menutup posisi dengan profit kecil atau rugi mikro, gagal menahan posisi pemenang lebih lama untuk mengimbangi besarnya nilai SL.

### 2. Evaluasi Durasi Tahan
* **Ke TP (Take Profit):** Rata-rata durasi bertahan hingga mencapai target profit adalah **38.23 menit**, menunjukkan bahwa *winning trades* membutuhkan waktu lebih panjang untuk matang.
* **Ke SL (Stop Loss):** Rata-rata durasi terkena SL adalah **7.66 menit**, mengindikasikan bahwa volatilitas pasar langsung menghantam batas risiko dalam waktu relatif singkat.
* **Auto-Cut Tanpa TP/SL:** Rata-rata durasi sangat cepat yaitu **2.21 menit**, menunjukkan fungsi pengaman darurat merespons kondisi fluktuatif dengan sigap tetapi belum efektif memfilter kualitas entry awal.

### 3. Evaluasi Blok 10 Entry & Pola Kesalahan (*Error Memory*)
* **Blok 10 Entry:** Performa sangat tidak stabil. Blok awal (#1-#30) dan pertengahan (#51-#70) banyak diwarnai hasil negatif (contoh terburuk pada blok #11-#20 dengan rugi **-$33.89 USD**). Profitabilitas hanya konsisten pada blok #31-#50.
* **Pola Kesalahan Utama:** Sistem *error_memory* mendeteksi korelasi kerugian mutlak pada **`rugi_saat_adx_kuat_ge_28` (27 kejadian)** dan **`rugi_skor_tinggi_ge_75` (21 kejadian)**. Akar masalahnya adalah sistem tetap agresif melakukan entry (bahkan saat skor sinyal tinggi ≥75) di tengah kondisi pasar dengan ADX sangat kuat (>28), yang mana pada instrumen XAUUSD justru sering memicu pembalikan arah atau *fake breakout* alih-alih tren berkelanjutan.

### 4. Saran Penyetelan Parameter Konkret
1. **Perketat Filter ADX Maksimal (`max_adx_entry`):** Turunkan batas maksimal ADX dari 28.0 menjadi **24.0** untuk menghindari entry di tengah volatilitas tren jenuh (*exhausted trend*), mengingat 27 kerugian besar terjadi saat ADX ≥28.
2. **Terapkan Rasio Risiko-Imbalan yang Sehat (*Risk-to-Reward Ratio*):** Perlebar target *Smart Early TP* atau perketat *Stop Loss* karena saat ini nilai SL tunggal jauh lebih besar dibandingkan rata-rata *Basket Profit Cut*, membuat 1 kali SL menghapus hasil 3-4 kali *win*.
3. **Optimalkan Jarak Tambah Posisi (`jarak_tambah_atr`):** Naikkan pengali ATR dari 0.35 menjadi **0.50 - 0.65** pada mode *Cautious* untuk mencegah penumpukan posisi (*averaging/grid*) terlalu rapat saat XAUUSD bergerak fluktuatif dalam rentang sempit ber-ADX tinggi.