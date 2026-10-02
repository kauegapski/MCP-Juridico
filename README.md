# MCP-Juridico

Base normativa curada e servidor **MCP (Model Context Protocol)** para apoiar, com modelos de linguagem, o trabalho jurídico, de licitações e de TI do **Poder Legislativo de Guarapuava/PR** e a advocacia em geral.

O objetivo é que a IA responda **somente com base em textos oficiais verificáveis**, sabendo a natureza de cada fonte (norma que obriga a Câmara, ato federal de mera referência, orientação de órgão de controle, jurisprudência) e a data da última conferência.

> A base **não substitui** a análise jurídica humana, o parecer jurídico obrigatório, a comissão de contratação ou o agente de contratação. É apoio técnico-informacional.

---

## 1. Como a base está organizada

| Pasta | Conteúdo |
|---|---|
| `CONSTITUCIONAL/` | Constituição Federal (com ADCT) |
| `LEGISLACAO/` | Lei nº 14.133/2021, Decreto nº 12.807/2025 (valores), LC nº 123/2006, Lei nº 4.320/1964, LAI, LGPD e atos federais de referência (INs SEGES/SGD, Portarias SGD) |
| `LEGISLACAO_MUNICIPAL_GUARAPUAVA/` | Lei Orgânica, Regimento Interno da Câmara, LC nº 61/2016 e LC nº 120/2020 |
| `DECRETOS/MUNICIPAIS_GUARAPUAVA/` | Decretos nº 37 a 41/2022 do Poder Legislativo (regulamentação da Lei nº 14.133/2021) |
| `ATOS_TCE_PR/` | IN TCE-PR nº 156/2020 compilada com a IN nº 208/2026 (Mural de Licitações) |
| `TI_E_SEGURANCA/` | Resoluções CD/ANPD nº 15 e 18/2024 e fichas de orientação em LGPD e segurança nas contratações de TIC |
| `MANUAIS_E_GUIAS/` | Fichas de manuais e guias (TCU, TCE-PR, TCE-SC, TCE-RS, SGD, CNJ/CNMP) — sem força normativa |
| `TEMPLATES_OPERACIONAIS/` | Modelos de ETP, TR e memorando do DTI |
| `PENAL/`, `CIVEL/`, `HONORARIOS/`, `JURISPRUDENCIA/` | Advocacia: códigos e leis, tabelas de honorários e súmulas |
| `FERRAMENTAS/` | Scripts de verificação, atualização e metadados |

O mapa completo, arquivo por arquivo, está no **[INDEX.md](INDEX.md)**. As regras de uso (hierarquia das fontes, vedações, jurisprudência somente a pedido) estão no **[PROTOCOLO_DE_USO_MCP.md](PROTOCOLO_DE_USO_MCP.md)**.

### Metadados

Todo arquivo de conteúdo começa com um cabeçalho YAML, por exemplo:

```yaml
---
titulo: "Decreto nº 41/2022 – Poder Legislativo de Guarapuava"
tipo: decreto_municipal
esfera: municipal
natureza: norma_vinculante      # norma_vinculante | norma_referencia | orientacao | jurisprudencia | tabela | modelo
situacao: vigente               # vigente | historico
area: [licitacoes]
fonte: "Boletim Oficial do Município de Guarapuava, Ano XXVIII, nº 2521, ..."
fonte_url: ""
ultima_verificacao: 2026-09-24
arquivo: DECRETOS/MUNICIPAIS_GUARAPUAVA/Decreto_41_2022_Dispensa_Eletronica.md
---
```

Os textos normativos trazem **somente a redação vigente** (trechos riscados das fontes oficiais excluídos), com as anotações de alteração ("Redação dada pela…", "Incluído pela…") preservadas.

---

## 2. Servidor MCP

`server.py` expõe a base, em modo somente leitura, a qualquer cliente MCP (Claude Desktop, Claude Code e outros).

### Instalação

```bash
git clone https://github.com/kauegapski/MCP-Juridico.git
cd MCP-Juridico
pip install -r requirements.txt
python3 server.py        # transporte stdio
```

### Configuração no cliente (exemplo)

```json
{
  "mcpServers": {
    "mcp-juridico": {
      "command": "python3",
      "args": ["/caminho/para/MCP-Juridico/server.py"]
    }
  }
}
```

### Ferramentas disponíveis

| Ferramenta | O que faz |
|---|---|
| `protocolo_de_uso` | Devolve o protocolo (hierarquia e regras). Deve ser consultado antes de fundamentar. |
| `mapa_decretos_municipais` | Indica qual Decreto Municipal (37 a 41/2022) regula cada tema e o arquivo correspondente. |
| `listar_documentos` | Lista os documentos, com filtros por pasta, natureza, área ou termo no título. |
| `buscar_artigo` | Devolve o texto literal de um artigo (aceita apelidos: `14133`, `LGPD`, `LAI`, `CF`, `LOM`, `Regimento Interno`, `Decreto 37/2022`…). |
| `buscar_texto` | Busca termo ou expressão (sem distinção de acentos) e indica arquivo e artigo de cada ocorrência. |
| `ler_documento` | Lê um documento em blocos de até 30 mil caracteres. |
| `valores_vigentes_lei_14133` | Devolve o decreto de atualização dos valores da Lei nº 14.133/2021 vigente na base. |

Toda resposta traz um cabeçalho de procedência (arquivo, natureza, fonte oficial, data da última verificação) e alertas automáticos quando a fonte é orientativa, de referência federal, jurisprudencial ou histórica.

---

## 3. Manutenção

```bash
# 1) Conferir as normas com a fonte oficial (Planalto, gov.br e DOU)
python3 FERRAMENTAS/verificar_atualizacoes.py            # relatório; código 1 se houver mudança
python3 FERRAMENTAS/verificar_atualizacoes.py --marcar   # registra a data nos arquivos sem divergência

# 2) Havendo mudança, reextrair a norma (com autorização) e revisar o diff
python3 FERRAMENTAS/atualizar_norma.py LEGISLACAO/Lei_14133_2021.md
git diff LEGISLACAO/Lei_14133_2021.md

# 3) Manter os metadados coerentes
python3 FERRAMENTAS/gerar_metadados.py           # grava
python3 FERRAMENTAS/gerar_metadados.py --checar  # só verifica
```

Rotina sugerida: verificação mensal e sempre que sair novo decreto de valores da Lei nº 14.133/2021 (atualização anual em 1º de janeiro — art. 182). A verificação automática não alcança o sítio da Câmara (captcha), o Boletim Oficial do Município e o Diário Eletrônico do TCE-PR: esses textos são conferidos manualmente, e o resultado é registrado na linha **Última verificação** do arquivo.

### Incluir um novo documento

1. Criar o `.md` na pasta adequada, com as linhas de cabeçalho `**Fonte oficial:**`, `**URL:**` e `**Última verificação:**`, a "Nota de Uso no MCP" e, para normas, a seção `## Texto integral`.
2. Se for pasta ou padrão de nome novo, incluir a regra de classificação em `FERRAMENTAS/gerar_metadados.py`.
3. Rodar `gerar_metadados.py`, atualizar o `INDEX.md` e fazer o commit.

---

## 4. Cuidados

- **Repositório público:** não incluir dados pessoais, documentos internos não publicados, credenciais ou informações de processos em andamento (LGPD, art. 6º, e LAI, art. 31). Peças e minutas de casos concretos devem ficar fora desta base.
- **Manuais e guias** entram como fichas com link para a fonte oficial, sem reprodução do conteúdo protegido.
- **Jurisprudência** só é usada quando o usuário pede expressamente.
- **Decretos municipais** não se sobrepõem à lei; INs e Portarias federais não obrigam a Câmara, salvo adoção expressa ou recursos federais que as exijam (ver protocolo).

---

## 5. Autoria e licença

Curadoria: Kaue Hansen Gapski Pereira — advogado; Chefe do Departamento de Tecnologia da Informação do Poder Legislativo de Guarapuava. Condições de uso em [LICENSE.md](LICENSE.md).
