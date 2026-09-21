# Como acessar os autos e documentos de cada processo

Este acervo contém a **ficha processual completa** (metadados + todas as
movimentações) de cada processo. Os **autos digitalizados** (petições,
denúncias, provas, sentenças na íntegra) não são distribuídos pela API do
DataJud: ficam nos sistemas processuais de cada tribunal. Este guia mostra
como chegar neles a partir de qualquer número deste acervo.

## Curitiba e TRF4 (1ª e 2ª instância)

- **Consulta unificada TRF4** (aceita o número de 20 dígitos):
  `https://www.trf4.jus.br/trf4/controlador.php?acao=consulta_processual_resultado_pesquisa&selForma=NU&txtValor=<NUMERO20DIGITOS>&selOrigem=TRF&chkMostrarBaixados=1`
  (os índices CSV deste acervo já trazem esse link pronto por processo);
- **eproc JFPR (1º grau)**: `https://eproc.jfpr.jus.br` → Consulta Pública;
- **Jurisprudência TRF4** (acórdãos com inteiro teor):
  `https://jurisprudencia.trf4.jus.br`;
- Sentenças e decisões de grande repercussão também foram publicadas pela
  imprensa especializada (ConJur, JOTA, Migalhas) e constam dos sites do MPF
  (`mpf.mp.br/grandes-casos/lava-jato`) — acessíveis pelo navegador.

## Rio de Janeiro (7ª Vara Federal Criminal / TRF2)

- **eproc JFRJ**: `https://eproc.jfrj.jus.br` → Consulta Pública
  (processos a partir de 2019 e migrados);
- **Consulta processual TRF2**: `https://www.trf2.jus.br` → Consulta
  Processual (aceita número CNJ).

## STF

- Consulta por classe e número: `https://portal.stf.jus.br/processos/`
  (ex.: pesquisar `AP 996`); abas de andamentos, decisões e inteiro teor;
- Jurisprudência: `https://jurisprudencia.stf.jus.br`.

## STJ

- Consulta processual: `https://processo.stj.jus.br/processo/pesquisa/`;
- Jurisprudência/inteiro teor: `https://scon.stj.jus.br/SCON/`.

## São Paulo (TRF3)

- Consulta: `https://web.trf3.jus.br/consultas` e PJe
  (`https://pje1g.trf3.jus.br/pje/ConsultaPublica/listView.seam`).

## O que esperar (e o que não esperar)

1. **Capa e movimentações** são públicas para processos sem sigilo — é o que
   este acervo já entrega offline.
2. **Documentos dos autos** em regra exigem login (advogado/parte) nos
   sistemas eproc/PJe, mesmo em processos públicos; sentenças e acórdãos
   costumam estar acessíveis na consulta pública e nas bases de
   jurisprudência.
3. **Processos sigilosos** (colaborações premiadas, cautelares em segredo)
   não aparecem na API pública do DataJud nem na consulta pública — é uma
   restrição legal, não uma lacuna do acervo.
4. Por que os PDFs não estão neste repositório: os sítios que hospedam os
   documentos (MPF, STF, ConJur, Internet Archive) bloqueiam download
   automatizado a partir de ambientes de nuvem. Os links acima funcionam
   normalmente em navegador; a estrutura do acervo já reserva espaço para
   anexá-los (`documentos/` pode ser criada por caso, se você quiser
   complementar manualmente).
