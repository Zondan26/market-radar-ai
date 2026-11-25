# Laporan Evaluasi Riset Scalping Otomatis
- **Diperbarui:** 2026-11-25 12:34:01 WIB
- **Koneksi Gemini API:** `TERSAMBUNG` — Berhasil terhubung ke Gemini API (models/gemini-flash-lite-latest) | models=[models/gemini-2.5-flash, models/gemini-2.5-pro, models/gemini-2.5-flash-preview-tts, models/gemini-2.5-pro-preview-tts, models/gemma-4-26b-a4b-it, models/gemma-4-31b-it].
- **Total Entry:** 30 | **Win Rate:** 50.0% | **Net P/L:** $-56.2

## Perintah Aktif untuk MT5 (`strategy_command.json`)
- **Mode:** `ACTIVE` | **Min Peluang:** `63%` | **Max Posisi (Lot 0.01):** `80`
- **Jarak Tambah ATR:** `0.3` | **Auto-Cut Goyah:** `AKTIF`
- **Alasan Arahan:** Evaluasi per 10 entry (Entry #21 - #30: $-19.63): sesuaikan ambang peluang ke 63% dan jarak ATR 0.30 agar kualitas entri lebih terjaga.

## Klasifikasi Tiap Entry
- Untung Besar: 3
- Untung Kecil: 5
- Rugi Kecil: 0
- Rugi Besar: 15
- Auto-Cut Untung (Chart/Berita Tidak Stabil): 7
- Auto-Cut Rugi (Chart/Berita Tidak Stabil): 0

## Rata-Rata Jeda Waktu / Durasi Tahan
- Entry ke TP: 38.23 menit
- Entry ke SL: 10.65 menit
- Entry ke Auto-Cut (Tanpa TP/SL): 0.5 menit

## Rekap Tiap 10 Kali Entry
- **Entry #1 - #10:** RUGI ($-2.68) | 9W / 1L | Rata-rata durasi: 1.83 menit
- **Entry #11 - #20:** RUGI ($-33.89) | 2W / 8L | Rata-rata durasi: 17.46 menit
- **Entry #21 - #30:** RUGI ($-19.63) | 4W / 6L | Rata-rata durasi: 1.2 menit

## Analisis Evaluasi AI
Berikut adalah analisis objektif dan ringkas berdasarkan riwayat evaluasi riset scalping otomatis XAUUSD & EURUSD:

### 1. Evaluasi Tiap Entry (Profit vs Loss)
*   **Penyebab Untung (Besar/Kecil):** Keuntungan mayoritas diperoleh melalui *profit taking* cepat (`UNSTABLE_PROFIT_GRAB` atau `BASKET_PROFIT_CUT`) dalam durasi sangat singkat saat harga berfluktuasi searah, serta beberapa entry sukses menyentuh TP (`TP_HIT` rata-rata di 38.23 menit).
*   **Penyebab Rugi (Besar):** 100% kerugian dikategorikan sebagai **Rugi Besar** (`SL_HIT`). Tidak ada rugi kecil karena sistem langsung memotong posisi pada batas Stop Loss (SL) statis yang relatif lebar dibanding target *auto-cut* profit.
*   **Perbandingan Auto-Cut Profit vs SL:** 
    *   Rata-rata profit dari *auto-cut* (misal: *unstable profit grab* / *basket profit*) sangat kecil (berkisar antara $0.20 – $3.50).
    *   Sebaliknya, rata-rata kerugian saat terkena SL sangat konsisten dan besar (berkisar di angka **-$4.30 hingga -$7.23**). Rasio risk-to-reward sangat timpang, di mana satu kali kena SL dapat menghapus hasil dari 3-5 kali entry profit kecil.

### 2. Evaluasi Jeda Waktu (Holding Time)
*   **Ke TP:** Rata-rata **38.23 menit**. Waktu tahan yang cukup lama untuk ukuran scalping, menunjukkan rentang target profit yang agak jauh dari titik entry.
*   **Ke SL:** Rata-rata **10.65 menit**. Cukup cepat terseret ke area negatif, menandakan momentum sering berbalik arah melawan posisi (terutama dominasi posisi SELL saat market XAUUSD melakukan koreksi naik/spike).
*   **Kondisi Tidak Stabil:** Fitur `auto_cut_unstable` bekerja sangat agresif dengan rata-rata durasi hanya **0.5 menit** (30 detik). Ini efektif mengamankan modal dari whipsaw pasar, namun membatasi potensi profit besar.

### 3. Evaluasi Per Blok 10 Entry & Skor Indikator
*   **Blok 1 #1 - #10 (Win: 9, Loss: 1 | Net: -$2.68 | Durasi: 1.83m):** 
    *   Win rate sangat tinggi karena didominasi *auto-cut* cepat. Namun secara finansial tetap rugi tipis akibat besarnya dampak 1 kali SL.
    *   *Skor & ADX:* Skor M5/M15 rendah (M5: ~45, M15: ~20) dengan ADX di kisaran 20-27 (pasar *ranging* / lemah).
*   **Blok 2 #11 - #20 (Win: 2, Loss: 8 | Net: -$33.89 | Durasi: 17.46m):** 
    *   Blok terburuk dengan *drawdown* terbesar. Sistem terjebak menahan posisi SELL terlalu lama saat tren naik melawan arah (banyak SL tersentuh di atas 10-28 menit).
    *   *Skor & ADX:* ADX meningkat (>30 - 43), menandakan pasar mulai masuk fase *trending* kuat yang menembus batas SL.
*   **Blok 3 #21 - #30 (Win: 4, Loss: 6 | Net: -$19.63 | Durasi: 1.20m):** 
    *   Mulai membaik dari sisi durasi (kembali ke scalping kilat 1.2 menit), namun rasio kekalahan masih mendominasi sehingga net PnL tetap negatif.
    *   *Skor & ADX:* Skor M5/M15 tinggi (85-100) dan ADX stabil di ~29. Tingginya skor belum menjamin akurasi karena arah tren masih mudah berbalik.

---

### 4. Saran Penyetelan Parameter Konkret
1.  **Perketat Filter Tren (ADX & Score M15):** 
    Naikkan ambang batas minimal ADX ke atas **30.0** dan wajibkan keselarasan *score* M15 yang lebih ketat (>75) sebelum entry. Hindari membuka posisi SELL beruntun saat skor M15 menunjukkan kekuatan *bullish* yang dominan.
2.  **Optimalkan Risk-to-Reward Ratio (Terapkan Trailing SL / Tightening SL):** 
    Karena rata-rata kerugian SL jauh lebih besar daripada profit *auto-cut*, percepat pengaktifan *Trailing Stop* atau perkecil jarak SL awal agar kerugian per transaksi bisa ditekan di bawah -$3.00.
3.  **Evaluasi Ulang Jeda Waktu *Auto-Cut* & *Basket Profit*:** 
    Pertahankan fitur `auto_cut_unstable` di bawah 1 menit karena terbukti menyelamatkan modal dari volatilitas ekstrem XAUUSD, namun naikkan batas minimum `min_untung_cut_usd` secara bertahap (misal ke $0.50)