#!/usr/bin/env python3
"""Gera (ou atualiza) o cabeçalho YAML de metadados de todos os arquivos da base.

Campos gravados no topo de cada .md (entre linhas '---'):
  titulo, tipo, esfera, natureza, situacao, area, fonte, fonte_url, ultima_verificacao, arquivo

- fonte: descrição textual da fonte oficial (linha **Fonte oficial:** ou equivalente). Para atos
  sem página web própria (ex.: Decretos Municipais 37-41/2022, publicados no Boletim Oficial do
  Município), fonte_url fica vazio e a referência de publicação vai em "fonte".
- situacao: "historico" quando o arquivo traz o aviso MATERIAL HISTÓRICO; senão "vigente".
- ultima_verificacao: data da linha **Última verificação:** (normas e fichas) ou
  **Última revisão:** (modelos).

- natureza:
    norma_vinculante  -> obriga o Poder Legislativo de Guarapuava
    norma_referencia  -> ato federal regulamentar sem vinculação direta à Câmara
                         (art. 187 da Lei nº 14.133/2021; ver PROTOCOLO_DE_USO_MCP.md)
    orientacao        -> manual, guia, nota técnica, ficha (sem força normativa)
    jurisprudencia    -> súmulas (uso só a pedido expresso)
    tabela            -> tabelas de honorários
    modelo            -> templates operacionais
- A classificação é feita pela pasta e pelo nome do arquivo (regras abaixo). Arquivo novo
  em pasta nova ou com nome fora do padrão deve ganhar regra aqui.

Uso:  python3 FERRAMENTAS/gerar_metadados.py          (grava)
      python3 FERRAMENTAS/gerar_metadados.py --checar (só lista o que mudaria; código 1 se houver)
"""
import argparse, glob, os, re, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IGNORAR = {"INDEX.md", "README.md", "PROTOCOLO_DE_USO_MCP.md", "LICENSE.md"}

def classificar(rel):
    p, f = os.path.dirname(rel), os.path.basename(rel)
    if p == "CONSTITUCIONAL":
        return "constituicao", "federal", "norma_vinculante", ["constitucional"]
    if p in ("PENAL", "CIVEL"):
        tipo = "decreto_lei" if "_DL_" in f else "lei_federal"
        return tipo, "federal", "norma_vinculante", [p.lower()]
    if p == "LEGISLACAO":
        regras = [
            (r"^Lei_14133", ("lei_federal", "norma_vinculante", ["licitacoes"])),
            (r"^Decreto_12807", ("decreto_federal", "norma_vinculante", ["licitacoes"])),
            (r"^LC_123", ("lei_complementar_federal", "norma_vinculante", ["licitacoes"])),
            (r"^Lei_4320", ("lei_federal", "norma_vinculante", ["financas_publicas"])),
            (r"^Lei_12527", ("lei_federal", "norma_vinculante", ["transparencia"])),
            (r"^Lei_13709", ("lei_federal", "norma_vinculante", ["lgpd"])),
            (r"^IN_SEGES", ("instrucao_normativa_federal", "norma_referencia", ["licitacoes"])),
            (r"^IN_SGD", ("instrucao_normativa_federal", "norma_referencia", ["licitacoes", "ti"])),
            (r"^Portaria_SGD", ("portaria_federal", "norma_referencia", ["licitacoes", "ti"])),
        ]
        for rx, (tipo, nat, area) in regras:
            if re.search(rx, f):
                return tipo, "federal", nat, area
    if p == "DECRETOS/MUNICIPAIS_GUARAPUAVA":
        return "decreto_municipal", "municipal", "norma_vinculante", ["licitacoes"]
    if p == "LEGISLACAO_MUNICIPAL_GUARAPUAVA":
        if f.startswith("Lei_Organica"):
            return "lei_organica_municipal", "municipal", "norma_vinculante", ["administracao_camara"]
        if f.startswith("Regimento"):
            return "regimento_interno", "municipal", "norma_vinculante", ["administracao_camara"]
        return "lei_complementar_municipal", "municipal", "norma_vinculante", ["administracao_camara", "pessoal"]
    if p == "ATOS_TCE_PR":
        return "ato_tce_pr", "estadual", "norma_vinculante", ["licitacoes", "controle_externo"]
    if p == "TI_E_SEGURANCA":
        if f.startswith("Resolucao_CD_ANPD"):
            return "resolucao_anpd", "federal", "norma_vinculante", ["lgpd", "ti"]
        return "orientacao", "federal", "orientacao", ["lgpd", "ti"]
    if p == "MANUAIS_E_GUIAS":
        esf = "estadual" if f.startswith("TCE_") else "federal"
        area = ["licitacoes", "ti"] if re.search(r"TI|TIC|Software|Sistema|SGD|CNJ", f) else ["licitacoes"]
        return "orientacao", esf, "orientacao", area
    if p == "JURISPRUDENCIA":
        return "sumulas", "federal", "jurisprudencia", ["jurisprudencia"]
    if p == "HONORARIOS":
        return ("resolucao_estadual" if "PGE" in f else "tabela_oab"), "estadual", "tabela", ["honorarios"]
    if p == "TEMPLATES_OPERACIONAIS":
        return "modelo", "municipal", "modelo", ["licitacoes"]
    return None

def separar(md):
    if md.startswith("---\n"):
        fim = md.find("\n---\n", 4)
        if fim > 0:
            return md[4:fim], md[fim + 5:].lstrip("\n")
    return None, md

def extrair(corpo, chave_rx):
    m = re.search(chave_rx, corpo, re.M)
    return m.group(1).strip() if m else ""

def yq(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'

def gerar(rel, corpo):
    c = classificar(rel)
    if not c:
        return None
    tipo, esfera, nat, area = c
    titulo = extrair(corpo, r"^# (.+)$")
    url = extrair(corpo, r"^\*\*URL(?: oficial)?(?: \([^)]*\))?:\*\*\s*(https?://\S+)") or \
          extrair(corpo, r"^\*\*URL(?: oficial)?:\*\*\s*\n(https?://\S+)") or \
          extrair(corpo, r"^\*\*Onde localizar:\*\*.*?(https?://[^\s)]+)") or \
          extrair(corpo, r"^\*\*Fonte:\*\*.*?\((https?://[^)\s]+)\)") or \
          extrair(corpo, r"^\*\*(?:Texto original|Fonte oficial):\*\*.*?(https?://[^\s)]+)")
    data = extrair(corpo, r"^\*\*Última (?:verificação(?: da fonte)?|revisão):\*\*\s*(\d{4}-\d{2}-\d{2})")
    fonte = next((v for k in ("Fonte oficial", "Fonte normativa federal", "Fonte", "Órgãos emissores", "Órgão emissor")
                  if (v := extrair(corpo, r"^\*\*" + k + r":\*\*\s*(.+?)\s*$"))), "")
    fonte = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", fonte)      # link markdown -> texto
    situacao = "historico" if "MATERIAL HISTÓRICO" in corpo[:3000] else "vigente"
    linhas = ["---", f"titulo: {yq(titulo)}", f"tipo: {tipo}", f"esfera: {esfera}", f"natureza: {nat}",
              f"situacao: {situacao}", "area: [" + ", ".join(area) + "]", f"fonte: {yq(fonte)}", f"fonte_url: {yq(url)}",
              f"ultima_verificacao: {data or 'null'}", f"arquivo: {rel}", "---", ""]
    return "\n".join(linhas) + "\n" + corpo

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--checar", action="store_true")
    a = ap.parse_args()
    mudou = []
    for arq in sorted(glob.glob(os.path.join(RAIZ, "**", "*.md"), recursive=True)):
        rel = os.path.relpath(arq, RAIZ).replace(os.sep, "/")
        if rel in IGNORAR or rel.startswith("."):
            continue
        md = open(arq, encoding="utf-8").read()
        _, corpo = separar(md)
        novo = gerar(rel, corpo)
        if novo is None:
            print(f"[SEM REGRA] {rel}")
            continue
        if novo != md:
            mudou.append(rel)
            if not a.checar:
                open(arq, "w", encoding="utf-8").write(novo)
    print(f"{len(mudou)} arquivo(s) {'a atualizar' if a.checar else 'atualizado(s)'}")
    for r in mudou:
        print("  " + r)
    sys.exit(1 if (a.checar and mudou) else 0)

if __name__ == "__main__":
    main()
