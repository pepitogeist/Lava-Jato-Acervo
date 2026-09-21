# Acervo Operação Lava Jato 

Acervo aberto e organizado dos processos judiciais da **Operação Lava Jato**
(2014–2021) e do entorno processual das varas que a conduziram, montado a
partir da **API Pública do DataJud/CNJ** (Base Nacional de Dados do Poder
Judiciário) e de fontes públicas oficiais.

Cada processo está aqui com a sua **ficha processual completa**: classe,
assuntos, órgão julgador, datas e **todas as movimentações registradas, da
distribuição ao último andamento**. Os autos
digitalizados (petições, provas, íntegras) não são distribuídos pelo CNJ.
o guia [`docs/como_acessar_autos.md`](docs/como_acessar_autos.md) mostra como
chegar neles em cada tribunal a partir de qualquer número deste acervo.

**Coleta realizada em 20/09/2026.** O acervo reflete o que a API pública do
CNJ reportava nessa data.

## Números do acervo

| Conjunto | Processos | Movimentações |
|---|---:|---:|
| 13ª Vara Federal de Curitiba: acervo criminal completo (1º grau, 59 classes) | **7.864** | **643.385** |
| -- das quais Ações Penais (classe 283) | 1.849 | — |
| TRF4 2ª instância: recursos das ações penais de Curitiba | **683** | **50.709** |
| 7ª Vara Federal Criminal do Rio de Janeiro: acervo completo (1º grau) | **3.713** | **42.904** |
| **Total** | **12.260** | **≈ 737.000** |

79 fases da operação catalogadas ([`indices/fases_operacao.csv`](indices/fases_operacao.csv)),
camada curada com os casos emblemáticos identificados
([`dados/00_acoes_identificadas/`](dados/00_acoes_identificadas/)) e tabelas de
referência do STF ([`dados/04_stf/`](dados/04_stf/)).

## Estrutura

```
├── dados/
│   ├── 00_acoes_identificadas/   # camada curada: casos emblemáticos com réus,
│   │                             # fase, nº CNJ verificado e caminho da ficha
│   ├── 01_curitiba_13vara/       # NÚCLEO — 13ª Vara Federal de Curitiba (TRF4)
│   │   ├── acoes_penais/AAAA/    # 1.849 ações penais, 1 JSON por processo
│   │   ├── outras_classes/       # demais 58 classes (inquéritos, buscas,
│   │   │                         # quebras de sigilo…) em .jsonl.gz
│   │   └── indice_13vara.csv     # índice geral com link de consulta por processo
│   ├── 02_trf4_2inst/            # recursos no TRF4 (apelações, embargos…)
│   │   ├── recursos/AAAA/        # 683 fichas individuais
│   │   └── indice_g2.csv
│   ├── 03_stj/                   # STJ: papel na operação e guia de consulta
│   ├── 04_stf/                   # STF: tabela curada (AP 996, 1000, 1002, 1003,
│   │                             # 1025, Inq 3983, 4327…) + links de consulta
│   ├── 05_rj_trf2/               # Lava Jato fluminense — 7ª VFC/RJ completa
│   │   ├── acoes_penais/AAAA/    # 849 ações penais individuais
│   │   ├── outras_classes/
│   │   └── indice_7vfc_rj.csv
│   └── 06_sp_trf3/               # frente paulista: camada curada + fontes
├── docs/
│   ├── dicionario_de_dados.md    # campos, códigos TPU, formato CNJ
│   ├── como_acessar_autos.md     # como abrir os autos em cada tribunal
│   └── NOTA_LEGAL.md             # base legal, LGPD, limites de uso
├── indices/
│   └── fases_operacao.csv        # as 79 fases (nome, data, alvo)
└── scripts/                      # coleta 100% reprodutível (Python, sem
                                  # dependências externas)
```

## Como navegar

- **Quero um caso famoso** → abra
  [`dados/00_acoes_identificadas/acoes_emblematicas.csv`](dados/00_acoes_identificadas/acoes_emblematicas.csv)
  e siga a coluna `ficha_no_acervo`. Ex.: o caso do triplex está em
  `dados/01_curitiba_13vara/acoes_penais/2016/5046512-94.2016.4.04.7000.json`
  — 1.265 movimentações, da distribuição em 14/09/2016 ao último andamento
  registrado em 2026, a apelação correspondente está em
  `dados/02_trf4_2inst/recursos/2016/`.
- **Quero varrer tudo** → use os índices CSV (um por conjunto). Cada linha
  tem número CNJ, classe, assuntos, datas, quantidade de movimentações e o
  **link de consulta pública** no tribunal.
- **Quero as investigações, buscas e quebras de sigilo** → estão em
  `outras_classes/` (JSONL comprimido, uma linha por processo), com todas as
  classes: inquéritos policiais, PIC-MP, pedidos de busca e apreensão,
  quebras de sigilo, prisões preventivas, sequestros de bens, colaborações
  homologadas etc.
- **Quero atualizar ou ampliar** → `scripts/` tem os coletores
  (`baixar_datajud_13vara.py`, `baixar_datajud_orgao.py`, `baixar_trf4_g2.py`)
  e o consultor avulso (`consultar_processo.py <numero>`), todos usando só a
  biblioteca-padrão do Python e a chave pública documentada pelo CNJ.

## Método

1. **DataJud não tem uma etiqueta "Lava Jato"** e a API pública não expõe
   nomes de partes. A forma exaustiva e reprodutível de capturar a operação
   é varrer **os órgãos julgadores que a conduziram**:
   a **13ª Vara Federal de Curitiba** (órgão 11891 — a vara do caso) e a
   **7ª Vara Federal Criminal do Rio de Janeiro** (órgão 12260 — a vara da
   fase fluminense). Este acervo traz o **acervo criminal completo** dessas
   varas, todas as classes, com dedupe por (número, grau).
2. Sobre essa base exaustiva, a **camada curada** identifica nominalmente os
   casos emblemáticos (réus, fase, situação), sempre com o número verificado
   na própria API e fonte citada.
3. A 2ª instância (TRF4) foi coletada por lote de números a partir das 1.849
   ações penais de Curitiba.
4. STF (fora do DataJud) e STJ/SP (identificação inviável sem fonte de
   números) estão documentados com tabelas curadas e guias de consulta.

### O que é este acervo

- ✔️ **É** a ficha íntegra e oficial (CNJ) de cada processo das varas da
  operação, do início ao fim do que foi reportado, mais a curadoria dos
  casos de repercussão em todas as frentes.
- ⚠️ O acervo das varas é um **superconjunto** da Lava Jato em sentido
  estrito: a 13ª Vara é especializada em crimes financeiros desde antes de
  2014 (há ações desde os anos 1970 migradas para o eproc) e seguiu ativa
  depois de 2021. O recorte 2014–2021 concentra o núcleo da operação
  (812 das 1.849 ações penais de Curitiba foram ajuizadas nesse período).
  O mesmo vale para a 7ª VFC/RJ (fase fluminense a partir de 2016).
- ⚠️ **Não** contém os autos digitalizados (restritos às partes nos sistemas
  dos tribunais) nem processos sigilosos (fora da API pública por lei), e
  **não** certifica andamento atual, então consulte sempre o tribunal competente para julgar o processo (links
  prontos nos índices).
- ⚠️ Lacunas da fonte existem e estão anotadas (ex.: o registro de 1º grau
  da ação de Eduardo Cunha não consta da API pública (só a apelação).

## Recomendação: 

- ⚠️ Ler os jornais da época junto aos processos. **Há fatos que não constam nos autos.**

## Fontes

- **CNJ, API Pública do DataJud** (`api-publica.datajud.cnj.jus.br`)
  Resolução CNJ nº 331/2020 sobre dados processuais
- **CNN Brasil**, que contém um catálogo das 79 fases e estatísticas do STF (10 anos da
  operação)
  **TRF4**, notícias e consulta processual
  **STF** (portal e arquivo oficial)
  **Agência Brasil**, **Migalhas**, **Poder360**, **MEON**, **ConJur** (pois continham links de acesso aos autos completos, consulte na tabela).

## Licença e uso

Dados processuais são públicos (fonte: CNJ/DataJud); os scripts estão sob
licença MIT. Leia [`docs/NOTA_LEGAL.md`](docs/NOTA_LEGAL.md) antes de
reutilizar — em especial: nada aqui afirma culpa ou estado atual de processo
algum, e condenações citadas podem ter sido reformadas ou anuladas (casos de
Lula anulados pelo STF em 2021 são o exemplo maior).
