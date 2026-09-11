# download_ena.py
import time
import requests
import subprocess
from pathlib import Path
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

WORKDIR = Path("rnaseq_work")   # <- ggf. auf externen Pfad anpassen, siehe vorherige Nachrichten
WORKDIR.mkdir(exist_ok=True, parents=True)


def get_ena_urls(srr):
    """Holt die direkten FASTQ-Download-Links von ENA für eine SRR-ID."""
    url = "https://www.ebi.ac.uk/ena/portal/api/filereport"
    params = {
        "accession": srr,
        "result": "read_run",
        "fields": "fastq_ftp",
        "format": "json"
    }
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()
    if not data or not data[0].get("fastq_ftp"):
        return None
    urls = data[0]["fastq_ftp"].split(";")
    return [f"https://{u}" if not u.startswith("http") else u for u in urls]


def download_with_retry(cmd, max_retries=3, timeout=3600):
    for attempt in range(1, max_retries + 1):
        try:
            subprocess.run(cmd, check=True, timeout=timeout)
            return True
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
            print(f"Versuch {attempt}/{max_retries} fehlgeschlagen: {e}")
            if attempt < max_retries:
                time.sleep(10)
    return False


def download_sample(srr):
    out_r1 = WORKDIR / f"{srr}_1.fastq.gz"
    out_r2 = WORKDIR / f"{srr}_2.fastq.gz"
    if out_r1.exists() and out_r1.stat().st_size > 0 and out_r2.exists() and out_r2.stat().st_size > 0:
        print(f"{srr}: schon heruntergeladen")
        return srr, True

    urls = get_ena_urls(srr)
    if not urls or len(urls) < 2:
        print(f"{srr}: keine Paired-End-URLs bei ENA gefunden")
        return srr, False

    success = True
    for url, out_path in zip(urls, [out_r1, out_r2]):
        print(f"{srr}: lade {url}")
        ok = download_with_retry([
            "aria2c", "-x", "8", "-s", "8",
            "--summary-interval=30",
            "--max-tries=5", "--retry-wait=10",
            "-c",
            "-d", str(out_path.parent),
            "-o", out_path.name,
            url
        ])
        success = success and ok

    if success:
        print(f"{srr}: fertig heruntergeladen")
    return srr, success


# ============================================
# HIER FEHLTE ES: Manifest einlesen + srr_list bauen
# ============================================
manifest = pd.read_csv("sample_manifest.csv")
srr_list = manifest["Run"].tolist()

# 4 parallele Downloads - bei Bedarf hoch/runter regeln je nach Bandbreite
with ThreadPoolExecutor(max_workers=4) as executor:
    futures = {executor.submit(download_sample, srr): srr for srr in srr_list}
    for future in as_completed(futures):
        srr = futures[future]
        try:
            future.result()
        except Exception as e:
            print(f"{srr}: FEHLER - {e}")