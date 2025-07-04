
import pymongo
import os
import requests
import json
from dotenv import load_dotenv
from main import validate_tool_access

load_dotenv()

TOOL_NAME = "raman_17_id_agratas_raman_17"
    
def raman_17_id_agratas_raman_17(inputs:dict) -> dict:
    """When people are looking for international policy related information use this function to get the informaation. Pass then entire user question as parameter"""
    if isinstance(inputs, str):
        try:
            inputs = json.loads(inputs)
        except json.JSONDecodeError:
            return {"status": "error", "message": "Invalid input format"}
        
    query = inputs["query"]
    user_id = inputs["user_id"]
    
    if not validate_tool_access(user_id, TOOL_NAME):
        return {"status": "error", "message": "Unauthorized access"}
    client = pymongo.MongoClient(os.getenv("MONGO_URI_ATLAS"))
    db = client["Agratas_raman_17_db"]
    collection = db["Agratas_raman_17_embedded_collection"]

    vector = requests.post(os.getenv("EMBED_API_URL") + "/embed",
                           json={"sentences": [query]}).json()["embeddings"][0]

    res = collection.aggregate([
        {
            '$vectorSearch': {
                "index": "Agratas_raman_17_vector_search_index",
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
        "text": f"Here is what I found:\n{context}" 
    }

EXPORTS = [raman_17_id_agratas_raman_17]