from fastmcp import FastMCP

# Create a server instance
mcp = FastMCP(name="MyAssistantServer")


    
from sentence_transformers import SentenceTransformer
import pymongo

def get_embeddings(sentences):
    data=[]
    model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
    embeddings = model.encode(sentences).tolist()
    print(embeddings)
    return embeddings


def query_results(query):

    uri="mongodb+srv://techadmin:9EJrwZtI7S2T3RIP@cluster0.vicyn1o.mongodb.net/?retryWrites=true&w=majority"
    #mongodb+srv://techadmin:9EJrwZtI7S2T3RIP@cluster0.vicyn1o.mongodb.net/?retryWrites=true&w=majority
    client = pymongo.MongoClient(uri)
    db = client.Agratas_pdf_final_db
    collection = db.Agratas_pdf_final_embedded_collection
    ATLAS_VECTOR_SEARCH_INDEX_NAME="Agratas_pdf_final_vector_search_index"
    EMBEDDING_FIELD_NAME="embedding"
   

    results = collection.aggregate([
    {
        '$vectorSearch': {
            "index": ATLAS_VECTOR_SEARCH_INDEX_NAME,
            "path": EMBEDDING_FIELD_NAME,
            "queryVector": get_embeddings(query),
            "numCandidates": 20,
            "limit": 2,
        }
    }
    ])
    return results

@mcp.tool
def get_policy(query: str) -> dict:
    """When people are lookig for policy related information use this function to get the informaation. Pass then entire user question as parameter

    Args:
        query (str): Question from the user.

    Returns:
        dict: status and result or error msg.
    """
    res=query_results(query)
    system_content = "Context:\n"
    for i in res:
        system_content=system_content+i["text"]+'\n'
    #report='anything'
    report=(system_content)
    return {"status": "success", "report": report}

@mcp.tool
def get_profile(query: str) -> dict:
    """When people are looking for profile related information, use this function to get the information. Pass the entire user question as the parameter.

    Args:
        query (str): Question from the user.

    Returns:
        dict: status and result or error message.
    """
    res=query_results(query)
    system_content = "Context:\n"
    for i in res:
        system_content=system_content+i["text"]+'\n'
    #report='anything'
    report=(system_content)
    return {"status": "success", "report": report}

	
	
if __name__ == "__main__":
    # mcp.run(transport="streamable-http", host="0.0.0.0", port=8005)
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8005)
