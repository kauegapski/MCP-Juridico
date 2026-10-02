# Índice Geral do MCP-Juridico

Mapa de navegação da base. O uso de qualquer arquivo observa o **PROTOCOLO_DE_USO_MCP.md** (hierarquia das fontes, vedações e jurisprudência só a pedido).

Cada arquivo de conteúdo começa com um cabeçalho de metadados (YAML) com `titulo`, `tipo`, `esfera`, `natureza`, `situacao`, `area`, `fonte`, `fonte_url`, `ultima_verificacao` e `arquivo`. Valores de `natureza`:

| natureza | significado |
|---|---|
| `norma_vinculante` | obriga o Poder Legislativo de Guarapuava (no seu âmbito) |
| `norma_referencia` | ato federal (IN/Portaria) que **não** obriga a Câmara, salvo adoção expressa ou recursos federais (art. 187 da Lei nº 14.133/2021) |
| `orientacao` | manual, guia ou nota técnica — **não é norma** |
| `jurisprudencia` | súmulas — uso somente a pedido expresso |
| `tabela` | tabelas de honorários |
| `modelo` | templates operacionais |

---

## 1. Governança da base

- **PROTOCOLO_DE_USO_MCP.md** — hierarquia das fontes, regras de aplicação, vedações, jurisprudência, manutenção
- **README.md** — apresentação, estrutura, como usar o servidor MCP e as ferramentas
- **LICENSE.md** — direitos sobre a curadoria (textos oficiais não são protegidos — Lei nº 9.610/1998, art. 8º, IV)
- **server.py** — servidor MCP (somente leitura) que expõe a base às IAs
- **requirements.txt** — dependências do servidor e das ferramentas

---

## 2. Constituição

📁 **CONSTITUCIONAL/**
- Constituição Federal de 1988 (inclui o ADCT) — `Constituicao_Federal_1988.md`

---

## 3. Legislação federal — licitações, finanças, transparência e LGPD

📁 **LEGISLACAO/** — normas vinculantes (redação vigente; trechos riscados excluídos)
- Lei nº 14.133/2021 — Licitações e Contratos Administrativos — `Lei_14133_2021.md`
- Decreto nº 12.807/2025 — valores da Lei nº 14.133/2021 vigentes em 2026 — `Decreto_12807_2025_Atualizacao_Valores_Lei_14133.md`
- Lei Complementar nº 123/2006 — Estatuto da ME/EPP (tratamento diferenciado nas licitações: arts. 42 a 49) — `LC_123_2006_Estatuto_ME_EPP.md`
- Lei nº 4.320/1964 — normas gerais de Direito Financeiro (empenho, liquidação, pagamento) — `Lei_4320_1964_Direito_Financeiro.md`
- Lei nº 12.527/2011 — Lei de Acesso à Informação — `Lei_12527_2011_Acesso_Informacao.md`
- Lei nº 13.709/2018 — LGPD — `Lei_13709_2018_LGPD.md`

📁 **LEGISLACAO/** — atos federais de referência (`norma_referencia`: não obrigam a Câmara, salvo adoção expressa ou recursos da União que os exijam)
- IN SEGES/ME nº 58/2022 — Estudo Técnico Preliminar — `IN_SEGES_58_2022_ETP.md`
- IN SEGES/ME nº 65/2021 — Pesquisa de preços — `IN_SEGES_65_2021_Pesquisa_Precos.md`
- IN SEGES/ME nº 67/2021 — Dispensa eletrônica — `IN_SEGES_67_2021_Dispensa_Eletronica.md`
- IN SEGES/ME nº 81/2022 — Termo de Referência — `IN_SEGES_81_2022_Termo_Referencia.md`
- IN SGD/ME nº 94/2022 — contratação de soluções de TIC — `IN_SGD_94_2022_Contratacao_TIC.md`
- Portaria SGD/MGI nº 5.950/2023 — software (licença, cessão temporária/“locação”, SaaS) e nuvem — `Portaria_SGD_MGI_5950_2023_Software_Nuvem.md`
- Portaria SGD/MGI nº 370/2023 — outsourcing de impressão — `Portaria_SGD_MGI_370_2023_Outsourcing_Impressao.md`

---

## 4. Normas municipais — Guarapuava

📁 **LEGISLACAO_MUNICIPAL_GUARAPUAVA/** — redação vigente extraída do Sistema Legislativo da Câmara
- Lei Orgânica do Município (consolidada até a Emenda nº 033/2025; competências do Presidente da Câmara no art. 31) — `Lei_Organica_Municipal_Guarapuava.md`
- Regimento Interno da Câmara — Resolução nº 01/2018 (compilado; competências do Presidente no art. 60) — `Regimento_Interno_Camara_Guarapuava_Resolucao_01_2018.md`
- LC Municipal nº 61/2016 — estrutura, cargos e atribuições da Câmara (competências do DTI: Anexo V, art. 30) — `LC_61_2016_Estrutura_Cargos_Camara_Guarapuava.md`
- LC Municipal nº 120/2020 — regime jurídico dos servidores (aplicável no que couber à Câmara) — `LC_120_2020_Estatuto_Servidores_Guarapuava.md`

📁 **DECRETOS/MUNICIPAIS_GUARAPUAVA/** — decretos do Poder Legislativo que regulamentam a Lei nº 14.133/2021 (texto integral do Boletim Oficial nº 2521, de 15/12/2022)

| Tema | Decreto | Arquivo |
|---|---|---|
| Governança, PCA, fase preparatória, DFD, **ETP (arts. 11 e 12)**, padronização, gestão e fiscalização, IMR | nº 37/2022 | `Decreto_37_2022_Governanca.md` |
| Pesquisa de preços | nº 38/2022 | `Decreto_38_2022_Pesquisa_Precos.md` |
| **Termo de Referência** (elaborado pelo Diretor de Gestão Administrativa — art. 1º, § 1º) | nº 39/2022 | `Decreto_39_2022_Termo_Referencia.md` |
| Compra direta de pequena monta / pronto pagamento (art. 95, § 2º, da Lei) — **não** trata da dispensa por valor | nº 40/2022 | `Decreto_40_2022_Compra_Direta.md` |
| Dispensa eletrônica, **inclusive dispensa por valor** (art. 75 da Lei) | nº 41/2022 | `Decreto_41_2022_Dispensa_Eletronica.md` |

---

## 5. Atos normativos do TCE-PR

📁 **ATOS_TCE_PR/** — vinculantes para os jurisdicionados no seu objeto
- IN TCE-PR nº 156/2020 — Mural de Licitações Municipais, **compilada com a IN nº 208/2026** (efeitos a partir de 01/05/2026; texto da IN 208 anexado) — `IN_156_2020_Mural_Licitacoes_compilada_IN_208_2026.md`

---

## 6. TI, segurança da informação e LGPD

📁 **TI_E_SEGURANCA/**
- Resolução CD/ANPD nº 15/2024 — comunicação de incidente de segurança (norma) — `Resolucao_CD_ANPD_15_2024_Comunicacao_Incidentes.md`
- Resolução CD/ANPD nº 18/2024 — atuação do encarregado (norma) — `Resolucao_CD_ANPD_18_2024_Encarregado.md`
- ANPD — Guia orientativo: tratamento de dados pessoais pelo Poder Público (ficha) — `ANPD_Guia_Poder_Publico.md`
- Requisitos de segurança, privacidade e LGPD em contratações de TIC (IN SGD 94/2022, item 7 do Anexo; Parecer CNMLC/AGU 04/2022) (ficha) — `SGD_Requisitos_Seguranca_Privacidade_Contratacoes_TIC.md`

---

## 7. Manuais, guias e orientações (fichas — sem força normativa)

📁 **MANUAIS_E_GUIAS/** — cada ficha descreve o material e aponta a fonte oficial; o conteúdo integral fica no órgão emissor.

Gerais:
- TCU — Licitações e Contratos: Orientações e Jurisprudência, 5ª ed. (2024) — `TCU_Licitacoes_Contratos_Orientacoes_Jurisprudencia_5ed_2024.md`
- TCE-PR — Prejulgados e consultas sobre licitações — `TCE_PR_Prejulgados_Consultas_Licitacoes.md`
- TCE-PR — Cartilha de ETP de obras e serviços de engenharia — `TCE_PR_Cartilha_ETP_Obras_Servicos_Engenharia.md`
- TCE-PR — Manual de Licitações, 3ª ed. (2021) — ⚠️ **histórico** (base em norma revogada) — `TCE_PR_Manual_Licitacoes.md`

Tecnologia da Informação:
- TCU — Guia de Boas Práticas em Contratação de Soluções de TI — `TCU_Guia_Boas_Praticas_Contratacao_Solucoes_TI.md`
- TCU — Nota Técnica AudTI nº 8/2023 (orçamento estimado de TI) — `TCU_Nota_Tecnica_AudTI_8_2023_Orcamento_TI.md`
- SGD/MGI — modelos e orientações de contratação de TIC — `SGD_Modelos_Orientacoes_Contratacao_TIC.md`
- TCE-SC — Nota Técnica nº TC-19/2026 (softwares de gestão) — `TCE_SC_Nota_Tecnica_19_2026_Softwares_Gestao.md`
- TCE-RS — Cartilha de Contratação de Sistema de Gestão Municipal v2.0 (locação e aquisição) — `TCE_RS_Cartilha_Contratacao_Sistema_Gestao_Municipal_v2.md`
- TCE-RS — Catálogos de Soluções de TIC e Guia de Governança das Contratações — `TCE_RS_Catalogos_TIC_Governanca_Contratacoes.md`
- CNJ e CNMP — guias de contratações de TI (referência comparada) — `CNJ_CNMP_Guias_Contratacoes_TI.md`

---

## 8. Modelos operacionais

📁 **TEMPLATES_OPERACIONAIS/**
- Modelo de ETP (Lei nº 14.133/2021, art. 18, § 1º; Decreto Municipal nº 37/2022, arts. 11 e 12) — `Template_ETP_Lei_14133.md`
- Modelo de TR (Lei nº 14.133/2021, art. 6º, XXIII; Decreto Municipal nº 39/2022) — `Template_TR_Lei_14133.md`
- Modelo de memorando do DTI (sem número; data à direita; De/Para/Assunto; fecho padrão) — `Template_Memorando_Tecnico_Administrativo.md`

---

## 9. Advocacia — Penal

📁 **PENAL/**
- Código Penal (DL nº 2.848/1940) — `Codigo_Penal_DL_2848_1940.md`
- Código de Processo Penal (DL nº 3.689/1941) — `Codigo_Processo_Penal_DL_3689_1941.md`
- Lei de Execução Penal (Lei nº 7.210/1984) — `Lei_7210_1984_Execucao_Penal.md`
- Lei de Drogas (Lei nº 11.343/2006) — `Lei_11343_2006_Drogas.md`
- Juizados Especiais (Lei nº 9.099/1995) — `Lei_9099_1995_Juizados_Especiais.md`
- Crimes Hediondos (Lei nº 8.072/1990) — `Lei_8072_1990_Crimes_Hediondos.md`
- Lei Maria da Penha (Lei nº 11.340/2006) — `Lei_11340_2006_Maria_da_Penha.md`
- Estatuto do Desarmamento (Lei nº 10.826/2003) — `Lei_10826_2003_Estatuto_Desarmamento.md`
- Crimes resultantes de preconceito (Lei nº 7.716/1989) — `Lei_7716_1989_Crimes_Preconceito.md`
- Organização Criminosa (Lei nº 12.850/2013) — `Lei_12850_2013_Organizacao_Criminosa.md`
- Código de Trânsito Brasileiro (Lei nº 9.503/1997; crimes: arts. 291 a 312-B) — `Lei_9503_1997_Codigo_Transito.md`
- Abuso de Autoridade (Lei nº 13.869/2019) — `Lei_13869_2019_Abuso_Autoridade.md`
- Interceptação Telefônica (Lei nº 9.296/1996) — `Lei_9296_1996_Interceptacao_Telefonica.md`
- ECA (Lei nº 8.069/1990; também de uso cível e de família) — `Lei_8069_1990_ECA.md`

## 10. Advocacia — Cível, Família e Empresarial

📁 **CIVEL/**
- Código Civil (Lei nº 10.406/2002) — `Codigo_Civil_Lei_10406_2002.md`
- Código de Processo Civil (Lei nº 13.105/2015) — `Codigo_Processo_Civil_Lei_13105_2015.md`
- Recuperação Judicial e Falência (Lei nº 11.101/2005) — `Lei_11101_2005_Recuperacao_Falencia.md`
- Ação de Alimentos (Lei nº 5.478/1968) — `Lei_5478_1968_Alimentos.md`
- Lei do Inquilinato (Lei nº 8.245/1991) — `Lei_8245_1991_Inquilinato.md`
- Código de Defesa do Consumidor (Lei nº 8.078/1990) — `Lei_8078_1990_CDC.md`
- Estatuto da Pessoa com Deficiência (Lei nº 13.146/2015; curatela: arts. 84 a 87) — `Lei_13146_2015_Estatuto_Pessoa_Deficiencia.md`

## 11. Advocacia — Honorários

📁 **HONORARIOS/**
- Advocacia dativa no Paraná — Resolução Conjunta nº 06/2024 PGE/SEFA — `Resolucao_Conjunta_06_2024_PGE_SEFA_Tabela_Dativos.md`
- Tabela de Honorários da OAB/PR 2026 — `Tabela_Honorarios_OAB_PR_2026.md`

## 12. Jurisprudência sumulada (uso somente a pedido expresso)

📁 **JURISPRUDENCIA/**
- Súmulas Vinculantes do STF — `STF_Sumulas_Vinculantes.md`
- Súmulas do STF — `STF_Sumulas.md`
- Súmulas do STJ — `STJ_Sumulas.md`

---

## 13. Ferramentas de manutenção

📁 **FERRAMENTAS/**
- `verificar_atualizacoes.py` — compara as normas com a fonte oficial (Planalto, gov.br e DOU) e lista trechos novos/alterados e leis alteradoras ausentes. `--marcar` registra a data nos arquivos conferidos sem divergência.
- `atualizar_norma.py` — reextrai o texto vigente de uma norma e reescreve a seção “Texto integral”, preservando cabeçalho e nota de uso (usar somente com autorização do Dr. Kaue e revisar o `git diff`).
- `gerar_metadados.py` — gera/atualiza o cabeçalho YAML de todos os arquivos; `--checar` aponta arquivos desatualizados.

Conferência manual (não automatizável a partir da nuvem): Lei Orgânica, Regimento Interno e LCs municipais (sítio da Câmara, protegido por captcha), Decretos 37 a 41/2022 (Boletim Oficial) e atos do TCE-PR (Diário Eletrônico em PDF).

---

Este índice é instrumento de navegação e não cria obrigações. Em dúvida sobre hierarquia ou interpretação, prevalece o **PROTOCOLO_DE_USO_MCP.md**.
