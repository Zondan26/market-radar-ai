import hashlib
import os
import shutil
import subprocess
import time

# Ganti path ini sesuai lokasi folder MQL5\Files di MetaTrader 5 kamu
MT5_CSV_PATH = r"C:\Users\NAMA_USER\AppData\Roaming\MetaQuotes\Terminal\ID_TERMINAL\MQL5\Files\trade_history.csv"

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_CSV_PATH = os.path.join(REPO_DIR, "trade_history.csv")
CEK_SETIAP_DETIK = 5


def hitung_hash(path_file):
    if not os.path.exists(path_file):
        return None
    h = hashlib.md5()
    with open(path_file, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def jalankan_git(args):
    return subprocess.run(
        ["git"] + args,
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )


def sinkronkan():
    print("Memantau perubahan trade_history.csv dari MT5...")
    last_hash = hitung_hash(REPO_CSV_PATH)

    while True:
        try:
            if os.path.exists(MT5_CSV_PATH):
                current_hash = hitung_hash(MT5_CSV_PATH)
                if current_hash and current_hash != last_hash:
                    shutil.copy2(MT5_CSV_PATH, REPO_CSV_PATH)
                    jalankan_git(["add", "trade_history.csv"])
                    commit_res = jalankan_git(["commit", "-m", "Update trade_history.csv dari MT5"])
                    if commit_res.returncode == 0:
                        push_res = jalankan_git(["push"])
                        if push_res.returncode == 0:
                            print("Berhasil dikirim ke GitHub -> workflow evaluasi otomatis berjalan.")
                            last_hash = current_hash
                        else:
                            print("Gagal git push:", push_res.stderr.strip())
                    else:
                        last_hash = current_hash
        except Exception as exc:
            print("Kendala sinkronisasi:", exc)

        time.sleep(CEK_SETIAP_DETIK)


if __name__ == "__main__":
    sinkronkan()
