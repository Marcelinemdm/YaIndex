#!/usr/bin/env python3
"""
YaIndex — Auto-updater
Verifica status dos sites e atualiza data.json.
Uso: python update.py
"""
import json, urllib.request, datetime, sys, threading, time

DATA_FILE = "data.json"
TIMEOUT = 8

def check_status(url: str) -> str:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 MoeIndex-Bot/1.0"})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return "online" if r.status < 400 else "warning"
    except Exception as e:
        msg = str(e).lower()
        if "403" in msg or "forbidden" in msg:
            return "warning"
        return "offline"

def update_all():
    with open(DATA_FILE, encoding="utf-8") as f:
        data = json.load(f)

    items_all = [(cat_idx, item_idx, item)
                 for cat_idx, cat in enumerate(data["categories"])
                 for item_idx, item in enumerate(cat["items"])]

    total = len(items_all)
    results = {}
    lock = threading.Lock()
    done = [0]

    def worker(cat_idx, item_idx, item):
        status = check_status(item["url"])
        with lock:
            results[(cat_idx, item_idx)] = status
            done[0] += 1
            pct = done[0] * 100 // total
            bar = "\u2588" * (pct // 5) + "\u2591" * (20 - pct // 5)
            print(f"\r[{bar}] {done[0]}/{total} — {item['name'][:30]:<30}", end="", flush=True)

    threads = []
    for args in items_all:
        t = threading.Thread(target=worker, args=args, daemon=True)
        t.start()
        threads.append(t)
        while sum(1 for th in threads if th.is_alive()) >= 20:
            time.sleep(0.05)

    for t in threads:
        t.join()

    print()

    changed = 0
    for (cat_idx, item_idx), status in results.items():
        old = data["categories"][cat_idx]["items"][item_idx].get("status")
        if old != status:
            data["categories"][cat_idx]["items"][item_idx]["status"] = status
            changed += 1

    now = datetime.datetime.utcnow()
    data["meta"]["last_updated"] = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    ver = data["meta"].get("version", "1.0.0")
    parts = [int(x) for x in str(ver).split(".")]
    while len(parts) < 3:
        parts.append(0)
    parts[2] += 1
    data["meta"]["version"] = ".".join(str(x) for x in parts)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    online  = sum(1 for s in results.values() if s == "online")
    warning = sum(1 for s in results.values() if s == "warning")
    offline = sum(1 for s in results.values() if s == "offline")
    print(f"\n✅ Concluído | 🟢 {online} online 🟡 {warning} aviso 🔴 {offline} offline")
    print(f"📝 {changed} status alterados | v{data['meta']['version']} | {data['meta']['last_updated']}")

if __name__ == "__main__":
    total_sites = sum(len(c["items"]) for c in json.load(open(DATA_FILE, encoding="utf-8"))["categories"])
    print(f"🔄 YaIndex Updater — verificando {total_sites} recursos...\n")
    t0 = time.time()
    update_all()
    print(f"⏱ Tempo total: {time.time()-t0:.1f}s")