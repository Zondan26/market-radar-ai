# Laporan Evaluasi Riset Scalping Otomatis
- **Diperbarui:** 2026-11-25 14:45:25 WIB
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
Berikut adalah analisis evaluasi riset scalping otomatis (XAUUSD & EURUSD) yang disusun secara singkat, padat, dan tuntas:

### 1. Evaluasi Profit vs Rugi
* **Kinerja Keseluruhan:** Meskipun win rate berada di angka cukup baik yaitu **58,9%** (43 win / 30 loss), sistem membukukan net profit negatif sebesar **-$56,5 USD**. Hal ini terjadi karena asimetri risiko di mana *Rugi Besar* mendominasi (24 kejadian) dibandingkan *Untung Besar* (20 kejadian).
* **Puncak Profit & Erosi:** Puncak profit (*peak profit*) tercatat sebesar **+$5,48 USD**, namun mengalami erosi masif sebesar **-$61,98 USD** atau setara dengan **1131,02%** dari puncak profit. Angka ini menunjukkan bahwa sistem gagal mengamankan profit saat tren berbalik, memaksa fitur rem tangan 30% aktif.
* **Auto-Cut vs SL:** Sebagian besar exit didorong oleh *Basket Profit Cut* dan *SL Hit*. Ketika tren kuat melawan posisi, Stop Loss (SL) mencatatkan kerugian nominal yang cukup besar per entry (rata-rata di atas -$6 USD), sementara auto-cut cepat dilakukan pada durasi sangat singkat namun belum mampu memangkas kerugian besar secara efektif.

### 2. Evaluasi Durasi Tahan (TP, SL, Auto-Cut)
* **Ke TP (Profit):** Rata-rata durasi bertahan hingga mencapai target profit adalah **38,23 menit**. Durasi ini relatif panjang untuk ukuran scalping, menunjukkan ketergantungan pada momentum tren yang stabil.
* **Ke SL (Loss):** Rata-rata durasi terkena SL adalah **7,66 menit**, mengindikasikan bahwa posisi yang salah arah cenderung cepat tereksekusi oleh batas risiko ketika volatilitas melonjak.
* **Auto-Cut Tanpa TP/SL:** Rata-rata durasi **2,21 menit** menunjukkan respons pemotongan otomatis yang sangat agresif pada fase awal entry, yang efektif mencegah kerugian compounding lebih dalam pada scalping jangka pendek.

### 3. Evaluasi Blok 10 Entry dan Pola Kesalahan (`error_memory`)
* **Kinerja Blok:** Performa sangat fluktuatif. Blok awal (#1-#20) dan blok tengah (#51-#70) mengalami kerugian besar (contoh: blok #11-#20 rugi -$33,89 dan blok #61-#70 rugi -$26,55). Sebaliknya, blok #31-#50 mencatat hasil positif konsisten karena kondisi pasar yang lebih bersahabat.
* **Pola Kesalahan Utama (`error_memory`):** 
  - **27 trade rugi** terjadi saat **ADX kuat (≥ 28)**, membuktikan bahwa sistem keliru masuk posisi *counter-trend* atau terlalu agresif mengejar tren yang sudah jenuh (exhaustion).
  - **21 trade rugi** terjadi saat **skor tinggi (≥ 75)**, menunjukkan indikator pentahapan skor masih menghasilkan *false signal* pada kondisi volatilitas tinggi XAUUSD.

### 4. Saran Penyetelan Parameter Konkret
1. **Perketat Filter ADX Maksimal:** Turunkan atau pertahankan batas `max_adx_entry` secara ketat di bawah **28.0** (sesuai mode *CAUTIOUS* saat ini). Hindari entry sama sekali jika ADX M5/M15 menunjukkan angka di atas 30 untuk mencegah jebakan tren kuat yang berbalik arah.
2. **Optimasi Trailing Stop / Smart Early TP:** Mengingat erosi profit mencapai >1100%, turunkan ambang batas `min_rasio_early_tp` atau percepat aktivasi *trailing stop* berbasis persentase profit kecil agar *peak profit* ($5.48) tidak habis tergerus oleh pembalikan arah mendadak.
3. **Validasi Ulang Skor Sinyal (≥75):** Lakukan rekalibrasi bobot indikator untuk mencegah *false high score* pada kondisi market trending ekstrem, serta wajibkan penyelarasan arah tren multi-timeframe (M5 + M15) secara lebih ketat sebelum eksekusi lot.