#!/usr/bin/env python3
"""Servidor MCP da base MCP-Juridico (somente leitura).

Expõe a base normativa deste repositório como ferramentas MCP, para uso por modelos de
linguagem (Claude Desktop, Claude Code ou outro cliente MCP). Não gera opinião jurídica:
devolve texto literal da base, com a indicação do arquivo, da natureza da fonte e da
data da última verificação, para que a resposta possa ser conferida.

Execução (transporte stdio):
    pip install -r requirements.txt
    python3 server.py

Configuração típica em um cliente MCP:
    {"mcpServers": {"mcp-juridico": {"command": "python3", "args": ["/caminho/MCP-Juridico/server.py"]}}}

As regras de uso (hierarquia das fontes, vedações, jurisprudência só a pedido) estão em
PROTOCOLO_DE_USO_MCP.md e são devolvidas pela ferramenta `protocolo_de_uso`.
"""
import os
import re
import unicodedata
from functools import lru_cache

try:                                   # SDK mcp 2.x
    from mcp.server.mcpserver import MCPServer as _Servidor
except ImportError:                    # SDK mcp 1.x
    from mcp.server.fastmcp import FastMCP as _Servidor

RAIZ = os.path.dirname(os.path.abspath(__file__))
IGNORAR_PASTAS = {".git", "FERRAMENTAS", "__pycache__", ".github"}
LIMITE_LEITURA = 30000          # caracteres por chamada de ler_documento

mcp = _Servidor(
    "MCP-Juridico",
    instructions=(
        "Base normativa de licitações, contratos, TI/LGPD e legislação geral, com foco no Poder "
        "Legislativo de Guarapuava/PR. Antes de fundamentar, consulte `protocolo_de_uso`. "
        "Cite apenas dispositivos devolvidos pelas ferramentas, transcrevendo-os. Fontes com "
        "natureza 'orientacao' não são norma; 'norma_referencia' (INs/Portarias federais) não "
        "vincula a Câmara salvo adoção expressa (art. 187 da Lei nº 14.133/2021); 'jurisprudencia' "
        "só pode ser usada a pedido expresso do usuário; situacao 'historico' indica material superado."
    ),
)


# --------------------------------------------------------------------------- utilidades
def _sem_acento(t: str) -> str:
    t = unicodedata.normalize("NFKD", t)
    return "".join(c for c in t if not unicodedata.combining(c)).lower()


_TABELA = {}


def _plano(texto: str) -> str:
    """Minúsculas sem acento, preservando o comprimento (1 caractere -> 1 caractere),
    para que as posições encontradas na busca valham também no texto original."""
    for c in set(texto):
        if ord(c) > 127 and ord(c) not in _TABELA:
            r = _sem_acento(c)
            _TABELA[ord(c)] = r[0] if len(r) >= 1 else c
    return texto.translate(_TABELA).lower()


def _separar(md: str):
    """Devolve (metadados: dict, corpo: str) a partir do cabeçalho YAML simples."""
    meta = {}
    if md.startswith("---\n"):
        fim = md.find("\n---\n", 4)
        if fim > 0:
            for linha in md[4:fim].splitlines():
                if ": " in linha:
                    k, v = linha.split(": ", 1)
                    v = v.strip()
                    if v.startswith("[") and v.endswith("]"):
                        v = [x.strip() for x in v[1:-1].split(",") if x.strip()]
                    elif v.startswith('"') and v.endswith('"'):
                        v = v[1:-1].replace('\\"', '"').replace("\\\\", "\\")
                    elif v == "null":
                        v = None
                    meta[k] = v
            return meta, md[fim + 5:]
    return meta, md


@lru_cache(maxsize=1)
def _catalogo():
    """Lista de documentos: [{arquivo, pasta, metadados..., corpo}] (lida uma vez)."""
    docs = []
    for dirpath, dirnames, filenames in os.walk(RAIZ):
        dirnames[:] = sorted(d for d in dirnames if d not in IGNORAR_PASTAS and not d.startswith("."))
        for f in sorted(filenames):
            if not f.endswith(".md"):
                continue
            caminho = os.path.join(dirpath, f)
            rel = os.path.relpath(caminho, RAIZ).replace(os.sep, "/")
            md = open(caminho, encoding="utf-8").read()
            meta, corpo = _separar(md)
            if not meta:   # README, INDEX, PROTOCOLO, LICENSE
                meta = {"titulo": rel, "natureza": "documento_da_base", "tipo": "documento_da_base"}
            docs.append({"arquivo": rel, "pasta": os.path.dirname(rel) or ".", **meta,
                         "corpo": corpo, "_busca": _sem_acento(rel + " " + str(meta.get("titulo", "")))})
    return docs


def _resumo(d: dict) -> str:
    sit = f" | situação: {d.get('situacao')}" if d.get("situacao") == "historico" else ""
    return (f"- {d['arquivo']}\n  título: {d.get('titulo')}\n  natureza: {d.get('natureza')} | "
            f"tipo: {d.get('tipo')} | esfera: {d.get('esfera', '-')}{sit} | última verificação: "
            f"{d.get('ultima_verificacao') or '-'}")


def _cabecalho(d: dict) -> str:
    linhas = [f"[Fonte: {d['arquivo']}]", f"[Título: {d.get('titulo')}]",
              f"[Natureza: {d.get('natureza')}; tipo: {d.get('tipo')}; esfera: {d.get('esfera', '-')}; "
              f"situação: {d.get('situacao', '-')}]",
              f"[Fonte oficial: {d.get('fonte') or '-'} {d.get('fonte_url') or ''}]".rstrip(),
              f"[Última verificação: {d.get('ultima_verificacao') or '-'}]"]
    if d.get("natureza") == "orientacao":
        linhas.append("[ATENÇÃO: material orientativo — não é norma jurídica.]")
    if d.get("natureza") == "norma_referencia":
        linhas.append("[ATENÇÃO: ato federal de referência — não vincula a Câmara salvo adoção expressa "
                      "ou execução de recursos federais que o exijam (art. 187 da Lei nº 14.133/2021).]")
    if d.get("natureza") == "jurisprudencia":
        linhas.append("[ATENÇÃO: jurisprudência — usar somente a pedido expresso do usuário.]")
    if d.get("situacao") == "historico":
        linhas.append("[ATENÇÃO: material histórico — baseado em normas revogadas.]")
    return "\n".join(linhas)


# Apelidos comuns -> trecho do caminho do arquivo
APELIDOS = {
    "lgpd": "Lei_13709", "lai": "Lei_12527", "cf": "Constituicao_Federal", "constituicao": "Constituicao_Federal",
    "nova lei de licitacoes": "Lei_14133", "lei de licitacoes": "Lei_14133", "14133": "Lei_14133",
    "14.133": "Lei_14133", "cdc": "Lei_8078", "cc": "Codigo_Civil", "codigo civil": "Codigo_Civil",
    "cpc": "Codigo_Processo_Civil", "cp": "Codigo_Penal", "codigo penal": "Codigo_Penal",
    "cpp": "Codigo_Processo_Penal", "eca": "Lei_8069", "ctb": "Lei_9503", "lom": "Lei_Organica",
    "lei organica": "Lei_Organica", "regimento interno": "Regimento_Interno", "ri": "Regimento_Interno",
    "estatuto me epp": "LC_123", "lc 123": "LC_123", "4320": "Lei_4320", "4.320": "Lei_4320",
    "valores": "Decreto_12807", "12807": "Decreto_12807", "12.807": "Decreto_12807",
}


def _localizar(norma: str):
    """Resolve 'norma' (caminho, apelido ou palavras do título) em uma lista de documentos."""
    docs = _catalogo()
    q = norma.strip().replace("\\", "/")
    exato = [d for d in docs if d["arquivo"] == q or d["arquivo"].endswith("/" + q)]
    if exato:
        return exato
    qn = _sem_acento(q)
    qn = re.sub(r"\b(lei|decreto|municipal|federal|n[oº°]|de)\b\.?", " ", qn) if re.search(r"\d", qn) else qn
    if _sem_acento(q) in APELIDOS:
        alvo = APELIDOS[_sem_acento(q)]
        return [d for d in docs if os.path.basename(d["arquivo"]).startswith(alvo)]
    tokens = [t for t in re.split(r"[\s/_.,º°-]+", qn) if t]
    if not tokens:
        return []
    achados = [d for d in docs if all(t in d["_busca"] for t in tokens)]
    # números: "37/2022" -> exige "37" e "2022" como trechos do caminho, evitando "370" para "37"
    nums = re.findall(r"\d+", q)
    if nums:
        achados = [d for d in achados if all(re.search(rf"(?<!\d){n}(?!\d)", d["arquivo"]) for n in nums)]
    return achados


RX_ART = re.compile(r"^\s*(?:\*\*)?\s*Art\.?\s*(\d{1,3}(?:\.\d{3})*|\d+)\s*(?:[º°o]|\.)?\s*(?:-\s*([A-Z]))?\b", re.M)
RX_TITULO_ESTRUTURA = re.compile(r"^\s*(?:#+\s*)?(?:\*\*)?\s*(T[ÍI]TULO|CAP[ÍI]TULO|Se[çc][ãa]o|SE[ÇC][ÃA]O|Subse[çc][ãa]o|LIVRO|PARTE)\b")


def _artigos(corpo: str, numero: str):
    m = re.match(r"\s*(?:art\.?\s*)?(\d[\d.]*)\s*[º°o]?\s*(?:-\s*([A-Za-z]))?\s*$", numero, re.I)
    if not m:
        return None
    num, letra = m.group(1).replace(".", ""), (m.group(2) or "").upper()
    marcas = list(RX_ART.finditer(corpo))
    chave = lambda mk: (mk.group(1).replace(".", ""), mk.group(2) or "")
    trechos = []
    for i, mk in enumerate(marcas):
        if chave(mk) == (num, letra):
            fim = len(corpo)
            for prox in marcas[i + 1:]:
                if chave(prox) != (num, letra):
                    fim = prox.start()
                    break
            bloco = corpo[mk.start():fim].rstrip().splitlines()
            # remove títulos de capítulo/seção que antecedem o artigo seguinte
            # (ex.: "CAPÍTULO IX" + "DAS ALIENAÇÕES"; "Seção III" + "Da Dispensa")
            while True:
                while bloco and (not bloco[-1].strip() or bloco[-1].strip() == "---"):
                    bloco.pop()
                ult = [j for j in range(len(bloco)) if bloco[j].strip()][-4:]
                corte = next((j for j in ult if RX_TITULO_ESTRUTURA.match(bloco[j])), None)
                if corte is None or corte == 0:
                    break
                bloco = bloco[:corte]
            trechos.append("\n".join(bloco))
    return trechos


# --------------------------------------------------------------------------- ferramentas
@mcp.tool()
def listar_documentos(pasta: str = "", natureza: str = "", area: str = "", termo_no_titulo: str = "") -> str:
    """Lista os documentos da base com seus metadados.

    Filtros opcionais (combináveis):
      pasta: ex. "LEGISLACAO", "DECRETOS/MUNICIPAIS_GUARAPUAVA", "MANUAIS_E_GUIAS", "TI_E_SEGURANCA"
      natureza: norma_vinculante | norma_referencia | orientacao | jurisprudencia | tabela | modelo
      area: licitacoes | ti | lgpd | transparencia | financas_publicas | administracao_camara | ...
      termo_no_titulo: palavra que deve constar do título ou do nome do arquivo
    """
    docs = _catalogo()
    if pasta:
        docs = [d for d in docs if d["pasta"].lower().startswith(pasta.strip("/").lower())]
    if natureza:
        docs = [d for d in docs if d.get("natureza") == natureza]
    if area:
        docs = [d for d in docs if area in (d.get("area") or [])]
    if termo_no_titulo:
        t = _sem_acento(termo_no_titulo)
        docs = [d for d in docs if t in d["_busca"]]
    if not docs:
        return "Nenhum documento encontrado com esses filtros."
    return f"{len(docs)} documento(s):\n" + "\n".join(_resumo(d) for d in docs)


@mcp.tool()
def buscar_artigo(norma: str, artigo: str) -> str:
    """Devolve o texto literal de um artigo (caput, parágrafos, incisos e alíneas).

    norma: caminho do arquivo (ex. "LEGISLACAO/Lei_14133_2021.md"), apelido ("LGPD", "14133", "CF",
           "LOM", "Regimento Interno", "LAI") ou palavras do título ("Decreto 37/2022").
    artigo: número do artigo, ex. "75", "75-A", "art. 6º".
    Se a norma tiver mais de uma ocorrência do número (ex.: CF e ADCT, ato com anexo), todas são devolvidas.
    """
    docs = _localizar(norma)
    if not docs:
        return f"Norma '{norma}' não localizada. Use listar_documentos para ver os arquivos disponíveis."
    if len(docs) > 1:
        normas = [d for d in docs if d.get("natureza") in ("norma_vinculante", "norma_referencia")]
        docs = normas if len(normas) == 1 else docs
    if len(docs) > 1:
        return "Mais de uma norma corresponde à consulta; especifique o arquivo:\n" + "\n".join(_resumo(d) for d in docs)
    d = docs[0]
    trechos = _artigos(d["corpo"], artigo)
    if trechos is None:
        return f"Número de artigo inválido: '{artigo}'."
    if not trechos:
        return f"{_cabecalho(d)}\n\nArtigo {artigo} não encontrado neste arquivo (verifique a numeração ou use buscar_texto)."
    partes = [f"--- ocorrência {i} de {len(trechos)} ---\n{t}" if len(trechos) > 1 else t for i, t in enumerate(trechos, 1)]
    return _cabecalho(d) + "\n\n" + "\n\n".join(partes)


@mcp.tool()
def buscar_texto(termo: str, pasta: str = "", natureza: str = "", limite: int = 20) -> str:
    """Busca um termo ou expressão (sem distinção de maiúsculas e acentos) em toda a base.

    Devolve trechos com o arquivo e o artigo em que o termo aparece.
    termo: palavra, expressão literal ou expressão regular simples (ex. "dispensa eletr", "art\\. 75")
    pasta / natureza: filtros opcionais, como em listar_documentos.
    limite: número máximo de trechos (padrão 20, máximo 100).
    """
    limite = max(1, min(int(limite), 100))
    try:
        rx = re.compile(_sem_acento(termo))
    except re.error:
        rx = re.compile(re.escape(_sem_acento(termo)))
    saida, total = [], 0
    for d in _catalogo():
        if pasta and not d["pasta"].lower().startswith(pasta.strip("/").lower()):
            continue
        if natureza and d.get("natureza") != natureza:
            continue
        corpo = d["corpo"]
        if "_plano" not in d:
            d["_plano"] = _plano(corpo)
        plano = d["_plano"]
        marcas = [(m.start(), m.group(1) + ("-" + m.group(2) if m.group(2) else "")) for m in RX_ART.finditer(corpo)]
        for m in rx.finditer(plano):
            total += 1
            if len(saida) >= limite:
                continue
            art = next((a for p, a in reversed(marcas) if p <= m.start()), None)
            ini, fim = max(0, m.start() - 220), min(len(corpo), m.end() + 220)
            trecho = " ".join(corpo[ini:fim].split())
            saida.append(f"- {d['arquivo']} ({d.get('natureza')})" + (f" — art. {art}" if art else "") +
                         f"\n  …{trecho}…")
    if not saida:
        return f"Nenhuma ocorrência de '{termo}'."
    extra = f" (exibindo {len(saida)}; refine a busca ou aumente o limite)" if total > len(saida) else ""
    return f"{total} ocorrência(s) de '{termo}'{extra}:\n" + "\n".join(saida)


@mcp.tool()
def ler_documento(arquivo: str, inicio: int = 0, max_caracteres: int = LIMITE_LEITURA) -> str:
    """Lê um documento da base (com cabeçalho de procedência), em blocos.

    arquivo: caminho ou apelido (como em buscar_artigo).
    inicio: posição (em caracteres) a partir da qual ler — use o valor indicado em 'próximo bloco'.
    max_caracteres: tamanho do bloco (padrão e máximo 30000).
    """
    docs = _localizar(arquivo)
    if len(docs) != 1:
        return ("Documento não localizado." if not docs else
                "Mais de um documento corresponde; especifique:\n" + "\n".join(_resumo(d) for d in docs))
    d = docs[0]
    n = max(1000, min(int(max_caracteres), LIMITE_LEITURA))
    ini = max(0, int(inicio))
    corpo = d["corpo"]
    bloco = corpo[ini:ini + n]
    rodape = (f"\n\n[próximo bloco: inicio={ini + n} de {len(corpo)} caracteres]" if ini + n < len(corpo)
              else f"\n\n[fim do documento — {len(corpo)} caracteres]")
    return _cabecalho(d) + "\n\n" + bloco + rodape


@mcp.tool()
def protocolo_de_uso() -> str:
    """Devolve o PROTOCOLO_DE_USO_MCP.md: hierarquia das fontes, regras de uso, vedações e
    tratamento de jurisprudência. Deve ser consultado antes de fundamentar qualquer resposta."""
    return open(os.path.join(RAIZ, "PROTOCOLO_DE_USO_MCP.md"), encoding="utf-8").read()


@mcp.tool()
def mapa_decretos_municipais() -> str:
    """Indica qual Decreto do Poder Legislativo de Guarapuava (2022) regulamenta cada tema da
    Lei nº 14.133/2021, com o arquivo correspondente na base."""
    return """Decretos do Poder Legislativo de Guarapuava que regulamentam a Lei nº 14.133/2021
(regulamentos de execução: não podem contrariar a lei; ver PROTOCOLO_DE_USO_MCP.md)

| Tema | Decreto | Arquivo |
|---|---|---|
| Governança, PCA, fase preparatória, DFD, ETP (arts. 11 e 12), padronização, artigos de luxo, gestão e fiscalização de contratos, IMR e recebimento | nº 37/2022 | DECRETOS/MUNICIPAIS_GUARAPUAVA/Decreto_37_2022_Governanca.md |
| Pesquisa de preços e estimativa de custos | nº 38/2022 | DECRETOS/MUNICIPAIS_GUARAPUAVA/Decreto_38_2022_Pesquisa_Precos.md |
| Termo de Referência (elaboração pelo Diretor de Gestão Administrativa — art. 1º, § 1º) | nº 39/2022 | DECRETOS/MUNICIPAIS_GUARAPUAVA/Decreto_39_2022_Termo_Referencia.md |
| Compra direta de pequena monta / pronto pagamento (art. 95, § 2º, da Lei nº 14.133/2021) | nº 40/2022 | DECRETOS/MUNICIPAIS_GUARAPUAVA/Decreto_40_2022_Compra_Direta.md |
| Dispensa de licitação na forma eletrônica, inclusive dispensa por valor (art. 75) | nº 41/2022 | DECRETOS/MUNICIPAIS_GUARAPUAVA/Decreto_41_2022_Dispensa_Eletronica.md |

Observações:
- O ETP é regulamentado pelo Decreto nº 37/2022 (não pelo nº 39/2022, que trata só do TR).
- A dispensa por valor segue o Decreto nº 41/2022; o nº 40/2022 trata apenas da compra direta de pequena monta.
- Valores vigentes dos limites da Lei nº 14.133/2021: use a ferramenta valores_vigentes_lei_14133."""


@mcp.tool()
def valores_vigentes_lei_14133() -> str:
    """Devolve os valores atualizados da Lei nº 14.133/2021 vigentes na base (decreto federal de
    atualização anual — art. 182 da Lei), com a tabela do Anexo por dispositivo."""
    docs = [d for d in _catalogo() if d["arquivo"].startswith("LEGISLACAO/Decreto_") and "Atualizacao_Valores" in d["arquivo"]]
    if not docs:
        return "Decreto de atualização de valores não encontrado na base."
    d = sorted(docs, key=lambda x: x["arquivo"])[-1]
    corpo = d["corpo"]
    i = corpo.find("## Texto integral")
    return _cabecalho(d) + "\n\n" + (corpo[i:] if i >= 0 else corpo)


if __name__ == "__main__":
    mcp.run()
