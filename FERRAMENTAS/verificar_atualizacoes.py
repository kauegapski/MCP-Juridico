#!/usr/bin/env python3
"""Verifica se as normas da base MCP-Juridico mudaram na fonte oficial.

Para cada arquivo .md cuja linha **URL:** aponta para uma fonte suportada, baixa a
página oficial, extrai somente a redação vigente (sem trechos riscados) e compara,
parágrafo por parágrafo (texto normalizado), com o texto da base.

Fontes suportadas (área de conteúdo extraída):
  planalto.gov.br  -> página inteira (leis, decretos, códigos)
  www.gov.br       -> #parent-fieldname-text (INs SEGES/SGD, Portarias SGD, páginas de órgãos)
  www.in.gov.br    -> .texto-dou (Diário Oficial da União: resoluções da ANPD etc.)
Não suportadas (conferência manual ou pelo navegador): sítio da Câmara de Guarapuava
(sistemalegislativo, protegido por captcha), Boletim Oficial do Município e Diário
Eletrônico do TCE-PR (PDF). Fichas orientativas (MANUAIS_E_GUIAS) não são verificadas.

Uso:  python3 FERRAMENTAS/verificar_atualizacoes.py [--json relatorio.json] [--marcar] [arquivo.md ...]
      --marcar  grava a data de hoje em "**Última verificação:**" e no campo ultima_verificacao
                do cabeçalho YAML dos arquivos conferidos SEM divergência (os divergentes não mudam)
Saída: relatório em texto; código de saída 0 = nada mudou, 1 = há diferenças, 2 = falha de acesso.
Requer: beautifulsoup4 e html5lib (pip install beautifulsoup4 html5lib).
"""
import argparse, glob, json, os, re, sys, unicodedata, urllib.request
from bs4 import BeautifulSoup

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTAS = ["CONSTITUCIONAL", "PENAL", "CIVEL", "LEGISLACAO", "TI_E_SEGURANCA"]
SUPORTADAS = ("planalto.gov.br", "www.gov.br", "www.in.gov.br")
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36 (verificador MCP-Juridico)",
      "Accept": "text/html,application/xhtml+xml",          # sem Accept o in.gov.br responde 403
      "Accept-Language": "pt-BR,pt;q=0.9"}

def baixar(url):
    erros = []
    for u in (url.replace("https://", "http://"), url):
        try:
            with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=90) as r:
                raw = r.read()
            if raw[:2] in (b"\xff\xfe", b"\xfe\xff"):          # algumas páginas do Planalto vêm em UTF-16
                return raw.decode("utf-16", errors="replace")
            for enc in ("utf-8", "cp1252"):   # utf-8 estrito primeiro: bytes cp1252 o invalidam
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

def area_conteudo(s, url):
    """Recorta a área do texto normativo conforme o portal de origem."""
    if "www.in.gov.br" in url:
        return s.select_one(".texto-dou") or s
    if "www.gov.br" in url:
        return s.select_one("#parent-fieldname-text") or s.select_one("#content-core") or s
    return s

def paragrafos_oficiais(html, url=""):
    try:   # html5lib reproduz o navegador e tolera o HTML malformado do Planalto
        s = BeautifulSoup(html, "html5lib")
    except Exception:
        s = BeautifulSoup(html, "html.parser")
    s = area_conteudo(s, url)
    for t in s(["script", "style", "head"]):
        t.decompose()
    for t in s.find_all(["strike", "s", "del"]):
        t.decompose()
    for t in s.find_all(style=re.compile(r"line-through", re.I)):
        t.decompose()
    for br in s.find_all("br"):
        br.replace_with(" ")
    out = []
    for p in s.find_all(["p", "h1", "h2", "h3", "h4", "div", "td"]):
        if p.find(["p", "div", "td", "table"]):
            continue
        # junta os nós de texto sem separador: o Planalto às vezes fatia palavras
        # em <span> letra a letra (ex.: LC 123/2006), e o separador " " as quebrava
        txt = " ".join(p.get_text("").split())
        if txt:
            out.append(txt)
    return out

def norm(t):
    t = unicodedata.normalize("NFC", t)
    t = t.replace(" ", " ").replace("–", "-").replace("—", "-")
    t = re.sub(r"[“”„\"]", '"', t)
    t = re.sub(r"[‘’']", "'", t)
    # ordinais: "1º", "1 o" (sobrescrito do Planalto) e "1" (gov.br às vezes omite) se equivalem
    t = re.sub(r"(\d)\s*[º°o](?![a-zà-ú])", r"\1", t)
    t = re.sub(r"(\d)\s*ª", r"\1", t)
    t = re.sub(r"\b([Nn])\s*[º°o]?\s*(?=\d)", r"\1", t)   # "nº 94", "n o 94", "n 94"
    t = t.replace("\u00ba", "o").replace("\u00b0", "o").replace("\u00aa", "a")
    t = re.sub(r"[*_`#>]", "", t)          # marcação markdown
    t = t.replace("-", "")                  # travessões/hífens de títulos ("CAPÍTULO I — ...")
    t = re.sub(r"\s+", "", t)               # ignora toda diferença de espaçamento
    return t.lower()

RUIDO = re.compile(r"^(presid[eê]ncia|secretaria|subchefia|casa civil|vig[eê]ncia|regulamento|mensagem de veto|"
                   r"este (texto|conte[uú]do) n[aã]o substitui|emendas constitucionais|o presidente da rep[uú]blica|a presidenta da rep[uú]blica|"
                   r"(lei|decreto|decreto-lei|lei complementar|emenda constitucional|constitui[cç][aã]o|instru[cç][aã]o normativa|portaria|resolu[cç][aã]o)\b.{0,60}\bde\s+\d{4}\s*\.?$)", re.I)

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
    if not m or not any(d in m.group(1) for d in SUPORTADAS):
        return None
    if re.search(r"^natureza:\s*orientacao\s*$", md, re.M):   # fichas orientativas não têm texto a comparar
        return None
    url = m.group(1)
    ofic = paragrafos_oficiais(baixar(url), url)
    if len(ofic) < 3:
        raise RuntimeError("área de texto não localizada na página (layout do portal mudou?)")
    base_txt = norm(md)   # inclui o cabeçalho, onde ficam ementa e dados de publicação
    novos = [p for p in ofic if relevante(p) and norm(p) not in base_txt]
    # leis alteradoras citadas na página oficial e ausentes da base
    ref = re.compile(r"(?:Lei|Lei Complementar|Medida Provisória|Decreto-Lei|Emenda Constitucional)\s+n[ºo°]\s*[\d.]+,?\s+de\s+\d{4}")
    leis_of = {norm(x) : x for p in ofic for x in ref.findall(p)}
    leis_novas = sorted({v for k, v in leis_of.items() if k not in base_txt})
    return {"arquivo": os.path.relpath(arq, RAIZ), "url": url,
            "trechos_novos_ou_alterados": novos, "leis_alteradoras_novas": leis_novas}

def marcar(arq):
    """Registra no arquivo a conferência sem divergências feita hoje."""
    hoje = __import__("datetime").date.today().isoformat()
    md = open(arq, encoding="utf-8").read()
    md = re.sub(r"^\*\*Última verificação:\*\*.*$",
                f"**Última verificação:** {hoje} (redação conferida sem divergências com a fonte oficial — FERRAMENTAS/verificar_atualizacoes.py)  ",
                md, count=1, flags=re.M)
    md = re.sub(r"^ultima_verificacao:.*$", f"ultima_verificacao: {hoje}", md, count=1, flags=re.M)
    open(arq, "w", encoding="utf-8").write(md)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("arquivos", nargs="*")
    ap.add_argument("--json")
    ap.add_argument("--marcar", action="store_true")
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
            if a.marcar:
                marcar(f)
    if a.json:
        json.dump({"resultados": rel, "falhas": falhas}, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    sys.exit(2 if falhas and not rel else (1 if mudou else 0))

if __name__ == "__main__":
    main()
