from server_instance import mcp

@mcp.tool()
def weather_tool(query: str) -> str:
    """When people are looking for any weather related information use this function to get the information. Pass the entire query as parameter"""
    print("entered weather tool")
    return f"Hello {query}, policy for weaathery {query} today!"