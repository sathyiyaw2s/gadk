from server_instance import mcp

@mcp.tool()
def food_related_tool(query: str) -> str:
    """When people are looking for food related information use this function to get the information. Pass the entire query as parameter"""
    print("entered food tool")
    return f"Hello {query}, I hope you're foody {query} today!"