# Laporan Evaluasi Riset Scalping Otomatis
- **Diperbarui:** 2026-11-25 18:44:12 WIB
- **Koneksi Gemini API:** `TERSAMBUNG` — Berhasil terhubung ke Gemini API (models/gemini-3-flash-preview) | models=[models/gemini-2.5-flash, models/gemini-2.5-pro, models/gemini-2.5-flash-preview-tts, models/gemini-2.5-pro-preview-tts, models/gemma-4-26b-a4b-it, models/gemma-4-31b-it].
- **Total Entry:** 77 | **Win Rate:** 59.74% | **Net P/L:** $-59.51 | **Puncak Profit:** $5.48 (Erosi: 1185.95%)

## Perintah Aktif untuk MT5 (`strategy_command.json`)
- **Mode:** `CAUTIOUS` | **Min Peluang:** `63%` | **Max ADX Entry:** `30.0` | **Max Posisi (Lot 0.01):** `40`
- **Aturan ADX Tinggi:** Maks `2` entry, target cut `$0.3`, lock jika 2x SL hingga ADX M5 & M15 < `30.0`
- **Jarak Tambah ATR:** `0.35` | **Auto-Cut Goyah:** `AKTIF`
- **Alasan Arahan:** Rem tangan ADX>30 (maks 2 entry, target $0.3) aktif karena kerugian besar (Entry #61 - #70: $-26.55, Net=$-59.51, RugiBesar=25).

## Memori & Pembelajaran Kesalahan (`error_memory.json`)
- **Evaluasi Ke-:** 1 | **Streak Evaluasi Rugi:** 1
- **Pola Rugi Terekam:** ADX Kuat (>=30): `22` | ADX Lemah (<20): `0` | Tahan >=10m: `5` | Skor Tinggi (>=75): `22`

## Klasifikasi Tiap Entry
- Untung Besar: 20
- Untung Kecil: 19
- Rugi Kecil: 6
- Rugi Besar: 25
- Auto-Cut Untung (Chart/Berita Tidak Stabil): 7
- Auto-Cut Rugi (Chart/Berita Tidak Stabil): 0

## Rata-Rata Jeda Waktu / Durasi Tahan
- Entry ke TP: 38.23 menit
- Entry ke SL: 7.62 menit
- Entry ke Auto-Cut (Tanpa TP/SL): 2.09 menit

## Rekap Tiap 10 Kali Entry
- **Entry #1 - #10:** RUGI ($-2.68) | 9W / 1L | Rata-rata durasi: 1.83 menit
- **Entry #11 - #20:** RUGI ($-33.89) | 2W / 8L | Rata-rata durasi: 17.46 menit
- **Entry #21 - #30:** RUGI ($-19.63) | 4W / 6L | Rata-rata durasi: 1.2 menit
- **Entry #31 - #40:** UNTUNG ($18.58) | 9W / 1L | Rata-rata durasi: 2.18 menit
- **Entry #41 - #50:** UNTUNG ($16.02) | 9W / 1L | Rata-rata durasi: 1.84 menit
- **Entry #51 - #60:** RUGI ($-15.01) | 5W / 5L | Rata-rata durasi: 2.15 menit
- **Entry #61 - #70:** RUGI ($-26.55) | 3W / 7L | Rata-rata durasi: 2.09 menit
- **Entry #71 - #77:** UNTUNG ($3.65) | 5W / 2L | Rata-rata durasi: 6.84 menit

## Analisis Evaluasi AI
Berikut adalah analisis evaluasi riset scalping otomatis Anda:

### 1. Evaluasi Profit vs Rugi
*   **Performa Netral-Negatif:** Meskipun *win rate* mencapai **59.74%**, hasil akhir adalah **Net Loss -$59.51**. Ini menunjukkan anomali *Risk-to-Reward Ratio* yang sangat buruk.
*   **Erosi Profit:** Puncak profit hanya menyentuh **$5.48**, namun terjadi erosi sebesar **1185.95%** ($64.99) hingga saldo menjadi negatif. Sistem mengalami *bleeding* hebat setelah mencapai titik tertinggi yang kecil.
*   **Auto-cut vs SL:** Strategi ini terjebak dalam pola "menabung receh, rugi sekarung". *Auto-cut* (Basket/ADX Cut) menghasilkan untung kecil ($0.7 - $3), namun dihantam oleh **25 Rugi Besar** (rata-rata -$6 per trade) yang mayoritas berasal dari **SL_HIT**.

### 2. Evaluasi Durasi Tahan
*   **Ketimpangan Durasi:** Rata-rata durasi ke **TP (38.23 menit)** jauh lebih lama dibandingkan durasi ke **SL (7.62 menit)**. 
*   **Indikasi:** Market bergerak melawan posisi Anda 5x lebih cepat daripada bergerak menuju target. 
*   **Auto-cut:** Durasi *auto-cut* sangat singkat (**2.09 menit**). Hal ini menunjukkan fitur "Rem Tangan" bekerja sangat agresif memotong posisi, namun seringkali terlambat karena SL sudah tersentuh lebih dulu dalam volatilitas tinggi.

### 3. Evaluasi Blok & Error Memory
*   **Analisis Blok:** Performa sangat tidak stabil. Keuntungan di Blok #31-#50 (+$34.6) langsung musnah oleh kerugian masif di Blok #61-#70 (-$26.55) dan Blok #11-#20 (-$33.89).
*   **Pola Kesalahan (Error Memory):**
    *   **ADX Kuat (>=30):** Menjadi penyebab utama dengan **22 kegagalan**. Sistem mencoba melakukan scalping/reversal saat tren sedang sangat kuat, sehingga tersapu arus.
    *   **Skor Tinggi (>=75):** Uniknya, 22 kerugian terjadi saat skor indikator sangat tinggi. Ini menandakan adanya *false signal* pada kondisi *overbought/oversold* di M5/M15 yang tidak selaras dengan tren besar.

### 4. Saran Penyetelan Parameter Konkret
1.  **Perketat Filter ADX:** Ubah `max_adx_entry` dari 30.0 menjadi **25.0**. Data menunjukkan kerugian berulang terjadi saat ADX > 30. Hindari entry saat volatilitas tren sedang di puncak.
2.  **Optimasi SL & TP:** Jarak SL saat ini terlalu lebar atau mudah tersentuh dalam waktu singkat (7 menit). Perkecil nilai SL atau gunakan **Trailing Stop berbasis ATR** yang lebih dinamis agar kerugian per trade tidak mencapai -$6 (targetkan maks -$2 s/d -$3 untuk lot 0.01).
3.  **Sinkronisasi M15:** Aktifkan `wajib_kompak_m15: true` secara permanen dan naikkan `min_probabilitas` menjadi **70%**. Jangan izinkan entry jika M15 tidak memberikan konfirmasi arah yang sama dengan M5 untuk menghindari *noise* scalping.