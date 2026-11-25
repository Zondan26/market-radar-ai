# Laporan Evaluasi Riset Scalping Otomatis
- **Diperbarui:** 2026-11-25 13:12:50 WIB
- **Koneksi Gemini API:** `TERSAMBUNG` — Berhasil terhubung ke Gemini API (models/gemini-3-flash-preview) | models=[models/gemini-2.5-flash, models/gemini-2.5-pro, models/gemini-2.5-flash-preview-tts, models/gemini-2.5-pro-preview-tts, models/gemma-4-26b-a4b-it, models/gemma-4-31b-it].
- **Total Entry:** 64 | **Win Rate:** 59.38% | **Net P/L:** $-61.67

## Perintah Aktif untuk MT5 (`strategy_command.json`)
- **Mode:** `CAUTIOUS` | **Min Peluang:** `63%` | **Max Posisi (Lot 0.01):** `40`
- **Jarak Tambah ATR:** `0.35` | **Auto-Cut Goyah:** `AKTIF`
- **Alasan Arahan:** Belajar dari kesalahan (Entry #51 - #60: $-15.01, Net=$-61.67, RugiBesar=23): mode CAUTIOUS, min peluang 63%, max posisi 40, ATR 0.35.

## Memori & Pembelajaran Kesalahan (`error_memory.json`)
- **Evaluasi Ke-:** 1 | **Streak Evaluasi Rugi:** 1
- **Pola Rugi Terekam:** ADX Kuat (>=28): `23` | ADX Lemah (<20): `0` | Tahan >=10m: `5` | Skor Tinggi (>=75): `19`

## Klasifikasi Tiap Entry
- Untung Besar: 16
- Untung Kecil: 15
- Rugi Kecil: 3
- Rugi Besar: 23
- Auto-Cut Untung (Chart/Berita Tidak Stabil): 7
- Auto-Cut Rugi (Chart/Berita Tidak Stabil): 0

## Rata-Rata Jeda Waktu / Durasi Tahan
- Entry ke TP: 38.23 menit
- Entry ke SL: 7.86 menit
- Entry ke Auto-Cut (Tanpa TP/SL): 1.45 menit

## Rekap Tiap 10 Kali Entry
- **Entry #1 - #10:** RUGI ($-2.68) | 9W / 1L | Rata-rata durasi: 1.83 menit
- **Entry #11 - #20:** RUGI ($-33.89) | 2W / 8L | Rata-rata durasi: 17.46 menit
- **Entry #21 - #30:** RUGI ($-19.63) | 4W / 6L | Rata-rata durasi: 1.2 menit
- **Entry #31 - #40:** UNTUNG ($18.58) | 9W / 1L | Rata-rata durasi: 2.18 menit
- **Entry #41 - #50:** UNTUNG ($16.02) | 9W / 1L | Rata-rata durasi: 1.84 menit
- **Entry #51 - #60:** RUGI ($-15.01) | 5W / 5L | Rata-rata durasi: 2.15 menit
- **Entry #61 - #64:** RUGI ($-25.06) | 0W / 4L | Rata-rata durasi: 2.64 menit

## Analisis Evaluasi AI
Berikut adalah analisis evaluasi riset scalping otomatis Anda secara objektif dan ringkas:

### 1. Evaluasi Entry: Profit vs Loss
*   **Analisis Profit:** Untung Besar (16) dan Untung Kecil (15) didominasi oleh `BASKET_PROFIT_CUT`. Ini menunjukkan sistem berhasil mengamankan profit kolektif, namun nilainya sering kali kecil (rata-rata profit jauh di bawah nilai SL).
*   **Analisis Rugi:** Rugi Besar (23) hampir seluruhnya disebabkan oleh `SL_HIT`. Terjadi ketimpangan fatal: sistem melakukan *auto-cut* profit dengan cepat (rata-rata 1.45 menit), tetapi membiarkan rugi menyentuh SL penuh.
*   **Perbandingan RRR:** Rasio *Risk-to-Reward* sangat buruk. Meskipun *Win Rate* 59%, *Net Profit* tetap minus (-$61.67) karena satu kali rugi (SL) menghapus keuntungan dari 3-4 kali menang.

### 2. Evaluasi Jeda Waktu (Holding Time)
*   **Kecepatan SL:** Rata-rata durasi ke SL sangat singkat (**7.86 menit**) dibandingkan ke TP (**38.23 menit**). Ini mengindikasikan entry sering dilakukan di "pucuk" atau saat momentum lawan sangat kuat, sehingga harga langsung menghantam SL.
*   **Auto-Cut Instabilitas:** Fitur `auto_cut_unstable` bekerja sangat agresif (1.45 menit). Hal ini menyelamatkan akun dari volatilitas, tetapi juga memangkas potensi profit yang seharusnya bisa berkembang lebih besar jika diberikan ruang napas.

### 3. Evaluasi Blok Entry & Memori Kesalahan
*   **Tren Per Blok:**
    *   **Entry #31 - #50:** Sempat membaik (Untung).
    *   **Entry #51 - #64:** Performa hancur total (Rugi beruntun).
*   **Pola Kesalahan Berulang:** Kesalahan **masih terulang dan memburuk**.
    *   **ADX Tinggi (>= 28):** 23 kali rugi terjadi saat tren sangat kuat. Sistem scalping ini tampaknya mencoba melawan arus (*counter-trend*) atau masuk saat tren sudah jenuh, namun justru tergilas momentum.
    *   **Skor Tinggi (>= 75):** 19 kali rugi terjadi saat skor indikator sangat meyakinkan. Ini menunjukkan adanya "False Signal" pada algoritma scoring saat menghadapi volatilitas XAUUSD.

### 4. Saran Penyetelan Parameter (Action Plan)
Untuk memperbaiki performa secara bertahap, disarankan mengubah parameter berikut:

1.  **Filter ADX (Hard Stop):**
    *   **Setelan:** Tambahkan parameter `max_adx_entry: 25`.
    *   **Alasan:** Data menunjukkan 23 rugi besar terjadi saat ADX > 28. Menghindari entry saat tren terlalu kuat akan memangkas 80% total kerugian Anda.
2.  **Sinkronisasi Skor & Timeframe:**
    *   **Setelan:** `wajib_kompak_m15: true` dengan `min_score: 80`.
    *   **Alasan:** Banyak rugi terjadi pada skor tinggi. Memperketat syarat kekompakan antara M5 dan M15 akan menyaring sinyal palsu pada XAUUSD yang sering bergerak liar di timeframe rendah.
3.  **Penyesuaian Rasio Basket Cut:**
    *   **Setelan:** Naikkan `min_untung_cut_usd` menjadi lebih tinggi atau gunakan `trailing_stop` pada level basket.
    *   **Alasan:** Agar rata-rata kemenangan tidak terlalu kecil dibandingkan hantaman SL yang besar. Jika rugi dibatasi ketat, maka profit harus dibiarkan sedikit lebih lebar.