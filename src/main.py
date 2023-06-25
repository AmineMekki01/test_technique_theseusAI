from fastapi import FastAPI, Response
from pydantic import BaseModel
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor

from text_processor import create_chunks
from chatbot import create_embeddings, create_vector_store, chunks_similarity_research, get_answer

app = FastAPI()

class Query(BaseModel):
    question: str

# Using LRU cache to store the precomputed results of expensive functions
@lru_cache(maxsize=None)
def get_vector_store() -> object:
    """
    Get the vector store for the transcript.
    
    Returns:
    -------
    vector_store : object
    
    """
    global_text = ""
    with open("./../data/1_transcript.txt", "r", encoding="utf-8") as file:
        global_text = file.read()

    embeddings = create_embeddings()
    chunks = create_chunks(global_text, 500)
    vector_store = create_vector_store(chunks, embeddings)
    return vector_store

# Background task to initialize the vector store
executor = ThreadPoolExecutor(max_workers=1)
executor.submit(get_vector_store)

@app.get("/")
def home():
    return {"Message": "Hello World! :)"}

@app.get("/about")
def about():
    return {
        "Content": "This task, assigned by TheseusAI, involves developing FastAPI endpoints. These endpoints accept a query, then find the most suitable response from the top three chunks that are most similar to the query. Each of these chunks contains no more than 500 tokens, extracted from a text file."
    }

@app.post("/get_answer")
def get_answer_endpoint(query: Query) -> Response:
    """
    Get the answer to the query from the most similar chunks.

    Parameters:
    ----------
    query : Query
        The query to find the most similar chunks to.

    Returns:
    -------
    response : Response
        The HTTP response containing the answer.
    """
    vector_store = get_vector_store()
    query_similar_chunks = chunks_similarity_research(vector_store, query.question, 3)
    answer = get_answer(query.question, query_similar_chunks)
    return Response(content=answer, media_type="text/plain")
