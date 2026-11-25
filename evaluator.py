import csv
import json
import os
from datetime import datetime, timedelta, timezone
from urllib import request

HISTORY_FILE = "trade_history.csv"
MEMORY_FILE = "error_memory.json"
REPORT_FILE = "evaluasi_riset.json"
SUMMARY_MD = "EVALUASI_TERBARU.md"
COMMAND_FILE = "strategy_command.json"

BIG_WIN_USD = 2.00
BIG_LOSS_USD = -2.00
DEFAULT_MAX_POSISI = 100
PROFIT_EROSION_TRIGGER_PCT = 30.0
MIN_PEAK_PROFIT_FOR_30PCT = 5.00
ADX_REM_TANGAN = 30.0
ADX_NORMAL_LONGGAR = 35.0
MAX_ENTRY_SAAT_ADX_TINGGI = 2
TARGET_PROFIT_ADX_TINGGI_USD = 0.30


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


def hitung_puncak_dan_erosi_profit(detail_catatan, net_profit_sekarang):
    running_pnl = 0.0
    peak_pnl = 0.0
    for item in detail_catatan:
        running_pnl = round(running_pnl + parse_float(item.get("profit_usd", 0.0)), 4)
        if running_pnl > peak_pnl:
            peak_pnl = running_pnl

    if net_profit_sekarang > peak_pnl:
        peak_pnl = net_profit_sekarang

    peak_rounded = round(peak_pnl, 2)
    erosi_usd = round(max(0.0, peak_rounded - net_profit_sekarang), 2)
    erosi_pct = 0.0
    if peak_rounded > 0.0:
        erosi_pct = round((erosi_usd / peak_rounded) * 100.0, 2)

    rem_tangan_30pct = (peak_rounded >= MIN_PEAK_PROFIT_FOR_30PCT and erosi_pct >= PROFIT_EROSION_TRIGGER_PCT)

    return {
        "peak_profit_usd": peak_rounded,
        "erosi_dari_puncak_usd": erosi_usd,
        "erosi_dari_puncak_pct": erosi_pct,
        "rem_tangan_30pct_aktif": rem_tangan_30pct,
    }


def muat_memori_kesalahan():
    default_mem = {
        "total_evaluasi": 0,
        "streak_rugi_evaluasi": 0,
        "total_trade_terakhir": 0,
        "net_pnl_terakhir": 0.0,
        "peak_profit_usd": 0.0,
        "erosi_dari_puncak_pct": 0.0,
        "pola_kesalahan": {
            "rugi_saat_adx_kuat_ge_30": 0,
            "rugi_saat_adx_lemah_lt_20": 0,
            "rugi_tahan_lama_ge_10_menit": 0,
            "rugi_skor_tinggi_ge_75": 0,
        },
        "catatan_pembelajaran": [
            "Sistem memori kesalahan diinisialisasi; akan mencatat pola rugi berulang dari tiap evaluasi."
        ],
    }
    if not os.path.exists(MEMORY_FILE):
        return default_mem
    try:
        with open(MEMORY_FILE, mode="r", encoding="utf-8") as f:
            data = json.load(f)
        for k, v in default_mem.items():
            if k not in data:
                data[k] = v
        if "pola_kesalahan" not in data or not isinstance(data["pola_kesalahan"], dict):
            data["pola_kesalahan"] = default_mem["pola_kesalahan"]
        for pk, pv in default_mem["pola_kesalahan"].items():
            if pk not in data["pola_kesalahan"]:
                data["pola_kesalahan"][pk] = pv
        return data
    except Exception:
        return default_mem


def perbarui_memori_kesalahan(memori, stats, detail_catatan, info_erosi, waktu_wib_str):
    pola = {
        "rugi_saat_adx_kuat_ge_30": 0,
        "rugi_saat_adx_lemah_lt_20": 0,
        "rugi_tahan_lama_ge_10_menit": 0,
        "rugi_skor_tinggi_ge_75": 0,
    }

    for item in detail_catatan:
        if item["profit_usd"] < 0:
            adx_val = parse_float(item.get("adx_m5", 0.0))
            hold_min = parse_float(item.get("holding_minutes", 0.0))
            skor_max = max(parse_int(item.get("score_m5", 0)), parse_int(item.get("score_m15", 0)))

            if adx_val >= ADX_REM_TANGAN:
                pola["rugi_saat_adx_kuat_ge_30"] += 1
            elif adx_val < 20.0:
                pola["rugi_saat_adx_lemah_lt_20"] += 1

            if hold_min >= 10.0:
                pola["rugi_tahan_lama_ge_10_menit"] += 1

            if skor_max >= 75:
                pola["rugi_skor_tinggi_ge_75"] += 1

    memori["total_evaluasi"] = parse_int(memori.get("total_evaluasi", 0)) + 1
    net_pnl = stats["net_profit_usd"]

    if net_pnl < 0:
        memori["streak_rugi_evaluasi"] = parse_int(memori.get("streak_rugi_evaluasi", 0)) + 1
    else:
        memori["streak_rugi_evaluasi"] = 0

    pola_dominan = max(pola.items(), key=lambda x: x[1])
    catatan_baru = (
        f"[{waktu_wib_str}] Trade={stats['total_trade']}, Net=${net_pnl} "
        f"(Peak=${info_erosi['peak_profit_usd']}, Erosi={info_erosi['erosi_dari_puncak_pct']}%), "
        f"StreakRugi={memori['streak_rugi_evaluasi']}, PolaRugiTerbanyak={pola_dominan[0]} ({pola_dominan[1]}x)."
    )

    catatan_list = list(memori.get("catatan_pembelajaran", []))
    catatan_list.append(catatan_baru)
    memori["catatan_pembelajaran"] = catatan_list[-10:]
    memori["pola_kesalahan"] = pola
    memori["total_trade_terakhir"] = stats["total_trade"]
    memori["net_pnl_terakhir"] = net_pnl
    memori["peak_profit_usd"] = info_erosi["peak_profit_usd"]
    memori["erosi_dari_puncak_pct"] = info_erosi["erosi_dari_puncak_pct"]
    memori["terakhir_update_wib"] = waktu_wib_str
    return memori


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


def susun_perintah_otomatis(stats, blok_10, memori, info_erosi, waktu_wib_str):
    cmd = {
        "updated_wib": waktu_wib_str,
        "mode_trading": "ACTIVE",
        "alasan_arahan": "Mode aktif: eksekusi tanpa jeda selama syarat terpenuhi, lot terkunci 0.01, auto-cut aktif.",
        "min_probabilitas": 60,
        "wajib_kompak_m15": True,
        "max_adx_entry": ADX_NORMAL_LONGGAR,
        "adx_over_limit_max_entry": MAX_ENTRY_SAAT_ADX_TINGGI,
        "adx_over_limit_profit_usd": TARGET_PROFIT_ADX_TINGGI_USD,
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
        cmd["max_adx_entry"] = ADX_REM_TANGAN if info_erosi["rem_tangan_30pct_aktif"] else ADX_NORMAL_LONGGAR
        cmd["alasan_arahan"] = (
            f"Sampel baru {total} entry (belum genap 1 blok 10 entry): pertahankan batas peluang 60%, "
            f"max_adx_entry={cmd['max_adx_entry']} (maks {MAX_ENTRY_SAAT_ADX_TINGGI} entry di atas ADX), "
            f"maksimal {DEFAULT_MAX_POSISI} posisi (lot 0.01)."
        )
        return cmd

    win_rate = stats["win_rate_pct"]
    rug_besar = stats["kategori"]["RUGI_BESAR"]
    streak_rugi = parse_int(memori.get("streak_rugi_evaluasi", 0))
    pola = memori.get("pola_kesalahan", {})
    rugi_pola_berat = (
        parse_int(pola.get("rugi_saat_adx_kuat_ge_30", pola.get("rugi_saat_adx_kuat_ge_28", 0)))
        + parse_int(pola.get("rugi_tahan_lama_ge_10_menit", 0))
        + parse_int(pola.get("rugi_skor_tinggi_ge_75", 0))
    )

    blok_genap = [b for b in blok_10 if b["jumlah_entry"] == 10]
    acuan_blok = blok_genap[-1] if blok_genap else blok_10[-1]

    kerugian_besar = (
        stats["net_profit_usd"] < 0
        or rug_besar >= 5
        or (acuan_blok["net_pnl_usd"] < 0 and acuan_blok["loss"] >= 6)
    )
    rem_adx_aktif = kerugian_besar or info_erosi["rem_tangan_30pct_aktif"]
    cmd["max_adx_entry"] = ADX_REM_TANGAN if rem_adx_aktif else ADX_NORMAL_LONGGAR

    if kerugian_besar:
        penalti_step = min(8, max(3, streak_rugi + (2 if rugi_pola_berat >= 4 else 0)))
        cmd["mode_trading"] = "CAUTIOUS"
        cmd["min_probabilitas"] = 60 + penalti_step
        cmd["max_posisi"] = 40 if rug_besar >= 8 else 60
        cmd["jarak_tambah_atr"] = 0.35 if rugi_pola_berat >= 3 else 0.30
        cmd["alasan_arahan"] = (
            f"Rem tangan ADX>{int(cmd['max_adx_entry'])} (maks {MAX_ENTRY_SAAT_ADX_TINGGI} entry, target ${TARGET_PROFIT_ADX_TINGGI_USD}) "
            f"aktif karena kerugian besar ({acuan_blok['blok']}: ${acuan_blok['net_pnl_usd']}, Net=${stats['net_profit_usd']}, RugiBesar={rug_besar})."
        )
    elif info_erosi["rem_tangan_30pct_aktif"]:
        cmd["mode_trading"] = "CAUTIOUS"
        cmd["min_probabilitas"] = 63
        cmd["max_posisi"] = 60
        cmd["jarak_tambah_atr"] = 0.30
        cmd["alasan_arahan"] = (
            f"Rem tangan ADX>{int(cmd['max_adx_entry'])} (maks {MAX_ENTRY_SAAT_ADX_TINGGI} entry, target ${TARGET_PROFIT_ADX_TINGGI_USD}) aktif: "
            f"profit terkikis {info_erosi['erosi_dari_puncak_pct']}% (${info_erosi['erosi_dari_puncak_usd']} dari puncak ${info_erosi['peak_profit_usd']})."
        )
    elif win_rate >= 65.0 and rug_besar <= 2 and stats["net_profit_usd"] > 0:
        cmd["mode_trading"] = "ACTIVE"
        cmd["min_probabilitas"] = 60
        cmd["max_posisi"] = DEFAULT_MAX_POSISI
        cmd["jarak_tambah_atr"] = 0.25
        cmd["alasan_arahan"] = (
            f"Keuntungan besar & aman (Net=${stats['net_profit_usd']}, Peak=${info_erosi['peak_profit_usd']}, "
            f"Erosi={info_erosi['erosi_dari_puncak_pct']}%, WR {win_rate}%): lanjutkan mode ACTIVE dengan max_adx_entry={int(cmd['max_adx_entry'])}."
        )
    else:
        cmd["mode_trading"] = "ACTIVE"
        cmd["min_probabilitas"] = 62
        cmd["max_posisi"] = 75
        cmd["jarak_tambah_atr"] = 0.28
        cmd["alasan_arahan"] = (
            f"Erosi profit masih ringan ({info_erosi['erosi_dari_puncak_pct']}% dari puncak ${info_erosi['peak_profit_usd']}, "
            f"Net=${stats['net_profit_usd']}): lanjutkan normal dengan max_adx_entry={int(cmd['max_adx_entry'])}."
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
        "Tulis analisis singkat, padat, dan tuntas sampai selesai tanpa terpotong dalam bahasa Indonesia:\n"
        "1. Evaluasi profit vs rugi (termasuk puncak profit, persentase erosi profit, dan perbandingan auto-cut vs SL).\n"
        "2. Evaluasi durasi tahan ke TP, SL, dan auto-cut.\n"
        "3. Evaluasi blok 10 entry dan pola kesalahan di error_memory.\n"
        "4. 2-3 saran penyetelan parameter konkret.\n\n"
        f"DATA EVALUASI:\n{json.dumps(ringkasan_data, ensure_ascii=False, indent=2)}"
    )

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 2048,
        },
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

    info_erosi = hitung_puncak_dan_erosi_profit(detail_catatan, stats["net_profit_usd"])
    memori = muat_memori_kesalahan()
    memori = perbarui_memori_kesalahan(memori, stats, detail_catatan, info_erosi, waktu_wib_str)
    with open(MEMORY_FILE, mode="w", encoding="utf-8") as f:
        json.dump(memori, f, ensure_ascii=False, indent=2)

    blok_10 = susun_blok_10_entry(detail_catatan)
    perintah = susun_perintah_otomatis(stats, blok_10, memori, info_erosi, waktu_wib_str)

    with open(COMMAND_FILE, mode="w", encoding="utf-8") as f:
        json.dump(perintah, f, ensure_ascii=False, indent=2)

    hasil_gemini = panggil_gemini_evaluasi({
        "statistik": stats,
        "kondisi_profit_dan_erosi": info_erosi,
        "memori_kesalahan": memori,
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
        "kondisi_profit_dan_erosi": info_erosi,
        "memori_kesalahan": memori,
        "evaluasi_tiap_10_entry": blok_10,
        "perintah_aktif": perintah,
        "evaluasi_tiap_entry": detail_catatan,
        "ai_analisis": hasil_gemini["teks"],
    }

    with open(REPORT_FILE, mode="w", encoding="utf-8") as f:
        json.dump(laporan, f, ensure_ascii=False, indent=2)

    pola_mem = memori.get("pola_kesalahan", {})
    adx_kuat_val = pola_mem.get("rugi_saat_adx_kuat_ge_30", pola_mem.get("rugi_saat_adx_kuat_ge_28", 0))
    lines = [
        "# Laporan Evaluasi Riset Scalping Otomatis",
        f"- **Diperbarui:** {waktu_wib_str}",
        f"- **Koneksi Gemini API:** `{hasil_gemini['status']}` — {hasil_gemini['keterangan']}",
        f"- **Total Entry:** {stats['total_trade']} | **Win Rate:** {stats['win_rate_pct']}% | **Net P/L:** ${stats['net_profit_usd']} | **Puncak Profit:** ${info_erosi['peak_profit_usd']} (Erosi: {info_erosi['erosi_dari_puncak_pct']}%)",
        "",
        "## Perintah Aktif untuk MT5 (`strategy_command.json`)",
        f"- **Mode:** `{perintah['mode_trading']}` | **Min Peluang:** `{perintah['min_probabilitas']}%` | **Max ADX Entry:** `{perintah['max_adx_entry']}` | **Max Posisi (Lot 0.01):** `{perintah['max_posisi']}`",
        f"- **Aturan ADX Tinggi:** Maks `{perintah['adx_over_limit_max_entry']}` entry, target cut `${perintah['adx_over_limit_profit_usd']}`, lock jika 2x SL hingga ADX M5 & M15 < `{perintah['max_adx_entry']}`",
        f"- **Jarak Tambah ATR:** `{perintah['jarak_tambah_atr']}` | **Auto-Cut Goyah:** `{'AKTIF' if perintah['auto_cut_unstable'] else 'NONAKTIF'}`",
        f"- **Alasan Arahan:** {perintah['alasan_arahan']}",
        "",
        "## Memori & Pembelajaran Kesalahan (`error_memory.json`)",
        f"- **Evaluasi Ke-:** {memori.get('total_evaluasi', 0)} | **Streak Evaluasi Rugi:** {memori.get('streak_rugi_evaluasi', 0)}",
        f"- **Pola Rugi Terekam:** ADX Kuat (>={int(ADX_REM_TANGAN)}): `{adx_kuat_val}` | ADX Lemah (<20): `{pola_mem.get('rugi_saat_adx_lemah_lt_20', 0)}` | Tahan >=10m: `{pola_mem.get('rugi_tahan_lama_ge_10_menit', 0)}` | Skor Tinggi (>=75): `{pola_mem.get('rugi_skor_tinggi_ge_75', 0)}`",
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
