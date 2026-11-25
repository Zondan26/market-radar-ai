# Laporan Evaluasi Riset Scalping Otomatis
- **Diperbarui:** 2026-11-25 15:23:34 WIB
- **Koneksi Gemini API:** `TERSAMBUNG` — Berhasil terhubung ke Gemini API (models/gemini-3-flash-preview) | models=[models/gemini-2.5-flash, models/gemini-2.5-pro, models/gemini-2.5-flash-preview-tts, models/gemini-2.5-pro-preview-tts, models/gemma-4-26b-a4b-it, models/gemma-4-31b-it].
- **Total Entry:** 76 | **Win Rate:** 60.53% | **Net P/L:** $-53.26 | **Puncak Profit:** $5.48 (Erosi: 1071.9%)

## Perintah Aktif untuk MT5 (`strategy_command.json`)
- **Mode:** `CAUTIOUS` | **Min Peluang:** `63%` | **Max ADX Entry:** `30.0` | **Max Posisi (Lot 0.01):** `40`
- **Aturan ADX Tinggi:** Maks `2` entry, target cut `$0.3`, lock jika 2x SL hingga ADX M5 & M15 < `30.0`
- **Jarak Tambah ATR:** `0.35` | **Auto-Cut Goyah:** `AKTIF`
- **Alasan Arahan:** Rem tangan ADX>30 (maks 2 entry, target $0.3) aktif karena kerugian besar (Entry #61 - #70: $-26.55, Net=$-53.26, RugiBesar=24).

## Memori & Pembelajaran Kesalahan (`error_memory.json`)
- **Evaluasi Ke-:** 1 | **Streak Evaluasi Rugi:** 1
- **Pola Rugi Terekam:** ADX Kuat (>=30): `22` | ADX Lemah (<20): `0` | Tahan >=10m: `5` | Skor Tinggi (>=75): `21`

## Klasifikasi Tiap Entry
- Untung Besar: 20
- Untung Kecil: 19
- Rugi Kecil: 6
- Rugi Besar: 24
- Auto-Cut Untung (Chart/Berita Tidak Stabil): 7
- Auto-Cut Rugi (Chart/Berita Tidak Stabil): 0

## Rata-Rata Jeda Waktu / Durasi Tahan
- Entry ke TP: 38.23 menit
- Entry ke SL: 7.66 menit
- Entry ke Auto-Cut (Tanpa TP/SL): 2.09 menit

## Rekap Tiap 10 Kali Entry
- **Entry #1 - #10:** RUGI ($-2.68) | 9W / 1L | Rata-rata durasi: 1.83 menit
- **Entry #11 - #20:** RUGI ($-33.89) | 2W / 8L | Rata-rata durasi: 17.46 menit
- **Entry #21 - #30:** RUGI ($-19.63) | 4W / 6L | Rata-rata durasi: 1.2 menit
- **Entry #31 - #40:** UNTUNG ($18.58) | 9W / 1L | Rata-rata durasi: 2.18 menit
- **Entry #41 - #50:** UNTUNG ($16.02) | 9W / 1L | Rata-rata durasi: 1.84 menit
- **Entry #51 - #60:** RUGI ($-15.01) | 5W / 5L | Rata-rata durasi: 2.15 menit
- **Entry #61 - #70:** RUGI ($-26.55) | 3W / 7L | Rata-rata durasi: 2.09 menit
- **Entry #71 - #76:** UNTUNG ($9.9) | 5W / 1L | Rata-rata durasi: 6.86 menit

## Analisis Evaluasi AI
Berikut adalah analisis evaluasi riset scalping otomatis Anda:

### 1. Evaluasi Profit vs Rugi
*   **Performa Net:** Meskipun *win rate* cukup tinggi (60.53%), sistem mencatat kerugian bersih **-$53.26**. Ini menunjukkan masalah fatal pada *Risk-to-Reward Ratio*.
*   **Puncak & Erosi:** Puncak profit sangat rendah ($5.48), namun erosi profit mencapai **1071.9% ($58.74)**. Hal ini mengindikasikan sistem tidak mampu mempertahankan keuntungan kecil dan langsung terhantam *drawdown* besar.
*   **Auto-cut vs SL:** Terdapat 24 kejadian **RUGI_BESAR** yang mayoritas dipicu oleh `SL_HIT`. Mekanisme *auto-cut* (rata-rata 2.09 menit) jauh lebih cepat daripada SL (7.66 menit), namun frekuensi SL yang terkena pada kondisi ADX tinggi menghancurkan akumulasi profit dari *basket cut*.

### 2. Evaluasi Durasi Tahan
*   **Ke TP (38.23 menit):** Terlalu lama untuk strategi scalping M5. Semakin lama posisi tertahan, semakin besar risiko pembalikan harga (terlihat dari banyaknya *win* yang hanya berakhir jadi *untung kecil*).
*   **Ke SL (7.66 menit):** Sangat cepat. Ini menandakan entri seringkali dilakukan di "pucuk" atau saat momentum lawan sangat kuat, sehingga harga langsung menghantam SL.
*   **Auto-cut (2.09 menit):** Berhasil membatasi durasi pada kondisi tidak stabil, namun belum cukup kuat untuk menahan laju kerugian dari entri beruntun (*stacking*).

### 3. Evaluasi Blok 10 Entry & Error Memory
*   **Analisis Blok:** Blok #11-#20 (-$33.89) dan #61-#70 (-$26.55) adalah fase kehancuran akun. Di sisi lain, blok #31-#50 sempat profit stabil. Ini menunjukkan strategi hanya bekerja di pasar *sideways* dan hancur saat pasar *trending*.
*   **Pola Kesalahan (Error Memory):**
    *   **ADX Kuat (>=30):** Menjadi penyebab utama dengan **22 kali rugi**. Sistem mencoba melawan arus atau masuk saat volatilitas sedang memuncak.
    *   **Skor Tinggi (>=75):** Sebanyak **21 kali rugi** terjadi saat skor indikator sangat tinggi. Ini adalah jebakan *overbought/oversold* di mana indikator teknis terlihat "sempurna" padahal harga sedang dalam *strong trend*.

### 4. Saran Penyetelan Parameter Konkret
1.  **Perketat Filter ADX:** Ubah `max_adx_entry` dari 30.0 menjadi **25.0**. Data menunjukkan kerugian masif terjadi saat ADX > 30. Jangan melakukan entri baru jika ADX berada di zona *trending* kuat kecuali strategi diubah menjadi *trend-following*.
2.  **Reduksi Max Posisi:** Turunkan `max_posisi` dari 40 menjadi maksimal **10-15**. Dengan lot 0.01, akumulasi 40 posisi saat terjadi *floating* salah arah mempercepat penggerusan saldo secara eksponensial.
3.  **Optimasi Skor Entri:** Karena skor >= 75 sering gagal, tambahkan parameter **wajib konfirmasi volume** atau gunakan `min_probabilitas` yang lebih tinggi (misal: 70) namun dengan filter ADX yang lebih rendah untuk memastikan entri hanya terjadi pada konsolidasi yang sehat.