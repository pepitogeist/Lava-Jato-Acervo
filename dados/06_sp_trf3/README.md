# Lava Jato em São Paulo (TRF3)

A frente paulista da Lava Jato (força-tarefa do MPF-SP com a Justiça Federal
de São Paulo) foi menor e mais difusa que as de Curitiba e do Rio: as ações
tramitaram em varas criminais federais comuns da capital (sobretudo a
**5ª Vara Criminal Federal de São Paulo**), que não são varas "da operação" —
uma varredura completa dessas varas traria milhares de casos sem relação com
a Lava Jato, e a API pública do DataJud não expõe nomes de partes que
permitissem filtrar.

Por isso esta pasta traz a **camada curada** da frente paulista, com fontes,
e o caminho para reproduzir a consulta de qualquer número que se obtenha.

## Casos documentados

### Paulo Vieira de Souza ("Paulo Preto"), ex-diretor da Dersa
- **Vara**: 5ª Vara Criminal Federal de São Paulo (juíza Maria Isabel do Prado)
- **Condenações noticiadas**: 27 anos (2018, peculato/organização criminosa —
  desvios do Rodoanel Sul e sistema viário) e 145 anos (2019, desvio de
  recursos de desapropriações do Rodoanel Sul); decisões posteriores anularam
  ao menos uma das condenações (2021+).
- **Relação com a operação**: fase 60 da LJ/PR ("Ad Infinitum", fev/2019,
  contra o mesmo alvo) e operações próprias da LJ-SP.
- **Número CNJ**: não confirmado em fonte aberta acessível a partir deste
  ambiente (o site do MPF bloqueou o acesso automatizado). Com o número em
  mãos, a ficha completa sai do DataJud com
  `scripts/consultar_processo.py <numero> api_publica_trf3`.
- Fontes: Poder360 (27/09/2018); MPF-SP (sala de imprensa, 2019); Terra/MEON.

### Outros marcos da LJ-SP
- Investigações sobre cartel/propinas em obras estaduais (Dersa/Rodoanel) e
  desdobramentos de colaborações da Odebrecht;
- Parte dos casos paulistas correu sob segredo de justiça, sem registro
  público detalhado.

## Como consultar

- Consulta processual TRF3/JFSP: `https://web.trf3.jus.br/consultas` e
  `https://pje1g.trf3.jus.br/pje/ConsultaPublica/listView.seam`;
- DataJud (índice `api_publica_trf3`) com os scripts deste repositório.
