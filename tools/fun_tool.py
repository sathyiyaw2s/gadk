from server_instance import mcp

@mcp.tool()
def fun_related_tool(query: str) -> str:
    """When people are looking for fun item related information use this function to get the information. Pass the entire query as parameter"""
    print("entered fun tool")
    return f"Hello {query}, I hope you're funny {query} today!"