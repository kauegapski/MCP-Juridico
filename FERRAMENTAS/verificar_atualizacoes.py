#!/usr/bin/env python3
"""Verifica se as normas da base MCP-Juridico mudaram no Planalto.

Para cada arquivo .md cuja linha **URL:** aponta para planalto.gov.br, baixa a
página oficial, extrai somente a redação vigente (sem trechos riscados) e compara,
parágrafo por parágrafo (texto normalizado), com o texto da base.

Uso:  python3 FERRAMENTAS/verificar_atualizacoes.py [--json relatorio.json] [arquivo.md ...]
Saída: relatório em texto; código de saída 0 = nada mudou, 1 = há diferenças, 2 = falha de acesso.
Requer: beautifulsoup4 e html5lib (pip install beautifulsoup4 html5lib).
"""
import argparse, glob, json, os, re, sys, unicodedata, urllib.request
from bs4 import BeautifulSoup

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTAS = ["CONSTITUCIONAL", "PENAL", "CIVEL", "LEGISLACAO"]
UA = {"User-Agent": "Mozilla/5.0 (verificador MCP-Juridico)"}

def baixar(url):
    erros = []
    for u in (url.replace("https://", "http://"), url):
        try:
            with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=90) as r:
                raw = r.read()
            for enc in ("cp1252", "utf-8"):
                try:
                    txt = raw.decode(enc)
                    if "�" not in txt:
                        return txt
                except UnicodeDecodeError:
                    pass
            return raw.decode("cp1252", errors="replace")
        except Exception as e:
            erros.append(f"{u}: {e}")
    raise RuntimeError("; ".join(erros))

def paragrafos_oficiais(html):
    try:   # html5lib reproduz o navegador e tolera o HTML malformado do Planalto
        s = BeautifulSoup(html, "html5lib")
    except Exception:
        s = BeautifulSoup(html, "html.parser")
    for t in s(["script", "style", "head"]):
        t.decompose()
    for t in s.find_all(["strike", "s", "del"]):
        t.decompose()
    for t in s.find_all(style=re.compile(r"line-through", re.I)):
        t.decompose()
    out = []
    for p in s.find_all(["p", "h1", "h2", "h3", "h4", "div", "td"]):
        if p.find(["p", "div", "td", "table"]):
            continue
        txt = p.get_text(" ", strip=True)
        if txt:
            out.append(txt)
    return out

def norm(t):
    t = unicodedata.normalize("NFC", t)
    t = t.replace(" ", " ").replace("–", "-").replace("—", "-")
    t = re.sub(r"[“”„\"]", '"', t)
    t = re.sub(r"[‘’']", "'", t)
    t = t.replace("\u00ba", "o").replace("\u00b0", "o").replace("\u00aa", "a")  # 1º / 1 o (sobrescrito)
    t = re.sub(r"[*_`#>]", "", t)          # marcação markdown
    t = re.sub(r"\s+", "", t)               # ignora toda diferença de espaçamento
    return t.lower()

RUIDO = re.compile(r"^(presid[eê]ncia|secretaria|subchefia|casa civil|vig[eê]ncia|regulamento|mensagem de veto|"
                   r"este texto n[aã]o substitui|emendas constitucionais|o presidente da rep[uú]blica|a presidenta da rep[uú]blica|"
                   r"(lei|decreto|decreto-lei|lei complementar|emenda constitucional|constitui[cç][aã]o)\b.{0,40}\bde\s+\d{4}\s*\.?$)", re.I)

def relevante(p):
    t = re.sub(r"\s+", " ", p).strip()
    if RUIDO.search(t):
        return False
    if re.fullmatch(r"(\((revogad[oa]|vide)[^)]*\)\s*)+", t, re.I) or re.fullmatch(r"(\(?vide [^)]*\)?\s*)+", t, re.I) or re.fullmatch(r"(regulamento\s*)+|(vig[eê]ncia\s*(encerrada)?\s*)+", t, re.I):
        return False
    return len(norm(t)) > 25

def corpo_base(md):
    i = md.find("## Texto integral")
    return md[i:] if i >= 0 else md

def comparar(arq):
    md = open(arq, encoding="utf-8").read()
    m = re.search(r"^\*\*URL:\*\*\s*(\S+)", md, re.M)
    if not m or "planalto.gov.br" not in m.group(1):
        return None
    url = m.group(1)
    ofic = paragrafos_oficiais(baixar(url))
    base_txt = norm(corpo_base(md))
    novos = [p for p in ofic if relevante(p) and norm(p) not in base_txt]
    # leis alteradoras citadas na página oficial e ausentes da base
    ref = re.compile(r"(?:Lei|Lei Complementar|Medida Provisória|Decreto-Lei|Emenda Constitucional)\s+n[ºo°]\s*[\d.]+,?\s+de\s+\d{4}")
    leis_of = {norm(x) : x for p in ofic for x in ref.findall(p)}
    leis_novas = sorted({v for k, v in leis_of.items() if k not in base_txt})
    return {"arquivo": os.path.relpath(arq, RAIZ), "url": url,
            "trechos_novos_ou_alterados": novos, "leis_alteradoras_novas": leis_novas}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("arquivos", nargs="*")
    ap.add_argument("--json")
    a = ap.parse_args()
    arqs = a.arquivos or sorted(f for p in PASTAS for f in glob.glob(os.path.join(RAIZ, p, "*.md")))
    rel, falhas, mudou = [], [], False
    for f in arqs:
        try:
            r = comparar(f)
        except Exception as e:
            falhas.append({"arquivo": os.path.relpath(f, RAIZ), "erro": str(e)[:300]})
            print(f"[FALHA]  {os.path.relpath(f, RAIZ)}: {str(e)[:200]}")
            continue
        if r is None:
            continue
        rel.append(r)
        n, l = len(r["trechos_novos_ou_alterados"]), r["leis_alteradoras_novas"]
        if n or l:
            mudou = True
            print(f"[MUDOU]  {r['arquivo']}: {n} trecho(s) novo(s)/alterado(s); leis alteradoras novas: {', '.join(l) or '-'}")
            for p in r["trechos_novos_ou_alterados"][:15]:
                print("         + " + p[:220])
        else:
            print(f"[OK]     {r['arquivo']}")
    if a.json:
        json.dump({"resultados": rel, "falhas": falhas}, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    sys.exit(2 if falhas and not rel else (1 if mudou else 0))

if __name__ == "__main__":
    main()
