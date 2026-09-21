#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Consulta um processo na API pública do DataJud/CNJ e imprime/salva a ficha
completa (todas as instâncias encontradas), com movimentos em ordem
cronológica.

Uso:
  python3 consultar_processo.py 5046512-94.2016.4.04.7000 [api_publica_trf4]

O número pode vir com ou sem pontuação. Se o índice não for informado, tenta
deduzir pelo segmento/tribunal do próprio número (J.TR):
  4.04 → api_publica_trf4 | 4.02 → api_publica_trf2 | 4.03 → api_publica_trf3
  4.01 → api_publica_trf1 | 3.00 → api_publica_stj  | 8.16 → api_publica_tjpr
"""
import json
import re
import sys
import urllib.request

KEY = "APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    num = re.sub(r"\D", "", sys.argv[1]).zfill(20)
    if len(sys.argv) > 2:
        alias = sys.argv[2]
    else:
        j, tr = num[13], num[14:16]
        alias = {
            ("4", "04"): "api_publica_trf4", ("4", "02"): "api_publica_trf2",
            ("4", "03"): "api_publica_trf3", ("4", "01"): "api_publica_trf1",
            ("3", "00"): "api_publica_stj", ("8", "16"): "api_publica_tjpr",
        }.get((j, tr))
        if not alias:
            print(f"Não sei deduzir o índice para J={j} TR={tr}; informe-o.")
            sys.exit(2)
    req = urllib.request.Request(
        f"https://api-publica.datajud.cnj.jus.br/{alias}/_search",
        data=json.dumps({
            "size": 10,
            "query": {"match_phrase": {"numeroProcesso": num}}}).encode(),
        headers={"Authorization": KEY, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        res = json.loads(r.read())
    hits = res["hits"]["hits"]
    if not hits:
        print("Processo não encontrado na API pública.")
        sys.exit(3)
    for h in hits:
        src = h["_source"]
        src["movimentos"] = sorted(
            src.get("movimentos") or [], key=lambda m: str(m.get("dataHora") or ""))
        fn = f"{num}_{src.get('grau','')}.json"
        with open(fn, "w") as f:
            json.dump(src, f, ensure_ascii=False, indent=1)
        cl = (src.get("classe") or {}).get("nome", "?")
        oj = (src.get("orgaoJulgador") or {}).get("nome", "?")
        print(f"[{src.get('grau')}] {cl} — {oj} — "
              f"{len(src['movimentos'])} movimentos → {fn}")

if __name__ == "__main__":
    main()
