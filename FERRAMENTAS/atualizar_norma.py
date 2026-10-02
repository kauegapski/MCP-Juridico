#!/usr/bin/env python3
"""Reextrai da fonte oficial o texto vigente de uma norma da base e reescreve o arquivo .md.

Fontes: as mesmas de verificar_atualizacoes.py (Planalto, www.gov.br, www.in.gov.br).
Mantém o cabeçalho e a "Nota de Uso no MCP" do arquivo; substitui apenas a seção
"## Texto integral" e atualiza a linha **Última verificação:** e o campo
ultima_verificacao do cabeçalho YAML. Revise o diff (git diff) antes de publicar.
Uso:  python3 FERRAMENTAS/atualizar_norma.py CIVEL/Lei_8078_1990_CDC.md [--saida outro.md]
Use somente com autorização do Dr. Kaue, depois de conferir o relatório de verificar_atualizacoes.py.
"""
import argparse, datetime, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verificar_atualizacoes import baixar, paragrafos_oficiais, RUIDO

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("arquivo")
    ap.add_argument("--saida")
    a = ap.parse_args()
    md = open(a.arquivo, encoding="utf-8").read()
    url = re.search(r"^\*\*URL:\*\*\s*(\S+)", md, re.M).group(1)
    def limpa(p):
        p = re.sub(r"\s+", " ", p).strip()
        p = re.sub(r"\s+([.,;:)])", r"\1", p)
        p = re.sub(r"\b(\d+) o\b", r"\1º", p)        # 6 o (sobrescrito) -> 6º
        p = re.sub(r"\b(\d+) º", r"\1º", p)
        p = re.sub(r"\b([Nn]) o\b", r"\1º", p)        # n o -> nº
        return re.sub(r"\(\s+", "(", p)
    paras = [limpa(p) for p in paragrafos_oficiais(baixar(url), url)]
    paras = [p for p in paras if not re.fullmatch(r"(\((Revogad[oa]|Vide)[^)]*\)\s*)+", p)]
    paras = [p for p in paras if not re.fullmatch(r"(Regulamento|Vig[eê]ncia|Mensagem de veto|Convers[aã]o da Medida Provis[oó]ria.*)( .*)?", p) or len(p) > 60]
    # descarta o cabeçalho do Planalto até o título da norma
    ini = next((i for i, p in enumerate(paras)
                if re.match(r"^(LEI|DECRETO|DECRETO-LEI|LEI COMPLEMENTAR|CONSTITUI|INSTRU|PORTARIA|RESOLU)", p, re.I) and re.search(r"\d{4}", p)), None)
    paras = [p for p in paras[ini or 0:] if not re.match(r"^(Presid[eê]ncia|Secretaria|Subchefia|Casa Civil)", p)]
    if ini is not None:            # título da norma em negrito (no gov.br/DOU o título fica fora da área de texto)
        paras[0] = "**" + paras[0].rstrip(" .") + "**"
    i = md.find("## Texto integral")
    if i < 0:
        sys.exit("Arquivo sem a seção '## Texto integral'")
    cab = md[:i]
    hoje = datetime.date.today().isoformat()
    cab = re.sub(r"^\*\*Última verificação:\*\*.*$",
                 f"**Última verificação:** {hoje} (texto vigente reextraído da página oficial em {hoje})  ", cab, count=1, flags=re.M)
    cab = re.sub(r"^ultima_verificacao:.*$", f"ultima_verificacao: {hoje}", cab, count=1, flags=re.M)
    sec = md[i:].split("\n", 1)[0]
    out = cab + sec + "\n\n" + "\n\n".join(paras) + "\n"
    open(a.saida or a.arquivo, "w", encoding="utf-8").write(out)
    print(f"{a.saida or a.arquivo}: {len(paras)} parágrafos gravados")

if __name__ == "__main__":
    main()
