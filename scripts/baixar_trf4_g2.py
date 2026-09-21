#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Baixa os registros de 2ª instância (TRF4, grau G2) para todos os números de
ações penais da 13ª Vara Federal de Curitiba já coletados na varredura G1.

Estratégia: consultas em lote (bool/should com match_phrase) de 40 números por
requisição, filtrando grau G2. Salva JSONL único + índice CSV.
"""
import json
import time
import csv
import re
import urllib.request
import urllib.error
from pathlib import Path

API = "https://api-publica.datajud.cnj.jus.br/api_publica_trf4/_search"
KEY = "APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
BASE = Path(__file__).resolve().parent.parent
SRC = BASE / "dados" / "01_curitiba_13vara" / "raw" / "classe_00283.jsonl"
OUTD = BASE / "dados" / "02_trf4_2inst"
OUTD.mkdir(parents=True, exist_ok=True)
OUT = OUTD / "raw_g2_acoes_penais.jsonl"
LOG = Path(__file__).resolve().parent / "scan_g2.log"

def log(msg):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")

def query(body, tries=6):
    data = json.dumps(body).encode()
    for i in range(tries):
        req = urllib.request.Request(API, data=data, headers={
            "Authorization": KEY, "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504):
                time.sleep(2 ** i)
                continue
            raise
        except Exception:
            time.sleep(2 ** i)
    raise RuntimeError("esgotadas as tentativas")

def fmt_cnj(n):
    n = str(n).zfill(20)
    return f"{n[0:7]}-{n[7:9]}.{n[9:13]}.{n[13]}.{n[14:16]}.{n[16:20]}"

def main():
    numeros = []
    with open(SRC) as f:
        for line in f:
            n = json.loads(line).get("numeroProcesso")
            if n:
                numeros.append(str(n))
    numeros = sorted(set(numeros))
    log(f"=== G2 para {len(numeros)} ações penais da 13ª Vara ===")

    achados, vistos = [], set()
    BATCH = 40
    with open(OUT, "w") as fo:
        for i in range(0, len(numeros), BATCH):
            lote = numeros[i:i+BATCH]
            r = query({
                "size": 200,
                "query": {"bool": {
                    "must": [{"match": {"grau": "G2"}}],
                    "should": [{"match_phrase": {"numeroProcesso": n}} for n in lote],
                    "minimum_should_match": 1}}
            })
            for h in r["hits"]["hits"]:
                src = h["_source"]
                key = h.get("_id") or (src.get("numeroProcesso"), src.get("grau"))
                if key in vistos:
                    continue
                vistos.add(key)
                fo.write(json.dumps(src, ensure_ascii=False) + "\n")
                achados.append(src)
            if (i // BATCH) % 5 == 0:
                log(f"  lote {i//BATCH + 1}/{(len(numeros)+BATCH-1)//BATCH}: acumulado {len(achados)}")
            time.sleep(0.4)

    with open(OUTD / "indice_g2.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["numero_processo", "numero_cnj", "classe_codigo", "classe_nome",
                    "orgao_julgador", "data_ajuizamento", "ultima_atualizacao",
                    "qtd_movimentos", "grau"])
        for src in sorted(achados, key=lambda s: str(s.get("numeroProcesso", ""))):
            np_ = src.get("numeroProcesso", "")
            cl = src.get("classe") or {}
            da = str(src.get("dataAjuizamento", ""))
            da_fmt = f"{da[0:4]}-{da[4:6]}-{da[6:8]}" if re.match(r"^\d{8}", da) else da
            w.writerow([np_, fmt_cnj(np_), cl.get("codigo", ""), cl.get("nome", ""),
                        (src.get("orgaoJulgador") or {}).get("nome", ""), da_fmt,
                        src.get("dataHoraUltimaAtualizacao", ""),
                        len(src.get("movimentos") or []), src.get("grau", "")])
    log(f"=== CONCLUÍDO: {len(achados)} registros G2 ===")

if __name__ == "__main__":
    main()
