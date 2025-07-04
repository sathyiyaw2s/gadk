
import pymongo
import os
import requests
import json
from dotenv import load_dotenv
from main import validate_tool_access
# from typing_extensions import TypedDict


load_dotenv()

TOOL_NAME = "raman_15_id_agratas_raman_15"

# class InputArgs(TypedDict):
#     query: str
#     user_id: str
    
def raman_15_id_agratas_raman_15(inputs: dict) -> dict:
    """When people are lookig for Employee insurance related information use this function to get the informaation. Pass then entire user question as parameter"""
    if isinstance(inputs, str):
        try:
            inputs = json.loads(inputs)
        except json.JSONDecodeError:
            return {"status": "error", "message": "Invalid input format"}
        
    query = inputs["query"]
    user_id = inputs["user_id"]
    print("userid coming inside the validate tool", user_id)
    
    if not validate_tool_access(user_id, TOOL_NAME):
        print("-----uesrid",user_id)
        return {"status": "error", "message": "Unauthorized access"}
    
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
    return {
        "status": "success",
        "report": context,
        "text": f"Here is what I found:\n{context}"  # ← REQUIRED for Gemini
    }

EXPORTS = [raman_15_id_agratas_raman_15]