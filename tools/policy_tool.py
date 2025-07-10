from server_instance import mcp

@mcp.tool()
def policy_tool(query: str) -> str:
    """When people are looking for Health insurance Policy information use this function to get the information. Pass the entire query as parameter"""
    print("entered policy tool")
    return f"Hello {query}, policy for insurance {query} today!"