# Laporan Evaluasi Riset Scalping Otomatis
- **Diperbarui:** 2026-11-25 14:56:07 WIB
- **Koneksi Gemini API:** `TERSAMBUNG` — Berhasil terhubung ke Gemini API (models/gemini-flash-lite-latest) | models=[models/gemini-2.5-flash, models/gemini-2.5-pro, models/gemini-2.5-flash-preview-tts, models/gemini-2.5-pro-preview-tts, models/gemma-4-26b-a4b-it, models/gemma-4-31b-it].
- **Total Entry:** 73 | **Win Rate:** 58.9% | **Net P/L:** $-56.5 | **Puncak Profit:** $5.48 (Erosi: 1131.02%)

## Perintah Aktif untuk MT5 (`strategy_command.json`)
- **Mode:** `CAUTIOUS` | **Min Peluang:** `63%` | **Max ADX Entry:** `30.0` | **Max Posisi (Lot 0.01):** `40`
- **Jarak Tambah ATR:** `0.35` | **Auto-Cut Goyah:** `AKTIF`
- **Alasan Arahan:** Rem tangan ADX>30 aktif karena kerugian besar (Entry #61 - #70: $-26.55, Net=$-56.5, RugiBesar=24): mode CAUTIOUS, min peluang 63%, max posisi 40, ATR 0.35.

## Memori & Pembelajaran Kesalahan (`error_memory.json`)
- **Evaluasi Ke-:** 1 | **Streak Evaluasi Rugi:** 1
- **Pola Rugi Terekam:** ADX Kuat (>=30): `22` | ADX Lemah (<20): `0` | Tahan >=10m: `5` | Skor Tinggi (>=75): `21`

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
Berikut adalah analisis evaluasi riset scalping otomatis (XAUUSD & EURUSD, lot 0.01) secara singkat, padat, dan tuntas:

### 1. Evaluasi Profit vs Rugi
*   **Performa Keseluruhan:** Walaupun *win rate* tampak cukup baik di angka **58.9%** (43 win dari 73 trade), akun mengalami kerugian bersih **-$56.5 USD**. 
*   **Puncak Profit & Erosi:** Puncak profit (*peak profit*) tercatat sangat rendah di **$5.48 USD**, namun mengalami erosi parah sebesar **1,131.02%** (-$61.98 USD) akibat akumulasi kerugian besar (*rugi_besar* sebanyak 24 trade).
*   **Auto-Cut vs SL:** Sebagian besar exit didorong oleh *Basket Profit Cut* atau *SL Hit*. Sistem kurang efektif melakukan *auto-cut* dini saat tren berbalik, membiarkan posisi terseret hingga terkena Stop Loss (SL) dengan nominal kerugian yang jauh lebih besar dibanding rata-rata profit kemenangan kecilnya.

### 2. Evaluasi Durasi Tahan
*   **Ke TP (38.23 menit):** Durasi rata-rata menuju TP cukup panjang, menunjukkan target profit sering kali membutuhkan waktu konfirmasi tren yang lebih lama.
*   **Ke SL (7.66 menit):** Posisi yang kalah cenderung lebih cepat dipangkas oleh SL (~7.6 menit), tetapi karena ukuran SL terlalu lebar atau lot bertumpuk saat tren kuat, dampaknya sangat merusak ekuitas.
*   **Auto-Cut Tanpa TP/SL (2.21 menit):** Durasi yang sangat singkat ini menunjukkan fitur pemotongan otomatis bekerja cepat pada kondisi tertentu, namun belum konsisten melindungi akumulasi profit basket.

### 3. Evaluasi Blok 10 Entry & Pola Kesalahan (`error_memory`)
*   **Analisis Blok:** Konsistensi profit hanya terlihat di blok tengah (#31-#50), sementara blok lainnya seperti #11-#20 (-$33.89) dan #61-#70 (-$26.55) mengalami kehancuran akibat *drawdown* yang dalam.
*   **Pola Kesalahan Utama:** Berdasarkan memori kesalahan, masalah terbesar adalah **`rugi_saat_adx_kuat_ge_30` (22 kejadian)** dan **`rugi_skor_tinggi_ge_75` (21 kejadian)**. Sistem keliru mengasumsikan skor tinggi dan ADX > 30 (tren kuat) sebagai sinyal entry yang aman untuk posisi *scalping* searah (dominan SELL di pasar emas yang sedang volatil), padahal kondisi tersebut rawan koreksi tajam/reversal.

### 4. Saran Penyetelan Parameter Konkret
1.  **Turunkan Ambang Batas ADX Maksimal (`max_adx_entry`):** Batasi entry pada ADX $\le$ 25 atau 30 untuk menghindari pasar yang *overextended* (mencegah 22 kasus rugi saat ADX kuat).
2.  **Perketat Filter Skor & Validasi M15:** Jangan mengeksekusi entry hanya karena skor $\ge$ 75 jika volatilitas XAUUSD sedang tinggi; wajibkan sinkronisasi momentum M15 yang lebih ketat.
3.  **Optimalkan *Smart Early TP* dan Rasio Risiko:** Naikkan kepekaan *auto-cut* profit labil (`min_untung_cut_usd`) dan perketat jarak *trailing stop* guna mencegah erosi profit dari puncak yang sudah tercapai ($5.48) agar tidak tersapu habis ke zona merah.