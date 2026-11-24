import os
import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
MODEL = "gpt-4o"

RSS_URLS = [
    "https://www.fxstreet.com/rss/news",
    "https://www.dailyfx.com/feeds/market-news"
]

def ambil_berita():
    judul_berita = []
    headers = {"User-Agent": "Mozilla/5.0"}
    for url in RSS_URLS:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                root = ET.fromstring(resp.read())
                for item in root.findall(".//item")[:15]:
                    title = item.find("title")
                    if title is not None and title.text:
                        teks = title.text.strip()
                        kata_kunci = ["gold", "xau", "eur", "usd", "fed", "fomc", "cpi", "nfp", "ecb", "powell", "lagarde", "dollar", "inflation", "rate"]
                        if any(k in teks.lower() for k in kata_kunci):
                            judul_berita.append(teks)
        except Exception as e:
            print(f"Gagal akses {url}: {e}")
    return list(dict.fromkeys(judul_berita))[:12]

def tanya_github_ai(daftar_berita):
    if not daftar_berita:
        return {
            "status": "NORMAL",
            "xau_bias": "NETRAL",
            "eur_bias": "NETRAL",
            "xauusd": "Tidak ada berita besar, fokus chart 60%+.",
            "eurusd": "Tidak ada berita besar, fokus chart 60%+."
        }

    gabungan = "\n- ".join(daftar_berita)
    prompt = (
        "Kamu analis kuantitatif forex & emas institusional. Analisis headline berita global terbaru ini:\n"
        f"- {gabungan}\n\n"
        "Tentukan apakah ada berita berdampak tinggi saat ini dan arah sentimennya untuk XAUUSD dan EURUSD. "
        "Balas HANYA JSON valid tanpa markdown dengan format persis:\n"
        '{"status": "PENTING atau NORMAL", "xau_bias": "BUY atau SELL atau NETRAL", "eur_bias": "BUY atau SELL atau NETRAL", '
        '"xauusd": "ringkasan maksimal 9 kata", "eurusd": "ringkasan maksimal 9 kata"}'
    )

    url = "https://models.inference.ai.azure.com/chat/completions"
    payload = json.dumps({
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1
    }).encode("utf-8")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GITHUB_TOKEN}"
    }

    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            res_json = json.loads(resp.read().decode("utf-8"))
            teks = res_json["choices"][0]["message"]["content"].strip()
            teks = teks.replace("```json", "").replace("```", "").strip()
            return json.loads(teks)
    except Exception as e:
        return {
            "status": "NORMAL",
            "xau_bias": "NETRAL",
            "eur_bias": "NETRAL",
            "xauusd": f"Fallback lokal ({str(e)[:22]})",
            "eurusd": "Fallback lokal aktif."
        }

if __name__ == "__main__":
    wib = datetime.now(timezone.utc) + timedelta(hours=7)
    berita = ambil_berita()
    hasil = tanya_github_ai(berita)
    hasil["updated_wib"] = wib.strftime("%H:%M WIB")
    hasil["model"] = MODEL

    with open("market_status.json", "w", encoding="utf-8") as f:
        json.dump(hasil, f, indent=2, ensure_ascii=False)
    print("Update sukses:", hasil)
