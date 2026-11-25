# Laporan Evaluasi Riset Scalping Otomatis
- **Diperbarui:** 2026-11-25 12:17:55 WIB
- **Koneksi Gemini API:** `TERSAMBUNG` — Berhasil terhubung ke Gemini API (models/gemini-flash-lite-latest) | models=[models/gemini-2.5-flash, models/gemini-2.5-pro, models/gemini-2.5-flash-preview-tts, models/gemini-2.5-pro-preview-tts, models/gemma-4-26b-a4b-it, models/gemma-4-31b-it].
- **Total Entry:** 19 | **Win Rate:** 57.89% | **Net P/L:** $-32.13

## Perintah Aktif untuk MT5 (`strategy_command.json`)
- **Mode:** `CAUTIOUS` | **Min Peluang:** `66%` | **Max Posisi (Lot 0.01):** `50`
- **Jarak Tambah ATR:** `0.35` | **Auto-Cut Goyah:** `AKTIF`
- **Alasan Arahan:** Entry #11 - #19 merugi (2W/7L, $-29.45): naikkan syarat peluang ke 66% dan perlebar jarak entri.

## Klasifikasi Tiap Entry
- Untung Besar: 1
- Untung Kecil: 3
- Rugi Kecil: 0
- Rugi Besar: 8
- Auto-Cut Untung (Chart/Berita Tidak Stabil): 7
- Auto-Cut Rugi (Chart/Berita Tidak Stabil): 0

## Rata-Rata Jeda Waktu / Durasi Tahan
- Entry ke TP: 38.23 menit
- Entry ke SL: 18.29 menit
- Entry ke Auto-Cut (Tanpa TP/SL): 0.52 menit

## Rekap Tiap 10 Kali Entry
- **Entry #1 - #10:** RUGI ($-2.68) | 9W / 1L | Rata-rata durasi: 1.83 menit
- **Entry #11 - #19:** RUGI ($-29.45) | 2W / 7L | Rata-rata durasi: 19.05 menit

## Analisis Evaluasi AI
Berikut adalah hasil analisis obyektif dan ringkas terhadap riwayat trading otomatis (XAUUSD, lot 0.01):

### 1. Evaluasi Tiap Entry & Perbandingan Profit vs Loss
* **Untung Besar / Kecil:** Keuntungan besar (Entry #12) tercapai berkat *holding time* optimal (38 menit) saat tren selaras. Untung kecil dan *auto-cut* profit cepat terjadi karena sistem memangkas posisi dalam hitungan detik (rata-rata 0.52 menit) demi mengamankan saldo di pasar yang tidak stabil.
* **Rugi Besar:** Seluruh 8 posisi rugi dikategorikan sebagai "Rugi Besar" karena terkena *Stop Loss* (SL). 
* **Perbandingan:** Terjadi ketimpangan *Risk-to-Reward Ratio* yang ekstrem. Rata-rata *auto-cut* profit sangat kecil (kisaran $0.21 - $0.85), sedangkan rata-rata rugi SL sangat besar (kisaran $-5 hingga $-7 per posisi). Satu kali SL langsung