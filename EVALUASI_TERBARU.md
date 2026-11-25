# Laporan Evaluasi Riset Scalping Otomatis
- **Diperbarui:** 2026-11-25 12:41:55 WIB
- **Koneksi Gemini API:** `TERSAMBUNG` — Berhasil terhubung ke Gemini API (models/gemini-flash-lite-latest) | models=[models/gemini-2.5-flash, models/gemini-2.5-pro, models/gemini-2.5-flash-preview-tts, models/gemini-2.5-pro-preview-tts, models/gemma-4-26b-a4b-it, models/gemma-4-31b-it].
- **Total Entry:** 37 | **Win Rate:** 56.76% | **Net P/L:** $-43.04

## Perintah Aktif untuk MT5 (`strategy_command.json`)
- **Mode:** `ACTIVE` | **Min Peluang:** `63%` | **Max Posisi (Lot 0.01):** `80`
- **Jarak Tambah ATR:** `0.3` | **Auto-Cut Goyah:** `AKTIF`
- **Alasan Arahan:** Evaluasi per 10 entry (Entry #31 - #37: $13.16): sesuaikan ambang peluang ke 63% dan jarak ATR 0.30 agar kualitas entri lebih terjaga.

## Klasifikasi Tiap Entry
- Untung Besar: 7
- Untung Kecil: 7
- Rugi Kecil: 1
- Rugi Besar: 15
- Auto-Cut Untung (Chart/Berita Tidak Stabil): 7
- Auto-Cut Rugi (Chart/Berita Tidak Stabil): 0

## Rata-Rata Jeda Waktu / Durasi Tahan
- Entry ke TP: 38.23 menit
- Entry ke SL: 10.65 menit
- Entry ke Auto-Cut (Tanpa TP/SL): 1.11 menit

## Rekap Tiap 10 Kali Entry
- **Entry #1 - #10:** RUGI ($-2.68) | 9W / 1L | Rata-rata durasi: 1.83 menit
- **Entry #11 - #20:** RUGI ($-33.89) | 2W / 8L | Rata-rata durasi: 17.46 menit
- **Entry #21 - #30:** RUGI ($-19.63) | 4W / 6L | Rata-rata durasi: 1.2 menit
- **Entry #31 - #37:** UNTUNG ($13.16) | 6W / 1L | Rata-rata durasi: 2.33 menit

## Analisis Evaluasi AI
Berikut adalah analisis objektif dan ringkas berdasarkan data riwayat trading otomatis XAUUSD (Lot 0.01):

### 1. Evaluasi Tiap Entry & Perbandingan Profit vs Loss
* **Penyebab Untung (Besar/Kecil):** Untung besar diraih saat tren bergerak searah posisi SELL (terutama lewat mekanisme *Basket Profit Cut* atau TP murni di durasi ideal). Untung kecil umumnya terjadi karena aksi *early profit-taking* saat volatilitas mulai meragukan.
* **Penyebab Rugi (Besar/Kecil):** Dominasi rugi besar (15 kasus) terjadi karena harga melawan arah posisi SELL cukup jauh hingga mengenai Stop Loss (SL) fisik, atau tertahan di tren naik yang kuat (terlihat dari ADX > 35 pada beberapa entri rugi).
* **Perbandingan Auto-Cut Profit vs SL:** Rata-rata rugi akibat SL jauh lebih besar secara nominal dolar dibandingkan rata-rata profit per trade. Hal ini membuat total net profit bernilai negatif meskipun *win rate* secara keseluruhan berada di angka **56.76%**.

### 2. Evaluasi Jeda Waktu (Holding Time)
* **Ke TP (38.23 menit):** Waktu tunggu yang cukup panjang, mengindikasikan target profit di-setting agak jauh atau pergerakan harga yang lambat pada pair XAUUSD.
* **Ke SL (10.65 menit):** Cukup cepat tertjemput, menunjukkan risiko terseret tren berlawanan langsung direspon SL tanpa menunggu terlalu lama.
* **Auto-Cut / Unstable (1.11 menit):** Fitur pengamanan darurat bekerja sangat cepat (rata-rata 1 menit) saat chart tidak stabil, efektif mencegah kerugian yang lebih dalam pada kondisi market yang tidak menentu.

### 3. Evaluasi Blok 10 Entry, Skor M5/M15, & ADX
* **Blok #1 - #10 (Win 9, Loss 1 | Net: -$2.68):** Walaupun win rate tinggi, keuntungan per trade terlalu tipis untuk menutupi biaya/spread. Skor M5/M15 cenderung rendah (di bawah 45).
* **Blok #11 - #20 (Win 2, Loss 8 | Net: -$33.89):** Blok terburuk. Mayoritas terseret SL akibat memaksakan entry saat skor M15 rendah (0–20) dan ADX tinggi (>38) yang menandakan market sedang trending kuat melawan posisi SELL.
* **Blok #21 - #30 (Win 4, Loss 6 | Net: -$19.63):** Mulai menggunakan filter skor M5/M15 lebih tinggi (70-100), namun masih banyak terkena SL cepat akibat volatilitas emas.
* **Blok #31 - #37 (Win 6, Loss 1 | Net: +$13.16):** Blok paling sehat. Skor M5 konsisten di atas 85, M15 di angka 85, dan ADX stabil di kisaran 29–34. Kinerja membaik signifikan.

---

### 4. Saran Penyetelan Parameter Konkret
1. **Perketat Filter Skor & Tren (M15 & ADX):** Wajibkan skor M15 minimal 70 dan batasi ADX maksimal di bawah 32 untuk menghindari *entry* saat market sedang *strong trending* (mencegah kasus rugi besar seperti di Blok #2).
2. **Optimalkan Rasio Risk-to-Reward (RRR):** Naikkan target *Smart Early TP* atau perketat jarak SL (misal memperlebar jarak ATR tambah sedikit atau mempercepat *Trailing Stop*) agar rata-rata profit bisa mengimbangi besarnya nilai SL.
3. **Pertahankan Validasi Peluang 63%:** Sesuai arahan terbaru, pertahankan ambang peluang di angka 63% dengan aturan wajib kompak M15 agar kualitas entri hanya tersaring pada probabilitas tinggi saja.