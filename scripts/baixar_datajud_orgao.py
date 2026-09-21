#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Varredura completa de um órgão julgador em um índice da API pública do DataJud/CNJ.

Uso: python3 baixar_datajud_orgao.py <alias> <codigo_orgao> <subpasta_dados> <rotulo>
Ex.:  python3 baixar_datajud_orgao.py api_publica_trf2 12260 05_rj_trf2 7vfc_rj

Baixa TODOS os processos do órgão (todas as classes), com a ficha completa
(classe, assuntos, datas e todas as movimentações).
"""
import json
import time
import csv
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path

ALIAS, ORGAO, SUBP, ROTULO = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
API = f"https://api-publica.datajud.cnj.jus.br/{ALIAS}/_search"
KEY = "APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
BASE = Path(__file__).resolve().parent.parent
RAW = BASE / "dados" / SUBP / "raw"
RAW.mkdir(parents=True, exist_ok=True)
LOG = Path(__file__).resolve().parent / f"scan_{ROTULO}.log"

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
    log(f"=== Varredura {ROTULO}: órgão {ORGAO} em {ALIAS} ===")
    agg = query({
        "size": 0,
        "query": {"match": {"orgaoJulgador.codigo": ORGAO}},
        "aggs": {"c": {"terms": {"field": "classe.codigo", "size": 200}}}
    })
    buckets = agg["aggregations"]["c"]["buckets"]
    log(f"{len(buckets)} classes; total aprox.: {agg['hits']['total']['value']}")

    indice, vistos = [], set()
    PAGE = 200
    for b in sorted(buckets, key=lambda x: -x["doc_count"]):
        cod, esperado = b["key"], b["doc_count"]
        out = RAW / f"classe_{cod:05d}.jsonl"
        if out.exists():
            n_ok = sum(1 for _ in open(out))
            if n_ok >= esperado:
                for line in open(out):
                    h = json.loads(line)
                    key = (h.get("numeroProcesso"), h.get("grau"))
                    if key not in vistos:
                        vistos.add(key)
                        indice.append(h)
                log(f"classe {cod}: já baixada ({n_ok}) — pulando")
                continue
            out.unlink()
        n, nome_classe, frm = 0, "?", 0
        with open(out, "w") as f:
            while frm < min(esperado, 10000):
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

    idx_path = BASE / "dados" / SUBP / f"indice_{ROTULO}.csv"
    with open(idx_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["numero_processo", "numero_cnj", "classe_codigo", "classe_nome",
                    "assuntos", "data_ajuizamento", "ultima_atualizacao",
                    "qtd_movimentos", "grau", "formato"])
        for src in sorted(indice, key=lambda s: str(s.get("dataAjuizamento", ""))):
            np_ = src.get("numeroProcesso", "")
            cl = src.get("classe") or {}
            ass = "; ".join(sorted({(a.get("nome") or "") for a in (src.get("assuntos") or []) if isinstance(a, dict)}))
            da = str(src.get("dataAjuizamento", ""))
            da_fmt = f"{da[0:4]}-{da[4:6]}-{da[6:8]}" if re.match(r"^\d{8}", da) else da
            w.writerow([np_, fmt_cnj(np_), cl.get("codigo", ""), cl.get("nome", ""),
                        ass, da_fmt, src.get("dataHoraUltimaAtualizacao", ""),
                        len(src.get("movimentos") or []), src.get("grau", ""),
                        (src.get("formato") or {}).get("nome", "")])
    log(f"Índice: {idx_path} ({len(indice)} processos)")
    log("=== CONCLUÍDO ===")

if __name__ == "__main__":
    main()
