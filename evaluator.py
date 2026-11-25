import csv
import json
import os
from datetime import datetime
from urllib import request

HISTORY_FILE = "trade_history.csv"
REPORT_FILE = "evaluasi_riset.json"
SUMMARY_MD = "EVALUASI_TERBARU.md"

# Ambang batas klasifikasi hasil (dalam USD untuk lot 0.01)
BIG_WIN_USD = 2.00
BIG_LOSS_USD = -2.00


def parse_float(val, default=0.0):
    try:
        return float(val)
    except (TypeError, ValueError):
        return default


def klasifikasi_hasil(profit_usd, exit_reason):
    if exit_reason == "UNSTABLE_PROFIT_GRAB":
        return "CUT_UNTUNG_TIDAK_STABIL" if profit_usd >= 0 else "CUT_RUGI_TIDAK_STABIL"
    if profit_usd >= BIG_WIN_USD:
        return "UNTUNG_BESAR"
    if profit_usd > 0:
        return "UNTUNG_KECIL"
    if profit_usd <= BIG_LOSS_USD:
        return "RUGI_BESAR"
    return "RUGI_KECIL"


def panggil_gemini_evaluasi(ringkasan_data):
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        return None

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-2.5-flash:generateContent?key={api_key}"
    )

    prompt = (
        "Kamu adalah analis evaluasi riset scalping otomatis (lot 0.01, M5+M15, XAUUSD & EURUSD). "
        "Analisis data riwayat trading berikut secara objektif, tajam, dan ringkas dalam bahasa Indonesia:\n"
        "1. Kenapa terjadi UNTUNG BESAR / UNTUNG KECIL dan RUGI BESAR / RUGI KECIL.\n"
        "2. Evaluasi durasi tahan (holding time) sampai TP, SL, atau auto-cut saat chart/berita tidak stabil.\n"
        "3. Berikan 2-3 saran penyetelan parameter konkret untuk perbaikan riset berikutnya.\n\n"
        f"DATA RINGKASAN:\n{json.dumps(ringkasan_data, ensure_ascii=False, indent=2)}"
    )

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.2},
    }

    req = request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=25) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            candidates = body.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts and "text" in parts[0]:
                    return parts[0]["text"].strip()
    except Exception as exc:
        return f"Catatan: Gagal memanggil Gemini API ({exc}). Evaluasi statistik lokal tetap tersimpan."

    return None


def jalankan_evaluasi():
    rows = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, mode="r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            for r in reader:
                rows.append(r)

    stats = {
        "total_trade": len(rows),
        "win_count": 0,
        "loss_count": 0,
        "win_rate_pct": 0.0,
        "net_profit_usd": 0.0,
        "kategori": {
            "UNTUNG_BESAR": 0,
            "UNTUNG_KECIL": 0,
            "RUGI_KECIL": 0,
            "RUGI_BESAR": 0,
            "CUT_UNTUNG_TIDAK_STABIL": 0,
            "CUT_RUGI_TIDAK_STABIL": 0,
        },
        "rata_durasi_menit": {
            "ke_tp": 0.0,
            "ke_sl": 0.0,
            "auto_cut_tanpa_tp_sl": 0.0,
        },
    }

    durasi_tp, durasi_sl, durasi_cut = [], [], []
    detail_catatan = []

    for r in rows:
        profit = parse_float(r.get("profit_usd", 0.0))
        durasi_detik = parse_float(r.get("holding_seconds", 0.0))
        durasi_menit = round(durasi_detik / 60.0, 2)
        exit_reason = (r.get("exit_reason") or "UNKNOWN").strip().upper()
        symbol = (r.get("symbol") or "").strip()
        direction = (r.get("direction") or "").strip()

        stats["net_profit_usd"] = round(stats["net_profit_usd"] + profit, 2)
        if profit > 0:
            stats["win_count"] += 1
        elif profit < 0:
            stats["loss_count"] += 1

        kat = klasifikasi_hasil(profit, exit_reason)
        if kat in stats["kategori"]:
            stats["kategori"][kat] += 1

        if "TP" in exit_reason and "EARLY" not in exit_reason and "UNSTABLE" not in exit_reason:
            durasi_tp.append(durasi_menit)
        elif "SL" in exit_reason:
            durasi_sl.append(durasi_menit)
        else:
            durasi_cut.append(durasi_menit)

        detail_catatan.append({
            "symbol": symbol,
            "direction": direction,
            "profit_usd": profit,
            "holding_minutes": durasi_menit,
            "exit_reason": exit_reason,
            "kategori": kat,
        })

    if stats["total_trade"] > 0:
        stats["win_rate_pct"] = round((stats["win_count"] / stats["total_trade"]) * 100.0, 2)
    if durasi_tp:
        stats["rata_durasi_menit"]["ke_tp"] = round(sum(durasi_tp) / len(durasi_tp), 2)
    if durasi_sl:
        stats["rata_durasi_menit"]["ke_sl"] = round(sum(durasi_sl) / len(durasi_sl), 2)
    if durasi_cut:
        stats["rata_durasi_menit"]["auto_cut_tanpa_tp_sl"] = round(sum(durasi_cut) / len(durasi_cut), 2)

    ai_analisis = panggil_gemini_evaluasi({
        "statistik": stats,
        "sampel_terakhir": detail_catatan[-25:],
    })

    waktu_wib = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    laporan = {
        "updated_at": waktu_wib,
        "statistik": stats,
        "ai_analisis": ai_analisis or "Belum ada data transaksi atau GEMINI_API_KEY belum disetel.",
    }

    with open(REPORT_FILE, mode="w", encoding="utf-8") as f:
        json.dump(laporan, f, ensure_ascii=False, indent=2)

    lines = [
        "# Laporan Evaluasi Riset Scalping Otomatis",
        f"- **Diperbarui:** {waktu_wib}",
        f"- **Total Transaksi:** {stats['total_trade']} | **Win Rate:** {stats['win_rate_pct']}% | **Net P/L:** ${stats['net_profit_usd']}",
        "",
        "## Klasifikasi Hasil",
        f"- Untung Besar: {stats['kategori']['UNTUNG_BESAR']}",
        f"- Untung Kecil: {stats['kategori']['UNTUNG_KECIL']}",
        f"- Rugi Kecil: {stats['kategori']['RUGI_KECIL']}",
        f"- Rugi Besar: {stats['kategori']['RUGI_BESAR']}",
        f"- Auto-Cut Untung (Chart/Berita Tidak Stabil): {stats['kategori']['CUT_UNTUNG_TIDAK_STABIL']}",
        f"- Auto-Cut Rugi (Chart/Berita Tidak Stabil): {stats['kategori']['CUT_RUGI_TIDAK_STABIL']}",
        "",
        "## Rata-Rata Durasi Tahan (Menit)",
        f"- Entry ke TP: {stats['rata_durasi_menit']['ke_tp']} menit",
        f"- Entry ke SL: {stats['rata_durasi_menit']['ke_sl']} menit",
        f"- Entry ke Auto-Cut (Tanpa TP/SL): {stats['rata_durasi_menit']['auto_cut_tanpa_tp_sl']} menit",
        "",
        "## Analisis Evaluasi AI",
        laporan["ai_analisis"],
    ]

    with open(SUMMARY_MD, mode="w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    jalankan_evaluasi()
