import os
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("MCP-Juridico")

@mcp.tool()
def analisar_edital(texto: str) -> str:
    return "Análise preliminar realizada."

@mcp.tool()
def gerar_tr(objeto: str) -> str:
    return f"TR gerado para contratação de {objeto}"

@mcp.tool()
def verificar_lgpd(texto: str) -> str:
    return "Conformidade LGPD analisada."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    mcp.run(transport="sse", port=port)
