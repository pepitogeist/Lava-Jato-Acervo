#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Acrescenta a coluna link_consulta aos índices CSV do acervo."""
import csv
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
TRF4 = ("https://www.trf4.jus.br/trf4/controlador.php?acao=consulta_processual_"
        "resultado_pesquisa&selForma=NU&txtValor={n}&selOrigem=TRF&chkMostrarBaixados=1")
TRF2 = "https://eproc.jfrj.jus.br/eproc/externo_controlador.php?acao=processo_consulta_publica"

def add_links(path, url_fn):
    rows = list(csv.reader(open(path)))
    head = rows[0]
    if "link_consulta" in head:
        return
    head.append("link_consulta")
    for r in rows[1:]:
        r.append(url_fn(r[0]))
    with open(path, "w", newline="") as f:
        csv.writer(f).writerows(rows)
    print(f"ok: {path}")

add_links(BASE / "dados/01_curitiba_13vara/indice_13vara.csv", lambda n: TRF4.format(n=n))
add_links(BASE / "dados/02_trf4_2inst/indice_g2.csv", lambda n: TRF4.format(n=n))
add_links(BASE / "dados/05_rj_trf2/indice_7vfc_rj.csv", lambda n: TRF2)
