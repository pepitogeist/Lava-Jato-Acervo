#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Varredura completa da 13ª Vara Federal de Curitiba (órgão julgador 11891, TRF4)
na API pública do DataJud/CNJ.

Baixa TODOS os processos da vara (todas as classes processuais), com a ficha
completa de cada um — classe, assuntos, datas e TODAS as movimentações, do
ajuizamento ao último andamento registrado.

Saída:
  dados/01_curitiba_13vara/raw/classe_<codigo>.jsonl   (1 processo por linha)
  dados/01_curitiba_13vara/indice_13vara.csv
  log em scripts/scan_13vara.log

Fonte: https://api-publica.datajud.cnj.jus.br (chave pública documentada pelo CNJ)
"""
import json
import time
import csv
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path

API = "https://api-publica.datajud.cnj.jus.br/api_publica_trf4/_search"
KEY = "APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
ORGAO = 11891  # 13ª Vara Federal de Curitiba
BASE = Path(__file__).resolve().parent.parent
RAW = BASE / "dados" / "01_curitiba_13vara" / "raw"
RAW.mkdir(parents=True, exist_ok=True)
LOG = Path(__file__).resolve().parent / "scan_13vara.log"

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
                wait = 2 ** i
                log(f"  HTTP {e.code}; aguardando {wait}s (tentativa {i+1})")
                time.sleep(wait)
                continue
            raise
        except Exception as e:
            wait = 2 ** i
            log(f"  erro {type(e).__name__}: {e}; aguardando {wait}s")
            time.sleep(wait)
    raise RuntimeError("esgotadas as tentativas")

def fmt_cnj(n):
    n = str(n).zfill(20)
    return f"{n[0:7]}-{n[7:9]}.{n[9:13]}.{n[13]}.{n[14:16]}.{n[16:20]}"

def main():
    log("=== Varredura da 13ª Vara Federal de Curitiba (DataJud/TRF4) ===")
    # 1) descobrir classes
    agg = query({
        "size": 0,
        "query": {"match": {"orgaoJulgador.codigo": ORGAO}},
        "aggs": {"c": {"terms": {"field": "classe.codigo", "size": 200}}}
    })
    buckets = agg["aggregations"]["c"]["buckets"]
    total_esperado = agg["hits"]["total"]["value"]
    log(f"{len(buckets)} classes; total de processos (aprox.): {total_esperado}")

    indice = []
    vistos = set()
    PAGE = 200

    for b in sorted(buckets, key=lambda x: -x["doc_count"]):
        cod, esperado = b["key"], b["doc_count"]
        out = RAW / f"classe_{cod:05d}.jsonl"
        if out.exists():
            n_ok = sum(1 for _ in open(out))
            if n_ok >= esperado:
                log(f"classe {cod}: já baixada ({n_ok}) — pulando")
                # ainda precisa entrar no índice
                for line in open(out):
                    h = json.loads(line)
                    key = (h.get("numeroProcesso"), h.get("grau"))
                    if key in vistos:
                        continue
                    vistos.add(key)
                    indice.append(h)
                continue
            out.unlink()
        n = 0
        nome_classe = "?"
        with open(out, "w") as f:
            frm = 0
            while frm < esperado and frm + PAGE <= 10000 + PAGE:
                r = query({
                    "size": PAGE, "from": frm,
                    "query": {"bool": {"must": [
                        {"match": {"orgaoJulgador.codigo": ORGAO}},
                        {"match": {"classe.codigo": cod}}]}},
                    "sort": [{"dataAjuizamento": {"order": "asc"}}]
                })
                hits = r["hits"]["hits"]
                if not hits:
                    break
                for h in hits:
                    src = h["_source"]
                    key = (src.get("numeroProcesso"), src.get("grau"))
                    if key in vistos:
                        continue
                    vistos.add(key)
                    nome_classe = (src.get("classe") or {}).get("nome", "?")
                    f.write(json.dumps(src, ensure_ascii=False) + "\n")
                    indice.append(src)
                    n += 1
                frm += PAGE
                time.sleep(0.35)
        log(f"classe {cod} ({nome_classe}): {n}/{esperado}")

    # 2) índice CSV
    idx_path = BASE / "dados" / "01_curitiba_13vara" / "indice_13vara.csv"
    with open(idx_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["numero_processo", "numero_cnj", "classe_codigo", "classe_nome",
                    "assuntos", "data_ajuizamento", "ultima_atualizacao",
                    "qtd_movimentos", "grau", "formato"])
        for src in sorted(indice, key=lambda s: str(s.get("dataAjuizamento", ""))):
            np_ = src.get("numeroProcesso", "")
            cl = src.get("classe") or {}
            ass = "; ".join(sorted({(a.get("nome") or "") for a in (src.get("assuntos") or []) if isinstance(a, dict)}))
            movs = src.get("movimentos") or []
            da = str(src.get("dataAjuizamento", ""))
            da_fmt = f"{da[0:4]}-{da[4:6]}-{da[6:8]}" if re.match(r"^\d{8}", da) else da
            w.writerow([np_, fmt_cnj(np_), cl.get("codigo", ""), cl.get("nome", ""),
                        ass, da_fmt, src.get("dataHoraUltimaAtualizacao", ""),
                        len(movs), src.get("grau", ""),
                        (src.get("formato") or {}).get("nome", "")])
    log(f"Índice: {idx_path} ({len(indice)} processos)")
    log("=== CONCLUÍDO ===")

if __name__ == "__main__":
    main()
