# Laporan Evaluasi Riset Scalping Otomatis
- **Diperbarui:** 2026-11-25 22:36:41 WIB
- **Koneksi Gemini API:** `TERSAMBUNG` — Berhasil terhubung ke Gemini API (models/gemini-3.5-transcribe) | models=[models/gemini-2.5-flash, models/gemini-2.5-pro, models/gemini-2.5-flash-preview-tts, models/gemini-2.5-pro-preview-tts, models/gemma-4-26b-a4b-it, models/gemma-4-31b-it].
- **Total Entry:** 118 | **Win Rate:** 62.71% | **Net P/L:** $-59.31 | **Puncak Profit:** $5.48 (Erosi: 1182.3%)

## Perintah Aktif untuk MT5 (`strategy_command.json`)
- **Mode:** `CAUTIOUS` | **Min Peluang:** `63%` | **Cut Profit:** `10.0% - 15.0%` | **Max Posisi (Lot 0.01):** `500`
- **Aturan Saldo:** Jeda `60 menit` jika saldo turun `>=10.0%` dari saldo tertinggi, lalu lanjut entry otomatis
- **Jarak Tambah ATR:** `0.35` | **Auto-Cut Goyah:** `AKTIF`
- **Alasan Arahan:** Cut profit 10%-15% | Entry terbuka selama sinyal candle memenuhi | Jeda 1 jam bila saldo turun >=10% puncak | Mode CAUTIOUS (Entry #101 - #110: $35.42, Net=$-59.31, RugiBesar=36): min peluang 63%, ATR 0.35.

## Memori & Pembelajaran Kesalahan (`error_memory.json`)
- **Evaluasi Ke-:** 1 | **Streak Evaluasi Rugi:** 1
- **Pola Rugi Terekam:** Tahan >=10m: `8` | Skor Tinggi (>=75): `35` | Cut Tidak Stabil: `0`

## Klasifikasi Tiap Entry
- Untung Besar: 28
- Untung Kecil: 25
- Rugi Kecil: 8
- Rugi Besar: 36
- Auto-Cut Untung (Chart/Berita Tidak Stabil): 21
- Auto-Cut Rugi (Chart/Berita Tidak Stabil): 0

## Rata-Rata Jeda Waktu / Durasi Tahan
- Entry ke TP: 13.19 menit
- Entry ke SL: 7.93 menit
- Entry ke Auto-Cut (Tanpa TP/SL): 2.72 menit

## Rekap Tiap 10 Kali Entry
- **Entry #1 - #10:** RUGI ($-2.68) | 9W / 1L | Rata-rata durasi: 1.83 menit
- **Entry #11 - #20:** RUGI ($-33.89) | 2W / 8L | Rata-rata durasi: 17.46 menit
- **Entry #21 - #30:** RUGI ($-19.63) | 4W / 6L | Rata-rata durasi: 1.2 menit
- **Entry #31 - #40:** UNTUNG ($18.58) | 9W / 1L | Rata-rata durasi: 2.18 menit
- **Entry #41 - #50:** UNTUNG ($16.02) | 9W / 1L | Rata-rata durasi: 1.84 menit
- **Entry #51 - #60:** RUGI ($-15.01) | 5W / 5L | Rata-rata durasi: 2.15 menit
- **Entry #61 - #70:** RUGI ($-26.55) | 3W / 7L | Rata-rata durasi: 2.09 menit
- **Entry #71 - #80:** RUGI ($-0.41) | 7W / 3L | Rata-rata durasi: 6.17 menit
- **Entry #81 - #90:** RUGI ($-17.79) | 6W / 4L | Rata-rata durasi: 7.82 menit
- **Entry #91 - #100:** UNTUNG ($3.74) | 6W / 4L | Rata-rata durasi: 6.42 menit
- **Entry #101 - #110:** UNTUNG ($35.42) | 10W / 0L | Rata-rata durasi: 2.4 menit
- **Entry #111 - #118:** RUGI ($-17.11) | 4W / 4L | Rata-rata durasi: 4.37 menit

## Analisis Evaluasi AI
