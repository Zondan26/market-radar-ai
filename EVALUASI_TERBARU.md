# Laporan Evaluasi Riset Scalping Otomatis
- **Diperbarui:** 2026-11-25 17:00:42 WIB
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
Berikut adalah analisis singkat, padat, dan tuntas terhadap hasil evaluasi riset scalping otomatis:

###