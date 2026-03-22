#!/usr/bin/env python3
"""
Lê o corpo de uma GitHub Issue e insere o site em data.json.
Saídas (via $GITHUB_OUTPUT):
  added=true/false
  name=<nome do site>
  category=<id da categoria>
  error=<mensagem de erro>
"""
import json, os, re, sys

DATA_FILE = "data.json"

def out(key, value):
    with open(os.environ["GITHUB_OUTPUT"], "a") as f:
        f.write(f"{key}={value}\n")

def fail(msg):
    out("added", "false")
    out("error", msg)
    print(f"[ERRO] {msg}")
    sys.exit(0)

body = os.environ.get("ISSUE_BODY", "")

json_match = re.search(r"```(?:json)?\s*([\s\S]*?)```", body)
if json_match:
    raw = json_match.group(1).strip()
else:
    raw_match = re.search(r"\{[\s\S]+\}", body)
    if not raw_match:
        fail("Nenhum bloco JSON encontrado na issue. Use o formato do README.")
    raw = raw_match.group(0)

try:
    site = json.loads(raw)
except json.JSONDecodeError as e:
    fail(f"JSON inválido: {e}")

required = ["name", "url", "category"]
for field in required:
    if field not in site or not str(site[field]).strip():
        fail(f"Campo obrigatório ausente ou vazio: \"{field}\"")

name     = str(site["name"]).strip()
url      = str(site["url"]).strip()
category = str(site["category"]).strip()
tags     = site.get("tags", [])
status   = site.get("status", "online")
if status not in ("online", "warning", "offline"):
    status = "online"
if not isinstance(tags, list):
    tags = [str(tags)]
tags = [str(t).strip() for t in tags if str(t).strip()]

if not re.match(r"https?://", url):
    fail(f"URL inválida: \"{url}\" — precisa começar com http:// ou https://")

with open(DATA_FILE, encoding="utf-8") as f:
    data = json.load(f)

cat_obj = next((c for c in data["categories"] if c["id"] == category), None)
if cat_obj is None:
    ids = [c["id"] for c in data["categories"]]
    fail(f"Categoria \"{category}\" não existe. Disponíveis: {ids}")

for item in cat_obj["items"]:
    if item["url"].rstrip("/") == url.rstrip("/"):
        fail(f"URL já existe na categoria \"{category}\": {url}")


new_item = {
    "name":   name,
    "url":    url,
    "tags":   tags,
    "rank":   len(cat_obj["items"]) + 1,
    "status": status
}
cat_obj["items"].append(new_item)

import datetime
ver = data["meta"].get("version", "1.0.0")
parts = [int(x) for x in str(ver).split(".")]
while len(parts) < 3: parts.append(0)
parts[2] += 1
data["meta"]["version"] = ".".join(str(x) for x in parts)
data["meta"]["last_updated"] = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"[OK] Adicionado: {name} → {category} ({url})")
out("added", "true")
out("name", name)
out("category", category)