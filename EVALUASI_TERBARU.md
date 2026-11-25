# Laporan Evaluasi Riset Scalping Otomatis
- **Diperbarui:** 2026-11-25 13:13:25 WIB
- **Koneksi Gemini API:** `TERSAMBUNG` — Berhasil terhubung ke Gemini API (models/gemini-flash-lite-latest) | models=[models/gemini-2.5-flash, models/gemini-2.5-pro, models/gemini-2.5-flash-preview-tts, models/gemini-2.5-pro-preview-tts, models/gemma-4-26b-a4b-it, models/gemma-4-31b-it].
- **Total Entry:** 65 | **Win Rate:** 58.46% | **Net P/L:** $-68.06

## Perintah Aktif untuk MT5 (`strategy_command.json`)
- **Mode:** `CAUTIOUS` | **Min Peluang:** `63%` | **Max Posisi (Lot 0.01):** `40`
- **Jarak Tambah ATR:** `0.35` | **Auto-Cut Goyah:** `AKTIF`
- **Alasan Arahan:** Belajar dari kesalahan (Entry #51 - #60: $-15.01, Net=$-68.06, RugiBesar=24): mode CAUTIOUS, min peluang 63%, max posisi 40, ATR 0.35.

## Memori & Pembelajaran Kesalahan (`error_memory.json`)
- **Evaluasi Ke-:** 1 | **Streak Evaluasi Rugi:** 1
- **Pola Rugi Terekam:** ADX Kuat (>=28): `24` | ADX Lemah (<20): `0` | Tahan >=10m: `5` | Skor Tinggi (>=75): `19`

## Klasifikasi Tiap Entry
- Untung Besar: 16
- Untung Kecil: 15
- Rugi Kecil: 3
- Rugi Besar: 24
- Auto-Cut Untung (Chart/Berita Tidak Stabil): 7
- Auto-Cut Rugi (Chart/Berita Tidak Stabil): 0

## Rata-Rata Jeda Waktu / Durasi Tahan
- Entry ke TP: 38.23 menit
- Entry ke SL: 7.66 menit
- Entry ke Auto-Cut (Tanpa TP/SL): 1.45 menit

## Rekap Tiap 10 Kali Entry
- **Entry #1 - #10:** RUGI ($-2.68) | 9W / 1L | Rata-rata durasi: 1.83 menit
- **Entry #11 - #20:** RUGI ($-33.89) | 2W / 8L | Rata-rata durasi: 17.46 menit
- **Entry #21 - #30:** RUGI ($-19.63) | 4W / 6L | Rata-rata durasi: 1.2 menit
- **Entry #31 - #40:** UNTUNG ($18.58) | 9W / 1L | Rata-rata durasi: 2.18 menit
- **Entry #41 - #50:** UNTUNG ($16.02) | 9W / 1L | Rata-rata durasi: 1.84 menit
- **Entry #51 - #60:** RUGI ($-15.01) | 5W / 5L | Rata-rata durasi: 2.15 menit
- **Entry #61 - #65:** RUGI ($-31.45) | 0W / 5L | Rata-rata durasi: 2.71 menit

## Analisis Evaluasi AI
Berikut adalah analisis evaluasi riset scalping otomatis (XAUUSD & EURUSD) secara objektif, bertahap, dan ringkas:

### 1. Evaluasi Tiap Entry & Perbandingan Profit vs Loss
*   **Penyebab Untung (Besar/Kecil):** Sebagian besar keuntungan diraih melalui mekanisme `BASKET_PROFIT_CUT` pada kondisi tren yang stabil. Untung besar terjadi ketika momentum searah dengan durasi singkat (1-2 menit), sedangkan untung kecil dicapai saat target profit tercapai lebih cepat atau dipotong dini (`smart_early_tp`).
*   **Penyebab Rugi (Besar/Kecil):** Seluruh kerugian besar (`RUGI_BESAR`, 24 kejadian) disebabkan oleh tersentuhnya Stop Loss (`SL_HIT`) akibat perlawanan arah harga yang kuat secara tiba-tiba.
*   **Perbandingan Profit vs Rugi:** Terjadi asimetri negatif yang signifikan. Rata-rata *auto-cut profit* jauh lebih kecil dibandingkan rata-rata kerugian saat terkena SL (Loss per SL rata-rata berkisar di angka -$6.00+, sedangkan profit bersih kumulatif tergerus di angka -$68.06 meski *win rate* mencapai 58.46%).

### 2. Evaluasi Jeda Waktu (Holding Time)
*   **Ke TP / Basket Profit:** Rata-rata durasi ke TP adalah **38.23 menit** (untuk TP konvensional) atau sangat cepat (1-3 menit) untuk *basket cut*, menunjukkan sistem efektif mengamankan profit kilat.
*   **Ke SL:** Rata-rata durasi kena SL adalah **7.66 menit**, yang berarti posisi rugi cenderung dibiarkan lebih lama dibanding target scalping ideal.
*   **Kondisi Tidak Stabil:** Auto-cut tanpa TP/SL sangat cepat (**1.45 menit**), menunjukkan fitur proteksi saat market tidak stabil sudah berfungsi memotong potensi kerugian lebih dalam.

### 3. Evaluasi Blok 10 Entry & Pola Kesalahan (*Error Memory*)
*   **Performa per Blok:** Performa sangat fluktuatif. Blok awal (#1-#20) dan akhir (#51-#65) mencatatkan kerugian berat, sementara blok tengah (#31-#50) sempat konsisten membukukan profit. 5 entry terakhir (#61-#65) mengalami kekalahan mutlak (0% win).
*   **Pola Kesalahan:** Memori kesalahan mencatat **24 kasus rugi saat ADX kuat ($\ge 28$)** dan **19 kasus rugi saat skor tinggi ($\ge 75$)**. 
*   **Status Perbaikan:** Pola kesalahan **belum membaik dan masih berulang**, terbukti dari entry #53 hingga #65 di mana sistem terus melakukan entry SELL saat ADX sangat tinggi (>51 hingga 58) yang berujung pada beruntunnya *SL Hit* akibat kondisi market yang ternyata sedang *trend strong/reversal*.

### 4. Saran Penyetelan Parameter Konkret
1.  **Filter ADX Maksimal (Regulasi Tren):** Tambahkan batas atas ADX (misal: `max_adx: 45.0`). Jika ADX di atas 45, hentikan aksi *scalping* karena pasar terlalu liar atau berisiko tinggi mengalami *exhaustion/reversal* tajam yang menembus SL.
2.  **Perketat Manajemen Risiko (Risk-Reward Ratio):** Sesuaikan jarak SL agar lebih ketat atau percepat *auto-cut* pada posisi yang melawan tren, mengingat kerugian per SL (`-$6`) jauh lebih besar daripada rata-rata profit bersih per entry.
3.  **Evaluasi Skor Validasi M5+M15:** Naikkan ambang batas skor (*min_probabilitas*) dari 63% menjadi minimal 70-75% khusus untuk instrumen XAUUSD guna menghindari sinyal palsu saat volatilitas tinggi.