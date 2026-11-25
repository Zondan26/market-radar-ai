import csv
import json
import os
from datetime import datetime, timedelta, timezone
from urllib import request

HISTORY_FILE = "trade_history.csv"
REPORT_FILE = "evaluasi_riset.json"
SUMMARY_MD = "EVALUASI_TERBARU.md"
COMMAND_FILE = "strategy_command.json"

BIG_WIN_USD = 2.00
BIG_LOSS_USD = -2.00
DEFAULT_MAX_POSISI = 100


def parse_float(val, default=0.0):
    try:
        return float(val)
    except (TypeError, ValueError):
        return default


def parse_int(val, default=0):
    try:
        return int(float(val))
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


def susun_blok_10_entry(detail_catatan):
    blok_list = []
    total = len(detail_catatan)
    for start_idx in range(0, total, 10):
        chunk = detail_catatan[start_idx : start_idx + 10]
        win_c = sum(1 for x in chunk if x["profit_usd"] > 0)
        loss_c = sum(1 for x in chunk if x["profit_usd"] < 0)
        net_pnl = round(sum(x["profit_usd"] for x in chunk), 2)
        avg_hold = round(sum(x["holding_minutes"] for x in chunk) / len(chunk), 2)
        status_blok = "UNTUNG" if net_pnl > 0 else ("RUGI" if net_pnl < 0 else "IMPAS")
        blok_list.append({
            "blok": f"Entry #{start_idx + 1} - #{start_idx + len(chunk)}",
            "jumlah_entry": len(chunk),
            "win": win_c,
            "loss": loss_c,
            "net_pnl_usd": net_pnl,
            "rata_durasi_menit": avg_hold,
            "hasil_blok": status_blok,
        })
    return blok_list


def susun_perintah_otomatis(stats, blok_10, waktu_wib_str):
    cmd = {
        "updated_wib": waktu_wib_str,
        "mode_trading": "ACTIVE",
        "alasan_arahan": "Mode aktif: eksekusi tanpa jeda selama syarat terpenuhi, lot terkunci 0.01, auto-cut aktif.",
        "min_probabilitas": 60,
        "wajib_kompak_m15": True,
        "max_posisi": DEFAULT_MAX_POSISI,
        "jarak_tambah_atr": 0.25,
        "auto_cut_unstable": True,
        "min_untung_cut_usd": 0.10,
        "smart_early_tp": True,
        "min_rasio_early_tp": 0.50,
        "max_sl_harian": 1000,
        "max_rugi_saldo_persen": 60.0,
    }

    total = stats["total_trade"]
    if total < 10:
        cmd["alasan_arahan"] = (
            f"Sampel baru {total} entry (belum genap 1 blok 10 entry): pertahankan batas peluang 60%, "
            f"maksimal {DEFAULT_MAX_POSISI} posisi (lot 0.01), dan auto-cut saat chart/berita tidak stabil."
        )
        return cmd

    blok_terakhir = blok_10[-1]
    win_rate = stats["win_rate_pct"]
    rug_besar = stats["kategori"]["RUGI_BESAR"]

    if blok_terakhir["net_pnl_usd"] < 0 and blok_terakhir["loss"] >= 7:
        cmd["mode_trading"] = "CAUTIOUS"
        cmd["min_probabilitas"] = 66
        cmd["max_posisi"] = 50
        cmd["jarak_tambah_atr"] = 0.35
        cmd["alasan_arahan"] = (
            f"{blok_terakhir['blok']} merugi ({blok_terakhir['win']}W/{blok_terakhir['loss']}L, "
            f"${blok_terakhir['net_pnl_usd']}): naikkan syarat peluang ke 66% dan perlebar jarak entri."
        )
    elif win_rate >= 65.0 and rug_besar <= 2:
        cmd["mode_trading"] = "ACTIVE"
        cmd["min_probabilitas"] = 60
        cmd["max_posisi"] = DEFAULT_MAX_POSISI
        cmd["jarak_tambah_atr"] = 0.25
        cmd["alasan_arahan"] = (
            f"{blok_terakhir['blok']} {blok_terakhir['hasil_blok']} (${blok_terakhir['net_pnl_usd']}) "
            f"dengan win rate {win_rate}%: pertahankan mode aktif penuh (hingga {DEFAULT_MAX_POSISI} posisi)."
        )
    else:
        cmd["mode_trading"] = "ACTIVE"
        cmd["min_probabilitas"] = 63
        cmd["max_posisi"] = 80
        cmd["jarak_tambah_atr"] = 0.30
        cmd["alasan_arahan"] = (
            f"Evaluasi per 10 entry ({blok_terakhir['blok']}: ${blok_terakhir['net_pnl_usd']}): "
            "sesuaikan ambang peluang ke 63% dan jarak ATR 0.30 agar kualitas entri lebih terjaga."
        )

    return cmd


def cari_model_gemini_aktif(api_key):
    kandidat = [
        ("v1beta", "models/gemini-2.5-flash"),
        ("v1beta", "models/gemini-2.5-flash-lite"),
        ("v1beta", "models/gemini-2.0-flash"),
        ("v1beta", "models/gemini-flash-latest"),
    ]
    daftar_nama = []
    list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    try:
        req = request.Request(list_url, method="GET")
        with request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            for m in data.get("models", []):
                methods = m.get("supportedGenerationMethods", [])
                name = m.get("name", "")
                if "generateContent" in methods and name:
                    daftar_nama.append(name)
    except Exception as exc:
        return kandidat, f"list_err={exc}"

    prioritas = []
    for p in [
        "models/gemini-2.5-flash",
        "models/gemini-2.5-flash-lite",
        "models/gemini-2.0-flash",
        "models/gemini-flash-latest",
    ]:
        if p in daftar_nama:
            prioritas.append(("v1beta", p))

    for name in daftar_nama:
        if ("v1beta", name) not in prioritas:
            prioritas.append(("v1beta", name))

    info_list = ", ".join(daftar_nama[:6]) if daftar_nama else "kosong"
    return (prioritas if prioritas else kandidat), f"models=[{info_list}]"


def panggil_gemini_evaluasi(ringkasan_data):
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        return {
            "status": "BELUM_ADA_API_KEY",
            "keterangan": "GEMINI_API_KEY belum terbaca di environment GitHub Actions.",
            "teks": "API Key Gemini belum terpasang; evaluasi statistik lokal tetap tersimpan.",
        }

    kandidat_list, info_model = cari_model_gemini_aktif(api_key)

    prompt = (
        "Kamu adalah analis evaluasi riset scalping otomatis (lot 0.01, M5+M15, XAUUSD & EURUSD). "
        "Analisis riwayat trading berikut secara objektif dan ringkas dalam bahasa Indonesia:\n"
        "1. Evaluasi tiap entry: kenapa muncul UNTUNG BESAR / UNTUNG KECIL dan RUGI BESAR / RUGI KECIL, "
        "termasuk perbandingan rata-rata auto-cut profit terhadap rata-rata rugi SL.\n"
        "2. Evaluasi jeda waktu (holding time) sampai TP, SL, atau auto-cut saat chart/berita tidak stabil.\n"
        "3. Evaluasi hasil tiap blok 10 kali entry (untung/rugi) serta skor M5/M15 & ADX saat entry.\n"
        "4. Berikan 2-3 saran penyetelan parameter konkret untuk perbaikan berikutnya.\n\n"
        f"DATA EVALUASI:\n{json.dumps(ringkasan_data, ensure_ascii=False, indent=2)}"
    )

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.2},
    }

    last_err = ""
    for api_ver, model_full in kandidat_list:
        url = (
            f"https://generativelanguage.googleapis.com/{api_ver}/"
            f"{model_full}:generateContent?key={api_key}"
        )
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
                        return {
                            "status": "TERSAMBUNG",
                            "keterangan": f"Berhasil terhubung ke Gemini API ({model_full}) | {info_model}.",
                            "teks": parts[0]["text"].strip(),
                        }
        except Exception as exc:
            last_err = f"{model_full}: {exc}"
            continue

    return {
        "status": "GAGAL_KONEKSI",
        "keterangan": f"Gagal memanggil Gemini API ({last_err or 'tidak ada model aktif'}) | {info_model}.",
        "teks": f"Catatan: Gagal memanggil Gemini API ({last_err}). Evaluasi statistik lokal tetap tersimpan.",
    }


def jalankan_evaluasi():
    rows = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, mode="r", encoding="utf-8-sig", newline="") as f:
            sample = f.read(2048)
            f.seek(0)
            delimiter = ";" if sample.count(";") > sample.count(",") else ","
            reader = csv.DictReader(f, delimiter=delimiter)
            for r in reader:
                if not r or not any((v or "").strip() for v in r.values()):
                    continue
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

    for idx_row, r in enumerate(rows, start=1):
        profit = parse_float(r.get("profit_usd", 0.0))
        impact_pct = parse_float(r.get("balance_impact_pct", 0.0))
        durasi_detik = parse_float(r.get("holding_seconds", 0.0))
        durasi_menit = round(durasi_detik / 60.0, 2)
        exit_reason = (r.get("exit_reason") or "UNKNOWN").strip().upper()
        symbol = (r.get("symbol") or "").strip()
        direction = (r.get("direction") or "").strip()
        score_m5 = parse_int(r.get("score_m5", 0))
        score_m15 = parse_int(r.get("score_m15", 0))
        adx_m5 = parse_float(r.get("adx_m5", 0.0))
        priority_flag = (r.get("priority_flag") or "NORMAL").strip()

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
            "entry_ke": idx_row,
            "symbol": symbol,
            "direction": direction,
            "profit_usd": profit,
            "balance_impact_pct": impact_pct,
            "priority_flag": priority_flag,
            "holding_seconds": int(durasi_detik),
            "holding_minutes": durasi_menit,
            "exit_reason": exit_reason,
            "score_m5": score_m5,
            "score_m15": score_m15,
            "adx_m5": adx_m5,
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

    wib_now = datetime.now(timezone.utc) + timedelta(hours=7)
    waktu_wib_str = wib_now.strftime("%Y-%m-%d %H:%M:%S WIB")

    blok_10 = susun_blok_10_entry(detail_catatan)
    perintah = susun_perintah_otomatis(stats, blok_10, waktu_wib_str)

    with open(COMMAND_FILE, mode="w", encoding="utf-8") as f:
        json.dump(perintah, f, ensure_ascii=False, indent=2)

    hasil_gemini = panggil_gemini_evaluasi({
        "statistik": stats,
        "evaluasi_tiap_10_entry": blok_10[-10:],
        "perintah_terbit": perintah,
        "riwayat_tiap_entry": detail_catatan[-30:],
    })

    laporan = {
        "updated_wib": waktu_wib_str,
        "koneksi_gemini": {
            "status": hasil_gemini["status"],
            "keterangan": hasil_gemini["keterangan"],
        },
        "statistik": stats,
        "evaluasi_tiap_10_entry": blok_10,
        "perintah_aktif": perintah,
        "evaluasi_tiap_entry": detail_catatan,
        "ai_analisis": hasil_gemini["teks"],
    }

    with open(REPORT_FILE, mode="w", encoding="utf-8") as f:
        json.dump(laporan, f, ensure_ascii=False, indent=2)

    lines = [
        "# Laporan Evaluasi Riset Scalping Otomatis",
        f"- **Diperbarui:** {waktu_wib_str}",
        f"- **Koneksi Gemini API:** `{hasil_gemini['status']}` — {hasil_gemini['keterangan']}",
        f"- **Total Entry:** {stats['total_trade']} | **Win Rate:** {stats['win_rate_pct']}% | **Net P/L:** ${stats['net_profit_usd']}",
        "",
        "## Perintah Aktif untuk MT5 (`strategy_command.json`)",
        f"- **Mode:** `{perintah['mode_trading']}` | **Min Peluang:** `{perintah['min_probabilitas']}%` | **Max Posisi (Lot 0.01):** `{perintah['max_posisi']}`",
        f"- **Jarak Tambah ATR:** `{perintah['jarak_tambah_atr']}` | **Auto-Cut Goyah:** `{'AKTIF' if perintah['auto_cut_unstable'] else 'NONAKTIF'}`",
        f"- **Alasan Arahan:** {perintah['alasan_arahan']}",
        "",
        "## Klasifikasi Tiap Entry",
        f"- Untung Besar: {stats['kategori']['UNTUNG_BESAR']}",
        f"- Untung Kecil: {stats['kategori']['UNTUNG_KECIL']}",
        f"- Rugi Kecil: {stats['kategori']['RUGI_KECIL']}",
        f"- Rugi Besar: {stats['kategori']['RUGI_BESAR']}",
        f"- Auto-Cut Untung (Chart/Berita Tidak Stabil): {stats['kategori']['CUT_UNTUNG_TIDAK_STABIL']}",
        f"- Auto-Cut Rugi (Chart/Berita Tidak Stabil): {stats['kategori']['CUT_RUGI_TIDAK_STABIL']}",
        "",
        "## Rata-Rata Jeda Waktu / Durasi Tahan",
        f"- Entry ke TP: {stats['rata_durasi_menit']['ke_tp']} menit",
        f"- Entry ke SL: {stats['rata_durasi_menit']['ke_sl']} menit",
        f"- Entry ke Auto-Cut (Tanpa TP/SL): {stats['rata_durasi_menit']['auto_cut_tanpa_tp_sl']} menit",
        "",
        "## Rekap Tiap 10 Kali Entry",
    ]

    if blok_10:
        for b in blok_10:
            lines.append(
                f"- **{b['blok']}:** {b['hasil_blok']} (${b['net_pnl_usd']}) | {b['win']}W / {b['loss']}L | "
                f"Rata-rata durasi: {b['rata_durasi_menit']} menit"
            )
    else:
        lines.append("- Belum ada data entry.")

    lines.extend([
        "",
        "## Analisis Evaluasi AI",
        laporan["ai_analisis"],
    ])

    with open(SUMMARY_MD, mode="w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    jalankan_evaluasi()
