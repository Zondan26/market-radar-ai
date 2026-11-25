# Laporan Evaluasi Riset Scalping Otomatis
- **Diperbarui:** 2026-11-25 17:22:12 WIB
- **Koneksi Gemini API:** `TERSAMBUNG` — Berhasil terhubung ke Gemini API (models/gemini-flash-lite-latest) | models=[models/gemini-2.5-flash, models/gemini-2.5-pro, models/gemini-2.5-flash-preview-tts, models/gemini-2.5-pro-preview-tts, models/gemma-4-26b-a4b-it, models/gemma-4-31b-it].
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
Berikut adalah analisis singkat, padat, dan tuntas terhadap evaluasi riset scalping otomatis XAUUSD & EURUSD:

**1. Evaluasi Profit vs Rugi**
*   **Performa Keseluruhan:** Sistem mencatatkan 77 trade dengan Win Rate 59,74% (46 Win, 31 Loss), namun berujung pada *Net Profit* negatif sebesar **-$59.51**. 
*   **Puncak Profit & Erosi:** Puncak profit (*peak profit*) tercatat sangat rendah di **+$5.48**, sementara erosi dari puncak mencapai **-$64.99 (-1.185,95%)**. Ini menunjukkan bahwa sistem gagal mengamankan profit kecil dan membiarkan posisi berbalik arah secara masif.
*   **Auto-Cut vs SL:** Kategori *Rugi Besar* mendominasi (25 trade) yang sebagian besar diakibatkan oleh *SL Hit*, jauh melampaui jumlah *CUT_UNTUNG_TIDAK_STABIL* (7 trade) dan tanpa ada *CUT_RUGI_TIDAK_STABIL*. Artinya, sistem terlalu mengandalkan SL mekanis alih-alih *auto-cut* dini saat tren mulai melawan posisi.

**2. Evaluasi Durasi Tahan**
*   **Ke TP (38,23 menit):** Durasi rata-rata menuju TP terlalu lama untuk gaya *scalping* M5+M15, meningkatkan risiko paparan volatilitas ekstrem XAUUSD.
*   **Ke SL (7,62 menit):** Durasi menuju SL relatif cepat, mengindikasikan bahwa penempatan *Stop Loss* terlalu ketat atau volatilitas pasar sedang tinggi.
*   **Auto-Cut Tanpa TP/SL (2,09 menit):** Durasi yang sangat ideal untuk scalping cepat, namun penerapannya belum konsisten menyelamatkan akun dari kerugian besar.

**3. Evaluasi Blok 10 Entry & Pola Kesalahan (`error_memory`)**
*   **Blok 10 Entry:** Performa sangat tidak stabil. Blok awal (#11-#20) dan tengah (#61-#70) mencatat kerugian terparah (masing-masing -$33.89 dan -$26.55), sementara blok #31-#50 sempat menunjukkan konsistensi profit.
*   **Pola Kesalahan:** Berdasarkan *error_memory*, akar masalah utama adalah **`rugi_saat_adx_kuat_ge_30` (22x)** dan **`rugi_skor_tinggi_ge_75` (22x)**. Sistem keliru mengasumsikan bahwa skor tinggi dan ADX kuat (>30) adalah peluang bagus untuk entry *counter-trend* (kebanyakan posisi SELL saat pasar agresif), yang justru berujung pada *SL Hit* beruntun.

**4. Saran Penyetelan Parameter Konkret**
1.  **Perketat Filter ADX & Ubah Logika Arah:** Turunkan `max_adx_entry` secara permanen ke bawah 25 atau pastikan sistem tidak melakukan *SELL* saat ADX > 30 kecuali ada konfirmasi pembalikan arah yang valid (hindari kebiasaan *fighting the trend*).
2.  **Optimalkan *Smart Early TP* & *Auto-Cut*:** Naikkan sensitivitas `min_untung_cut_usd` dan perketat `min_rasio_early_tp` agar profit kecil tidak tergerus menjadi minus (mengingat erosi puncak yang mencapai >1000%).
3.  **Perlebar Jarak ATR / Sesuaikan SL:** Karena rata-rata durasi ke SL sangat cepat (7 menit) dengan kerugian besar, evaluasi ulang rasio *Risk-to-Reward* atau perlebar jarak *buffer* ATR untuk menghindari tersapu (*noise hunting*) pada timeframe M5.