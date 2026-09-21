# Ações emblemáticas identificadas

Esta pasta traz a **camada curada** do acervo: as ações penais e processos da
Operação Lava Jato identificados nominalmente (caso, réus principais, fase da
operação), com o número CNJ verificado na API pública do DataJud e o caminho da
ficha completa dentro deste repositório.

## Arquivo

- `acoes_emblematicas.csv` — uma linha por caso identificado, nas frentes de
  Curitiba, Rio de Janeiro, STF e São Paulo.

## Critérios

1. **Número verificado**: todo número CNJ listado foi confirmado na API pública
   do DataJud/CNJ (existe, é da classe e do órgão julgador indicados).
2. **Atribuição confirmada**: o vínculo número ↔ caso/réus consta de fonte
   pública (notícia oficial do tribunal, MPF ou imprensa) ou é de conhecimento
   público amplamente documentado. Quando o vínculo é apenas provável, a coluna
   `situacao_confianca` diz isso expressamente.
3. **Nada aqui é exaustivo**: a operação teve centenas de ações. A lista
   exaustiva (sem atribuição nominal) está nas varreduras completas em
   `01_curitiba_13vara/` e `05_rj_trf2/`. Esta pasta destaca apenas os casos de
   maior repercussão.

## Observações importantes

- As condenações de Lula (triplex e sítio) foram **anuladas** pelo STF em 2021
  (incompetência da 13ª Vara e suspeição do juiz); os registros processuais
  permanecem no acervo como documento histórico.
- Vários processos de Curitiba foram redistribuídos a outras seções judiciárias
  (DF, SP) após 2021; a ficha do DataJud/TRF4 registra a tramitação até a
  redistribuição e os andamentos posteriores no próprio TRF4, quando houve.
- O STF não integra o DataJud; os casos do STF estão referenciados por classe e
  número (AP 996 etc.) com links de consulta em `04_stf/`.
