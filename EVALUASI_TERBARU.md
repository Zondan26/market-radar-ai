# Laporan Evaluasi Riset Scalping Otomatis
- **Diperbarui:** 2026-11-25 12:36:55 WIB
- **Koneksi Gemini API:** `TERSAMBUNG` — Berhasil terhubung ke Gemini API (models/gemini-3-flash-preview) | models=[models/gemini-2.5-flash, models/gemini-2.5-pro, models/gemini-2.5-flash-preview-tts, models/gemini-2.5-pro-preview-tts, models/gemma-4-26b-a4b-it, models/gemma-4-31b-it].
- **Total Entry:** 32 | **Win Rate:** 53.12% | **Net P/L:** $-51.2

## Perintah Aktif untuk MT5 (`strategy_command.json`)
- **Mode:** `ACTIVE` | **Min Peluang:** `63%` | **Max Posisi (Lot 0.01):** `80`
- **Jarak Tambah ATR:** `0.3` | **Auto-Cut Goyah:** `AKTIF`
- **Alasan Arahan:** Evaluasi per 10 entry (Entry #31 - #32: $5.0): sesuaikan ambang peluang ke 63% dan jarak ATR 0.30 agar kualitas entri lebih terjaga.

## Klasifikasi Tiap Entry
- Untung Besar: 4
- Untung Kecil: 6
- Rugi Kecil: 0
- Rugi Besar: 15
- Auto-Cut Untung (Chart/Berita Tidak Stabil): 7
- Auto-Cut Rugi (Chart/Berita Tidak Stabil): 0

## Rata-Rata Jeda Waktu / Durasi Tahan
- Entry ke TP: 38.23 menit
- Entry ke SL: 10.65 menit
- Entry ke Auto-Cut (Tanpa TP/SL): 0.77 menit

## Rekap Tiap 10 Kali Entry
- **Entry #1 - #10:** RUGI ($-2.68) | 9W / 1L | Rata-rata durasi: 1.83 menit
- **Entry #11 - #20:** RUGI ($-33.89) | 2W / 8L | Rata-rata durasi: 17.46 menit
- **Entry #21 - #30:** RUGI ($-19.63) | 4W / 6L | Rata-rata durasi: 1.2 menit
- **Entry #31 - #32:** UNTUNG ($5.0) | 2W / 0L | Rata-rata durasi: 2.67 menit

## Analisis Evaluasi AI
Berikut adalah analisis evaluasi riset trading scalping otomatis Anda:

### 1. Evaluasi Tiap Entry (Profit vs Loss)
*   **Ketimpangan Risk/Reward:** Meskipun *Win Rate* mencapai 53.12%, hasil akhir tetap minus (-$51.2). Ini disebabkan oleh kategori **RUGI_BESAR (15 kali)** yang tidak sebanding dengan **UNTUNG_BESAR (4 kali)**.
*   **Penyebab Untung Kecil:** Fitur `UNSTABLE_PROFIT_GRAB` dan `BASKET_PROFIT_CUT` terlalu agresif mengambil untung di angka $0.2 - $0.5.
*   **Penyebab Rugi Besar:** Rata-rata rugi per SL berkisar -$4.3 hingga -$7.2. Perbandingannya sangat buruk: Anda membutuhkan sekitar **10-15 kali *auto-cut profit*** hanya untuk menutupi **1 kali *SL hit***. Sistem saat ini "menjemput receh tapi menyetor dolar".

### 2. Evaluasi Jeda Waktu (Holding Time)
*   **Efisiensi TP vs SL:** Rata-rata waktu ke TP (38 menit) jauh lebih lama dibandingkan waktu ke SL (10 menit). Ini mengindikasikan bahwa saat market berlawanan, harga bergerak sangat cepat menghantam SL, sementara saat searah, harga bergerak lambat atau ragu-ragu.
*   **Auto-Cut Unstable:** Durasi *auto-cut* sangat singkat (rata-rata 0.77 menit). Fitur ini menyelamatkan posisi dari pembalikan harga, namun jika terlalu sensitif, ia mematikan potensi *running profit* yang seharusnya bisa mencapai TP utama.

### 3. Evaluasi Blok 10 Entry & Skor (M5/M15/ADX)
*   **Blok #1 - #10 (Net -$2.68):** Skor rendah (M5:45, M15:20) dengan ADX rendah (~20). Banyak *win* tapi nominal sangat kecil, sehingga 1 kali kalah langsung menghapus semua keuntungan.
*   **Blok #11 - #20 (Net -$33.89):** **Blok terburuk.** Terjadi saat skor teknikal sangat rendah (M5:20, M15:0) dan ADX tinggi (30-40). Sistem memaksakan *Sell* saat market sedang *trending* kuat ke atas (melawan arus).
*   **Blok #21 - #30 (Net -$19.63):** Meskipun skor kompak tinggi (85/85), hasil tetap rugi. Ini menunjukkan bahwa pada volatilitas XAUUSD yang tinggi, skor teknikal saja tidak cukup jika jarak SL terlalu rapat atau entri dilakukan di ujung tren.
*   **Blok #31 - #32 (Net +$5.0):** Menunjukkan perbaikan kualitas setelah parameter `min_probabilitas` dinaikkan ke 63%.

### 4. Saran Penyetelan Parameter Konkret
Untuk memperbaiki performa pada tahap berikutnya, lakukan penyesuaian berikut:

1.  **Naikkan Ambang Batas Profit Cut:** Ubah `min_untung_cut_usd` dari **0.1** menjadi **1.5 - 2.0**. Ini bertujuan agar *auto-cut* tidak mematikan posisi terlalu dini sebelum biaya *spread* dan komisi tertutupi dengan layak secara rasio.
2.  **Filter ADX untuk Entry:** Tambahkan parameter untuk **melarang entry jika ADX M5 > 35** kecuali skor M5/M15 adalah 100. Hal ini untuk mencegah sistem melakukan *counter-trend* (melawan arus) saat momentum market sedang sangat kuat.
3.  **Perlebar Jarak ATR:** Pertahankan `jarak_tambah_atr` di **0.30 - 0.45** untuk memberikan "ruang bernapas" pada XAUUSD agar tidak mudah terkena *noise* harga yang memicu SL prematur.
4.  **Seleksi Skor Ketat:** Tetapkan `min_probabilitas` minimal **70%** dan pastikan `wajib_kompak_m15` tetap **TRUE**. Data menunjukkan skor di bawah 50% hampir selalu berakhir dengan `SL_HIT`.