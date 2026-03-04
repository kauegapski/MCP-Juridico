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
    mcp.run(
        transport="sse",
        host="0.0.0.0",
        port=8000
    )
