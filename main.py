import os
import importlib
import asyncio
from server_instance import mcp

TOOLS_DIR = "tools"

def dynamic_import_tools():
    for filename in os.listdir(TOOLS_DIR):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = filename[:-3]
            import_path = f"{TOOLS_DIR}.{module_name}"
            try:
                importlib.import_module(import_path)
                print(f"Loaded tools from: {import_path}")
            except Exception as e:
                print(f"Failed to import {import_path}: {e}")

async def main():
    dynamic_import_tools()

    tool_names = await mcp.get_tools()
    print("\n Registered MCP Tools:")
    for name in tool_names:
        tool = await mcp.get_tool(name)
        print(f"- Name: {tool.name}")
        print(f"  Description: {tool.description}\n")

    await mcp.run_async(transport="streamable-http", host="127.0.0.1", port=8005)

if __name__ == "__main__":
    asyncio.run(main())
