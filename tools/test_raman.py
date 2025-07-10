from fastmcp import FastMCP
import os
from dotenv import load_dotenv
from os import environ
load_dotenv()
import json
import requests
import pymongo
from server_instance import mcp

@mcp.tool()
def test_raman_tool(query: str) -> str:
    """When people are lookig for Employee insurance related information use this function to get the informaation. Pass then entire user question as parameter"""
    
    client = pymongo.MongoClient(os.getenv("MONGO_URI_ATLAS"))
    db = client["Agratas_raman_15_db"]
    collection = db["Agratas_raman_15_embedded_collection"]

    vector = requests.post(os.getenv("EMBED_API_URL") + "/embed",
                           json={"sentences": [query]}).json()["embeddings"][0]

    res = collection.aggregate([
        {
            '$vectorSearch': {
                "index": "Agratas_raman_15_vector_search_index",
                "path": "embedding",
                "queryVector": vector,
                "numCandidates": 20,
                "limit": 2,
            }
        }
    ])

    context = "\n".join(doc.get("text", "") for doc in res)
    return context