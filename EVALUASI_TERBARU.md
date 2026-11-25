# Laporan Evaluasi Riset Scalping Otomatis
- **Diperbarui:** 2026-11-25 13:25:41 WIB
- **Koneksi Gemini API:** `TERSAMBUNG` — Berhasil terhubung ke Gemini API (models/gemini-flash-lite-latest) | models=[models/gemini-2.5-flash, models/gemini-2.5-pro, models/gemini-2.5-flash-preview-tts, models/gemini-2.5-pro-preview-tts, models/gemma-4-26b-a4b-it, models/gemma-4-31b-it].
- **Total Entry:** 69 | **Win Rate:** 59.42% | **Net P/L:** $-62.94

## Perintah Aktif untuk MT5 (`strategy_command.json`)
- **Mode:** `CAUTIOUS` | **Min Peluang:** `63%` | **Max Posisi (Lot 0.01):** `40`
- **Jarak Tambah ATR:** `0.35` | **Auto-Cut Goyah:** `AKTIF`
- **Alasan Arahan:** Belajar dari kesalahan (Entry #51 - #60: $-15.01, Net=$-62.94, RugiBesar=24): mode CAUTIOUS, min peluang 63%, max posisi 40, ATR 0.35.

## Memori & Pembelajaran Kesalahan (`error_memory.json`)
- **Evaluasi Ke-:** 1 | **Streak Evaluasi Rugi:** 1
- **Pola Rugi Terekam:** ADX Kuat (>=28): `25` | ADX Lemah (<20): `0` | Tahan >=10m: `5` | Skor Tinggi (>=75): `19`

## Klasifikasi Tiap Entry
- Untung Besar: 18
- Untung Kecil: 16
- Rugi Kecil: 4
- Rugi Besar: 24
- Auto-Cut Untung (Chart/Berita Tidak Stabil): 7
- Auto-Cut Rugi (Chart/Berita Tidak Stabil): 0

## Rata-Rata Jeda Waktu / Durasi Tahan
- Entry ke TP: 38.23 menit
- Entry ke SL: 7.66 menit
- Entry ke Auto-Cut (Tanpa TP/SL): 1.49 menit

## Rekap Tiap 10 Kali Entry
- **Entry #1 - #10:** RUGI ($-2.68) | 9W / 1L | Rata-rata durasi: 1.83 menit
- **Entry #11 - #20:** RUGI ($-33.89) | 2W / 8L | Rata-rata durasi: 17.46 menit
- **Entry #21 - #30:** RUGI ($-19.63) | 4W / 6L | Rata-rata durasi: 1.2 menit
- **Entry #31 - #40:** UNTUNG ($18.58) | 9W / 1L | Rata-rata durasi: 2.18 menit
- **Entry #41 - #50:** UNTUNG ($16.02) | 9W / 1L | Rata-rata durasi: 1.84 menit
- **Entry #51 - #60:** RUGI ($-15.01) | 5W / 5L | Rata-rata durasi: 2.15 menit
- **Entry #61 - #69:** RUGI ($-26.33) | 3W / 6L | Rata-rata durasi: 2.3 menit

## Analisis Evaluasi AI
Berikut adalah analisis singkat, padat, dan tuntas terhadap evaluasi riset scalping otomatis XAUUSD & EURUSD:

### 1. Evaluasi Profit vs Rugi
* **Win Rate & Net PNL:** Dari total 69 trade, sistem mencatatkan *Win Rate* yang cukup baik di angka **59.42%** (41 win, 28 loss). Namun, secara finansial sistem masih merugi dengan **Net PNL $-62.94**.
* **Distribusi Kategori:** Kategori *Untung Besar* (18) dan *Untung Kecil* (16) sebetulnya mendominasi frekuensi profit. Masalah utama terletak pada masifnya **Rugi Besar (24 trade)** dibandingkan Rugi Kecil (4 trade). 
* **Rasio Profit/Loss:** Rata-rata profit per trade tertutup sepenuhnya oleh besarnya nominal saat *Stop Loss* (SL) tersentuh, mengindikasikan bahwa *Risk-to-Reward Ratio* (RRR) tidak seimbang di mana ukuran SL terlalu lebar/besar dibanding target profit tersier.

### 2. Evaluasi Durasi Tahan (TP, SL, Auto-Cut)
* **Ke TP (38.23 menit):** Durasi rata-rata menuju *Take Profit* terlalu lama untuk ukuran *scalping* M5+M15, membuat posisi rentan terkena balik arah pasar (reversal).
* **Ke SL (7.66 menit):** Cukup cepat, menunjukkan bahwa volatilitas XAUUSD sering menembus batas toleransi risiko sebelum tren sempat terbentuk sempurna.
* **Auto-Cut (1.49 menit):** Sangat efisien dan cepat memangkas posisi yang tidak stabil, mencegah kerugian yang lebih dalam pada kondisi tertentu.

### 3. Evaluasi Blok 10 Entry & Pola Kesalahan (`error_memory`)
* **Blok 10 Entry:** Performa sangat fluktuatif. Blok awal (#1-#10) dan akhir (#61-#69) hancur akibat kerugian besar, sementara blok tengah (#31-#50) sempat sangat konsisten menghasilkan profit.
* **Pola Kesalahan:** Memori kesalahan mendeteksi dua anomali fatal:
  1. **`rugi_saat_adx_kuat_ge_28` (25x):** Sistem keliru mengasumsikan ADX tinggi (>28) selalu bagus untuk entry searah (SELL), padahal pada instrumen XAUUSD, tren yang terlalu kuat sering berujung pada *exhaustion* atau *spike* berlawanan.
  2. **`rugi_skor_tinggi_ge_75` (19x):** Skor sinyal tinggi (>75) kerap memicu *overconfidence* entry padahal momentum pasar sudah jenuh.

### 4. Saran Penyetelan Parameter Konkret
1. **Batasi Maksimal ADX (Filter Kejenuhan Tren):** Tambahkan filter *upper-bound* ADX maksimal di angka 28-30 (misal: `max_adx: 30`). Jangan lakukan entry *scalping* searah jika ADX terlalu tinggi di atas 30 karena rawan koreksi tajam (mengatasi pola `rugi_saat_adx_kuat_ge_28`).
2. **Ketatkan Proteksi Skor Tinggi:** Turunkan sensitivitas skor atau wajibkan konfirmasi tambahan (seperti *Wajib Kompak M15*) ketika skor indikator berada di atas 75 untuk menghindari *fake breakout* di ujung tren.
3. **Optimalkan Risk-Reward & Perkecil Jarak SL:** Mengingat durasi ke SL sangat cepat (7 menit) dengan kerugian besar, perkecil jarak ATR untuk SL atau perketat *Smart Early TP* (turunkan `min_rasio_early_tp` di bawah 0.5) agar profit terkunci lebih cepat sebelum tersapu reversal.