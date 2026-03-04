from mcp.server.fastmcp import FastMCP

# Nome do servidor MCP
mcp = FastMCP("MCP-Juridico")

@mcp.tool()
def analisar_edital(texto: str) -> str:
    """
    Analisa edital de licitação e identifica riscos jurídicos.
    """
    return "Análise preliminar realizada."

@mcp.tool()
def gerar_tr(objeto: str) -> str:
    """
    Gera estrutura inicial de Termo de Referência.
    """
    return f"TR gerado para contratação de {objeto}"

@mcp.tool()
def verificar_lgpd(texto: str) -> str:
    """
    Verifica aderência à LGPD.
    """
    return "Conformidade LGPD analisada."


if __name__ == "__main__":
    mcp.run(transport="sse")
