# Laporan Evaluasi Riset Scalping Otomatis
- **Diperbarui:** 2026-11-25 12:23:38 WIB
- **Koneksi Gemini API:** `TERSAMBUNG` — Berhasil terhubung ke Gemini API (models/gemini-flash-lite-latest) | models=[models/gemini-2.5-flash, models/gemini-2.5-pro, models/gemini-2.5-flash-preview-tts, models/gemini-2.5-pro-preview-tts, models/gemma-4-26b-a4b-it, models/gemma-4-31b-it].
- **Total Entry:** 21 | **Win Rate:** 52.38% | **Net P/L:** $-41.01

## Perintah Aktif untuk MT5 (`strategy_command.json`)
- **Mode:** `ACTIVE` | **Min Peluang:** `63%` | **Max Posisi (Lot 0.01):** `80`
- **Jarak Tambah ATR:** `0.3` | **Auto-Cut Goyah:** `AKTIF`
- **Alasan Arahan:** Evaluasi per 10 entry (Entry #21 - #21: $-4.44): sesuaikan ambang peluang ke 63% dan jarak ATR 0.30 agar kualitas entri lebih terjaga.

## Klasifikasi Tiap Entry
- Untung Besar: 1
- Untung Kecil: 3
- Rugi Kecil: 0
- Rugi Besar: 10
- Auto-Cut Untung (Chart/Berita Tidak Stabil): 7
- Auto-Cut Rugi (Chart/Berita Tidak Stabil): 0

## Rata-Rata Jeda Waktu / Durasi Tahan
- Entry ke TP: 38.23 menit
- Entry ke SL: 15.26 menit
- Entry ke Auto-Cut (Tanpa TP/SL): 0.52 menit

## Rekap Tiap 10 Kali Entry
- **Entry #1 - #10:** RUGI ($-2.68) | 9W / 1L | Rata-rata durasi: 1.83 menit
- **Entry #11 - #20:** RUGI ($-33.89) | 2W / 8L | Rata-rata durasi: 17.46 menit
- **Entry #21 - #21:** RUGI ($-4.44) | 0W / 1L | Rata-rata durasi: 3.12 menit

## Analisis Evaluasi AI
Berikut adalah analisis objektif dan ringkas berdasarkan riwayat evaluasi riset scalping otomatis (XAUUSD, Lot 0.01):

### 1. Evaluasi Tiap Entry & Perbandingan PnL
* **Penyebab Untung/Rugi:** Untung besar diraih saat tren bergerak searah dalam durasi lebih panjang (TP Hit). Untung kecil dan *auto-cut* profit terjadi karena fitur pengamanan pasar tidak stabil (*profit grab* cepat) untuk mengunci profit mini. Sebaliknya, **seluruh kerugian masuk kategori Rugi Besar** akibat terkena *Stop Loss* (SL Hit) saat posisi melawan arah tren atau volatilitas XAUUSD melonjak.
* **Perbandingan Rata-rata:** 
  * Rata-rata auto-cut/profit (termasuk untung kecil) sangat kecil, berkisar di bawah $1.00 per trade.
  * Rata-rata rugi SL jauh lebih besar, rata-rata mencapai -$5.00 hingga -$7.00 per trade. 
  * **Kesimpulan Risk-to-Reward Ratio (RRR) buruk:** 1 kemenangan besar atau beberapa profit mikro langsung habis oleh 1 kali kena SL. Inilah alasan utama Net PnL bernilai negatif (-$41.01).

### 2. Evaluasi Jeda Waktu (Holding Time)
* **Ke TP (Rata-rata 38.23 menit):** Waktu ideal bagi scalping M5+M15 untuk mencapai target terjauh saat tren stabil.
* **Ke SL (Rata-rata 15.26 menit):** Waktu tahan yang cukup lama untuk ukuran scalping, mengindikasikan bahwa sistem sering menahan posisi rugi terlalu lama berharap harga berbalik arah, alih-alih melakukan *cut loss* dini.
* **Auto-cut Tanpa TP/SL (Rata-rata 0.52 menit / ~31 detik):** Sangat cepat dan efektif mengamankan profit mikroskopis saat kondisi pasar/berita terdeteksi tidak stabil.

### 3. Evaluasi Blok 10 Entry, Skor M5/M15, & ADX
* **Blok #1 - #10 (Win: 9, Loss: 1 | Net: -$2.68):** Win rate tinggi (90%) didominasi *scalp* cepat dan *auto-cut*, namun tetap rugi tipis karena besarnya nilai SL pada 1 trade yang kalah. Skor M5 cenderung di kisaran 45 dengan ADX ~20 (pasar *sideways* / lemah).
* **Blok #11 - #20 (Win: 2, Loss: 8 | Net: -$33.89):** Penurunan performa drastis. Dominasi SL besar. Skor M5/M15 bervariasi (0–50), dengan ADX sempat tinggi (>38), menandakan sistem salah membaca arah saat tren kuat atau terjebak *fakeout*.
* **Blok #21 - #21 (Win: 0, Loss: 1 | Net: -$4.44):** Gagal total meskipun skor M5 (85) dan M15 (100) sangat tinggi dengan ADX 30.35, menunjukkan indikator teknikal masih bisa gagal menyaring titik *reversal* XAUUSD.

### 4. Saran Penyetelan Parameter Konkret
1. **Perketat Filter Tren & Batasi Indikator (Wajib Kompak):** Sesuai arahan sistem, naikkan ambang probabilitas minimal ke 63% dan optimalkan *wajib_kompak_m15* menjadi `true` untuk menghindari entry palsu saat skor tinggi tapi berujung SL.
2. **Terapkan Trailing Stop / Stop Loss Dinamis yang Ketat:** Mengingat rata-rata durasi kena SL adalah 15 menit dengan kerugian besar, turunkan batas toleransi rugi per transaksi (perpendek jarak SL atau aktifkan *trailing stop* lebih awal) agar rasionya tidak timpang dibanding *profit grab*.
3. **Evaluasi Jarak ATR:** Pertahankan jarak tambah ATR di angka `0.30` untuk memberikan ruang nafas yang lebih ideal bagi volatilitas XAUUSD, sehingga entry tidak terlalu dekat dengan noise market M5.