# Lava Jato no STJ

O STJ **integra o DataJud** (índice `api_publica_stj`), e este acervo consultou
esse índice. A dificuldade específica do STJ é de **identificação**, não de
acesso: 

1. Recursos e habeas corpus recebem no STJ um **número CNJ novo**
   (`NNNNNNN-DD.AAAA.3.00.0000`), diferente do número de origem
   (Curitiba/TRF4 etc.);
2. A imprensa e o próprio STJ citam os casos pelo **número de registro**
   (ex.: `HC 434.766/PR`, `REsp 1.765.139/PR`), que **não consta** dos campos
   da API pública do DataJud;
3. A API pública não expõe nomes de partes (proteção de dados), o que
   inviabiliza filtrar "casos Lava Jato" diretamente.

Sem uma tabela oficial de correspondência acessível por aqui, optamos por
**não chutar números**: em vez de uma varredura com falsos positivos, esta
pasta documenta os papéis do STJ na operação e como consultar cada caso.

## Papéis do STJ na Lava Jato

- **Recursos (REsp/AREsp) e habeas corpus** contra decisões do TRF4, TRF2 e
  TRF3 — ex.: o STJ reduziu em 2019 a pena de Lula no caso do triplex
  (HC/REsp da defesa) antes da anulação pelo STF em 2021;
- **Ações penais originárias (APn)** contra governadores em exercício —
  ex.: a fase fluminense atingiu governadores do RJ; quando perderam o cargo,
  os processos desceram à 7ª Vara Federal Criminal do RJ
  (ver `05_rj_trf2/`, que inclui as ações de Pezão e Witzel na 1ª instância
  quando aplicável);
- **Conflitos de competência e cautelares** ligados à operação.

## Como consultar

- Consulta processual: `https://processo.stj.jus.br/processo/pesquisa/`
  (aceita número de registro, número CNJ ou nome da parte);
- Jurisprudência (acórdãos, inteiro teor): `https://scon.stj.jus.br/SCON/`;
- Pesquisando por "operação lava jato" na jurisprudência do STJ é possível
  recuperar os acórdãos e, a partir deles, os números CNJ — que podem então
  ser consultados no DataJud com os scripts em `scripts/` deste repositório.
