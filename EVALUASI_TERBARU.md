# Laporan Evaluasi Riset Scalping Otomatis
- **Diperbarui:** 2026-11-25 13:34:57 WIB
- **Koneksi Gemini API:** `TERSAMBUNG` — Berhasil terhubung ke Gemini API (models/gemini-flash-lite-latest) | models=[models/gemini-2.5-flash, models/gemini-2.5-pro, models/gemini-2.5-flash-preview-tts, models/gemini-2.5-pro-preview-tts, models/gemma-4-26b-a4b-it, models/gemma-4-31b-it].
- **Total Entry:** 73 | **Win Rate:** 58.9% | **Net P/L:** $-56.5

## Perintah Aktif untuk MT5 (`strategy_command.json`)
- **Mode:** `CAUTIOUS` | **Min Peluang:** `63%` | **Max Posisi (Lot 0.01):** `40`
- **Jarak Tambah ATR:** `0.35` | **Auto-Cut Goyah:** `AKTIF`
- **Alasan Arahan:** Belajar dari kesalahan (Entry #61 - #70: $-26.55, Net=$-56.5, RugiBesar=24): mode CAUTIOUS, min peluang 63%, max posisi 40, ATR 0.35.

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
Berikut adalah analisis evaluasi riset scalping otomatis (XAUUSD & EURUSD, lot 0.01) secara singkat, padat, dan tuntas:

### 1. Evaluasi Profit vs Rugi
* **Performa Keseluruhan:** Meskipun *Win Rate* berada di angka **58.9%** (43 Win vs 30 Loss), sistem mencatatkan net PnL negatif sebesar **$-56.5 USD**. 
* **Distribusi Kategori & Asimetri Risiko:** Dominasi kerugian berasal dari kategori **RUGI_BESAR (24 trade)** yang jauh menggerus akumulasi profit dari **UNTUNG_BESAR (20 trade)** dan **UNTUNG_KECIL (16 trade)**. 
* **Rata-rata Auto-Cut vs SL:** Sistem terlalu sering membiarkan posisi terkena *Stop Loss* murni (SL Hit dengan nominal besar, rata-rata $-6 USD per trade) dibandingkan memotong kerugian lebih awal melalui mekanisme *auto-cut* yang tidak stabil (tercatat 0 untuk cut rugi tidak stabil, mengindikasikan fitur *cut loss* dini belum bekerja optimal saat tren berbalik).

### 2. Evaluasi Durasi Tahan (Holding Time)
* **Ke TP (38.23 menit):** Durasi rata-rata menuju Target Profit tergolong panjang untuk ukuran scalping M5, menunjukkan posisi sempat mengalami floating minus yang cukup lama sebelum akhirnya tertutup profit.
* **Ke SL (7.66 menit):** Waktu potong rugi relatif cepat, namun ukuran kerugian tetap besar karena volatilitas XAUUSD yang tinggi pada timeframe tersebut.
* **Auto-Cut Tanpa TP/SL (2.21 menit):** Durasi yang sangat singkat ini menunjukkan efektivitas *basket profit cut* atau *early exit* dalam mengamankan posisi mikro dengan cepat, namun belum diaplikasikan secara agresif untuk memangkas *floating loss*.

### 3. Evaluasi Blok 10 Entry & Pola Kesalahan (`error_memory`)
* **Blok Entry:** Performa sangat tidak konsisten. Blok awal dan tengah sempat mencatat win rate tinggi (misal Entry #31-#50), namun hancur lebur pada blok **Entry #11-#20 ($-33.89)** dan **Entry #61-#70 ($-26.55)** akibat rentetan SL beruntun.
* **Pola Kesalahan Utama:** Berdasarkan `error_memory`, masalah terbesar terdeteksi pada:
  1. `rugi_saat_adx_kuat_ge_28` (**27 kasus**): Sistem keliru melakukan entry searah tren (kebanyakan SELL) saat ADX sangat kuat (>28), di mana kondisi tersebut justru rawan *reversal* tajam pada XAUUSD.
  2. `rugi_skor_tinggi_ge_75` (**21 kasus**): Skor probabilitas tinggi (>75) gagal menjadi jaminan karena indikator sering terjebak lagging pada tren jenuh (overextended).

---

### 2-3 Saran Penyetelan Parameter Konkret
1. **Filter Filter ADX Maksimal (Regulasi Tren Jenuh):** Tambahkan parameter batas atas ADX (misal: batasi atau abaikan sinyal jika `ADX > 45` atau `ADX >= 28`) untuk menghindari jebakan *false breakout* / pembalikan arah mendadak pada instrumen XAUUSD.
2. **Perketat Cut Rugi Dini (*Auto-Cut Unstable*):** Aktifkan dan sesuaikan ambang batas *cut loss* otomatis berdasarkan waktu atau *floating drawdown* (misal: jika posisi minus mencapai >$-2 USD dalam waktu <3 menit tanpa tanda pemulihan, paksa *auto-cut* daripada menunggu kena SL penuh di angka $-6 USD).
3. **Turunkan Ambang Skor & Perketat Validasi M15:** Karena skor tinggi (≥75) sering gagal, turunkan sensitivitas skor atau wajibkan konfirmasi arah *Candle Close* M15 yang lebih ketat (`wajib_kompak_m15 = true` dengan filter momentum tambahan) guna menyaring sinyal palsu di zona volatilitas tinggi.