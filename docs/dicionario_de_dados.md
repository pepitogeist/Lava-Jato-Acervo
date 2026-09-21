# Dicionário de dados

## Origem

Todos os registros processuais deste acervo vêm da **API Pública do DataJud**
(Base Nacional de Dados do Poder Judiciário, CNJ):
`https://api-publica.datajud.cnj.jus.br` — consultas aos índices
`api_publica_trf4` (Curitiba/TRF4) e `api_publica_trf2` (Rio de Janeiro),
autenticadas com a chave pública documentada pelo CNJ em
`https://datajud-wiki.cnj.jus.br/api-publica/`.

Cada arquivo `.json` (ou linha de `.jsonl`) é o documento `_source` retornado
pela API, **sem alteração de conteúdo** — a única transformação é a ordenação
cronológica do array `movimentos` (do primeiro ao último andamento).

## Campos de cada processo

| Campo | Descrição |
|---|---|
| `numeroProcesso` | Número único CNJ com 20 dígitos, sem pontuação (`NNNNNNNDDAAAAJTROOOO`) |
| `classe.codigo` / `classe.nome` | Classe processual conforme as Tabelas Processuais Unificadas (TPU/CNJ) — ex.: 283 = Ação Penal – Procedimento Ordinário |
| `assuntos[]` | Assuntos TPU do processo (ex.: corrupção ativa, lavagem de dinheiro) |
| `orgaoJulgador.codigo` / `.nome` | Órgão julgador (ex.: 11891 = 13ª Vara Federal de Curitiba; 12260 = 7ª Vara Federal Criminal do RJ) |
| `dataAjuizamento` | Data/hora do ajuizamento, formato `AAAAMMDDHHMMSS` |
| `movimentos[]` | **Todas as movimentações** registradas: `codigo` e `nome` TPU, `dataHora`, complementos tabelados e, quando houver, órgão julgador do ato |
| `grau` | `G1` = 1ª instância; `G2` = 2ª instância (TRF) |
| `nivelSigilo` | 0 = público. Processos sigilosos não aparecem (ou aparecem sem conteúdo) na API pública |
| `sistema`, `formato` | Sistema de tramitação (eproc etc.) e formato (eletrônico/físico) |
| `dataHoraUltimaAtualizacao`, `@timestamp` | Última atualização do registro na base do CNJ |
| `id` / `_id` | Identificador do registro no DataJud (ex.: `TRF4_G1_<numero>`) |

Os **códigos de movimento** seguem a tabela nacional do CNJ e podem ser
consultados em `https://www.cnj.jus.br/sgt/consulta_publica_movimentos.php`
(o campo `nome` já traz a descrição por extenso).

## Formato do número CNJ

`NNNNNNN-DD.AAAA.J.TR.OOOO`
- `NNNNNNN` sequencial; `DD` dígito verificador; `AAAA` ano de autuação;
- `J` segmento (4 = Justiça Federal; 3 = STJ; 1 = STF*);
- `TR` tribunal (04 = TRF4; 02 = TRF2; 03 = TRF3; 00 = tribunal superior);
- `OOOO` unidade de origem (7000 = Subseção de Curitiba; 5101 = Subseção do RJ).

\* O STF usa números próprios por classe (AP 996, Inq 4327) na comunicação
pública.

## Índices CSV

Cada pasta de dados tem um índice com uma linha por processo:
`numero_processo` (20 dígitos), `numero_cnj` (formatado), `classe_codigo`,
`classe_nome`, `assuntos`, `data_ajuizamento` (AAAA-MM-DD),
`ultima_atualizacao`, `qtd_movimentos`, `grau`, `formato` e, quando presente,
`link_consulta` (consulta processual pública do tribunal).

## Avisos de qualidade

- O DataJud tem registros duplicados ocasionais; a coleta deduplicou por
  (`numeroProcesso`, `grau`), o que explica pequenas diferenças entre o total
  de documentos do índice do CNJ e o total de processos salvos.
- Movimentações refletem o que os tribunais reportaram ao CNJ; lacunas e
  atrasos de reporte existem, sobretudo em processos antigos ou migrados.
- Processos redistribuídos a outros tribunais (após decisões do STF de
  2021) seguem tramitando fora do TRF4/TRF2; a ficha aqui registra o que o
  tribunal de origem reportou.
