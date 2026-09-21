#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Organiza o acervo para publicação:

1. Ações penais (classe 283) de Curitiba e do RJ → um arquivo JSON individual
   por processo, organizado por ano de ajuizamento, com movimentações em ordem
   cronológica (do ajuizamento ao último andamento).
2. Demais classes → JSONL compactado (gzip) por classe.
3. Registros de 2ª instância (TRF4) → JSONs individuais por ano.
4. Gera contagens de verificação.
"""
import json
import gzip
import re
import shutil
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
D = BASE / "dados"

def fmt_cnj(n):
    n = str(n).zfill(20)
    return f"{n[0:7]}-{n[7:9]}.{n[9:13]}.{n[13]}.{n[14:16]}.{n[16:20]}"

def mov_key(m):
    return str(m.get("dataHora") or "")

def salvar_individual(src, destdir):
    np_ = str(src.get("numeroProcesso", "")).zfill(20)
    ano = np_[9:13]
    movs = src.get("movimentos") or []
    src = dict(src)
    src["movimentos"] = sorted(movs, key=mov_key)
    d = destdir / ano
    d.mkdir(parents=True, exist_ok=True)
    out = d / f"{fmt_cnj(np_)}.json"
    with open(out, "w") as f:
        json.dump(src, f, ensure_ascii=False, indent=1)
    return out

def processar_orgao(subpasta, rotulo):
    raw = D / subpasta / "raw"
    ap_dir = D / subpasta / "acoes_penais"
    outras = D / subpasta / "outras_classes"
    ap_dir.mkdir(exist_ok=True)
    outras.mkdir(exist_ok=True)
    n_ap = 0
    for jl in sorted(raw.glob("classe_*.jsonl")):
        cod = int(jl.stem.split("_")[1])
        if cod == 283:
            with open(jl) as f:
                for line in f:
                    salvar_individual(json.loads(line), ap_dir)
                    n_ap += 1
        else:
            gz = outras / (jl.name + ".gz")
            with open(jl, "rb") as fi, gzip.open(gz, "wb", compresslevel=9) as fo:
                shutil.copyfileobj(fi, fo)
    print(f"[{rotulo}] ações penais individuais: {n_ap}; "
          f"outras classes gzip: {len(list(outras.glob('*.gz')))}")

def processar_g2():
    src = D / "02_trf4_2inst" / "raw_g2_acoes_penais.jsonl"
    dest = D / "02_trf4_2inst" / "recursos"
    dest.mkdir(exist_ok=True)
    n = 0
    with open(src) as f:
        for line in f:
            salvar_individual(json.loads(line), dest)
            n += 1
    print(f"[TRF4 G2] recursos individuais: {n}")

if __name__ == "__main__":
    processar_orgao("01_curitiba_13vara", "13ª Vara Curitiba")
    processar_orgao("05_rj_trf2", "7ª VFC RJ")
    processar_g2()
    print("OK")
