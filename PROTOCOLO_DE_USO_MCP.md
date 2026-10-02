# Protocolo de Uso do Model Context Protocol (MCP)

## Finalidade

Este Protocolo estabelece as **regras de utilização, hierarquia normativa e limites operacionais** do Model Context Protocol (MCP), aplicável ao uso de modelos de linguagem (LLMs) em atividades jurídicas, administrativas e técnicas relacionadas a licitações, contratos administrativos, tecnologia da informação e governança pública.

O MCP tem por finalidade **reduzir riscos de interpretação indevida**, **evitar inferências normativas automáticas** e **assegurar conformidade jurídica** com a legislação vigente.

---

## Escopo de Aplicação

O MCP aplica-se a:
- Elaboração e análise de documentos de licitação;
- Estudos Técnicos Preliminares (ETP);
- Termos de Referência (TR);
- Pareceres técnicos e jurídicos;
- Memorandos administrativos;
- Análises de conformidade normativa;
- Apoio à tomada de decisão administrativa.

---

## Hierarquia das Fontes Normativas

Para fins de uso do MCP no âmbito do **Poder Legislativo de Guarapuava**, a seguinte hierarquia **deve ser rigorosamente observada**:

1. **Constituição Federal**
2. **Leis Federais** (inclusive leis complementares)  
   - Ex.: Lei nº 14.133/2021, Lei nº 13.709/2018 (LGPD), Lei nº 12.527/2011 (LAI), Lei nº 4.320/1964, LC nº 123/2006
3. **Atos regulamentares federais de aplicação nacional**, editados com fundamento direto em lei nacional  
   - Ex.: Decreto nº 12.807/2025 (valores da Lei nº 14.133/2021, art. 182); Resoluções do Conselho Diretor da ANPD nº 15/2024 e nº 18/2024 (LGPD, art. 55-J, XIII)
4. **Lei Orgânica do Município de Guarapuava e leis municipais**  
   - Ex.: LC Municipal nº 61/2016 (estrutura e cargos da Câmara) e LC Municipal nº 120/2020 (regime jurídico dos servidores)
5. **Regimento Interno da Câmara (Resolução nº 01/2018)**, nas matérias de organização e funcionamento interno do Poder Legislativo
6. **Decretos Municipais do Poder Legislativo de Guarapuava** (nº 37 a 41/2022), regulamentos de execução da Lei nº 14.133/2021
7. **Instruções Normativas e Portarias Federais** (SEGES, SGD e outras), como referência técnica correlata
8. **Orientações e Guias de Órgãos de Controle**
   - TCU
   - TCE-PR
   - ANPD (guias orientativos)
   - outros Tribunais de Contas (TCE-SC, TCE-RS etc.)

**Atos normativos do TCE-PR dirigidos aos jurisdicionados** (ex.: Instrução Normativa nº 156/2020 — Mural de Licitações, compilada com a IN nº 208/2026) obrigam a Câmara no seu objeto próprio (envio e publicidade de informações ao controle externo). Não disputam hierarquia com os decretos municipais, por regerem matéria distinta; em caso de dúvida sobre conflito, a questão deve ser submetida à análise jurídica humana.

### Regras de aplicação da hierarquia

- **Decreto não se sobrepõe à lei.** Os Decretos Municipais nº 37 a 41/2022 são regulamentos de execução: detalham a aplicação da Lei nº 14.133/2021 e não podem contrariá-la, restringi-la ou ampliá-la. Havendo conflito, aplica-se a lei (CF, art. 22, XXVII, e art. 30, I e II).
- **Não há hierarquia entre decreto municipal e IN ou Portaria federal**, por pertencerem a esferas federativas distintas. As INs e Portarias federais de organização administrativa (SEGES, SGD e similares) vinculam a administração federal e **não obrigam a Câmara**, salvo:
  - adoção expressa por ato local, conforme faculta o art. 187 da Lei nº 14.133/2021; ou
  - execução de recursos da União decorrentes de transferências voluntárias, quando o próprio ato federal assim exigir.
- Fora dessas hipóteses, **prevalece o Decreto Municipal correspondente**, e o ato federal pode ser usado apenas como referência técnica, nunca como fundamento obrigatório.
- Orientações e guias de órgãos de controle não possuem força normativa (ver item seguinte).

Em caso de conflito, **prevalece sempre a norma hierarquicamente superior**, observadas as regras acima.

---

## Classificação das Fontes no MCP

As fontes incluídas no MCP são classificadas da seguinte forma:

### 1. Fontes Normativas Primárias
- Constituição, leis federais e municipais, Lei Orgânica e Regimento Interno
- Decretos e demais atos regulamentares (federais de aplicação nacional e municipais)
- Atos normativos do TCE-PR dirigidos aos jurisdicionados
- Instruções Normativas e Portarias federais (na Câmara, apenas conforme as regras de aplicação da hierarquia)

👉 Possuem **caráter vinculante** (no seu âmbito) e podem fundamentar decisões administrativas. No cabeçalho de metadados de cada arquivo, o campo `natureza` indica: `norma_vinculante`, `norma_referencia` (ato federal que não obriga a Câmara), `orientacao`, `jurisprudencia`, `tabela` ou `modelo`; o campo `situacao: historico` sinaliza material baseado em normas revogadas.

### 2. Fontes Orientativas e Interpretativas
- Manuais
- Guias
- Orientações técnicas e notas técnicas (TCU, TCE-PR, ANPD, outros Tribunais de Contas)

👉 **Não possuem força normativa**, servindo apenas como **apoio interpretativo**.

---

## Regras de Uso pelo Modelo de Linguagem

### É EXPRESSAMENTE PERMITIDO:
- Utilizar leis, decretos e INs como base normativa;
- Consultar manuais e guias para contextualização técnica;
- Auxiliar na estruturação de documentos administrativos;
- Sugerir boas práticas, desde que fundamentadas.

### É EXPRESSAMENTE VEDADO:
- Inventar dispositivos legais;
- Criar ou citar jurisprudência não fornecida;
- Inferir obrigações não expressamente previstas em norma;
- Tratar manuais ou guias como se fossem lei;
- Produzir decisões administrativas automáticas.

---

## Uso de Jurisprudência

A utilização de jurisprudência:
- **Somente será admitida se expressamente solicitada pelo usuário**;
- Deve indicar a **fonte oficial**;
- Não poderá ser inferida automaticamente a partir de manuais ou guias.

Na ausência de solicitação expressa, **a jurisprudência não deve ser utilizada**.

---

## Limites Operacionais do MCP

O MCP:
- **Não substitui** a análise jurídica humana;
- **Não decide** processos administrativos;
- **Não emite** parecer jurídico vinculante;
- Atua exclusivamente como **instrumento de apoio técnico e informacional**.

---

## Atualização e Manutenção

- As fontes do MCP devem ser periodicamente revisadas;
- Sempre que houver atualização normativa relevante, o repositório deve ser ajustado;
- A data da última verificação deve constar nos arquivos correspondentes.
- A conferência das normas federais com a fonte oficial é feita por `FERRAMENTAS/verificar_atualizacoes.py` (Planalto, gov.br e DOU); textos municipais (Lei Orgânica, Regimento Interno, LCs, Decretos 37 a 41/2022) e atos do TCE-PR exigem conferência manual na fonte indicada no arquivo.
- Última revisão deste Protocolo: 2026-10-02 (hierarquia completa: Lei Orgânica, Regimento Interno, leis municipais, Resoluções da ANPD e atos do TCE-PR).

---

## Disposição Final

Este Protocolo é de **observância obrigatória** no uso do MCP e deve orientar todas as interações do modelo de linguagem com o conteúdo normativo e técnico aqui disponibilizado.
