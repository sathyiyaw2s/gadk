# main.py
import os
import importlib
from fastmcp import FastMCP
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP(name="DynamicMCP")
MODELFILES_DIR = "modelfile"

def validate_tool_access(user_id: str, tool_name: str) -> bool:
    try:
        print(tool_name,"-------s")
        client = MongoClient(os.getenv("MONGO_URI_DB"))
        db = client["global_config_db"]
        col = db["toolmap_configs"]
        print("userid coming inside the validate tool",user_id)
        doc = col.find_one({"user_id": user_id})
        print(doc and tool_name in doc.get("tools", []),"----sending---")
        return doc and tool_name in doc.get("tools", [])
    except Exception as e:
        print(f" Access validation failed: {e}")
        return False

def get_toolmap_from_db():
    print("Get tools amd going")
    client = MongoClient(os.getenv("MONGO_URI_DB"))
    db = client["global_config_db"]
    col = db["toolmap_configs"]
    toolmap = {}
    for doc in col.find():
        toolmap[doc["user_id"]] = doc["tools"]
    return toolmap

def load_and_register_tools():
    toolmap = get_toolmap_from_db()
    print(toolmap,"----tool map info")
    for user_id, tool_modules in toolmap.items():
        for mod_name in tool_modules:
            try:
                module_path = f"{MODELFILES_DIR}.{mod_name}"
                mod = importlib.import_module(module_path)
                for func in getattr(mod, "EXPORTS", []):
                    mcp.tool(func)
                print(f"[✔] Loaded: {module_path}")
            except Exception as e:
                print(f" Failed to load {mod_name}: {e}")

@mcp.tool()
def reload_tools():
    """Reload all tools from MongoDB + modelfiles."""
    print("-------sdsf")
    load_and_register_tools()
    print("----cam")
    return {"status": "success", "message": "Tools reloaded"}

if __name__ == "__main__":
    load_and_register_tools()
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8005)
