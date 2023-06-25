from fastapi import FastAPI, Request, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor

from text_processor import create_chunks
from chatbot import create_embeddings, create_vector_store, chunks_similarity_research, get_answer

app = FastAPI()
app.mount("/static", StaticFiles(directory="./static"), name="static")

# Instantiate the jinja2 class
templates = Jinja2Templates(directory="./templates")

class Query(BaseModel):
    question: str

# Using LRU cache to store the precomputed results of expensive functions
@lru_cache(maxsize=None)
def get_vector_store(text: str) -> object:
    """
    Get the vector store for the text.

    Parameters:
    ----------
    text : str
        The text content to create the vector store from.

    Returns:
    -------
    vector_store : object
    """
    embeddings = create_embeddings()
    chunks = create_chunks(text, 500)
    vector_store = create_vector_store(chunks, embeddings)
    return vector_store

# Background task to initialize the vector store
executor = ThreadPoolExecutor(max_workers=1)
vector_store = None  # Variable to store the vector store

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/about")
def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/query")
async def query(request: Request):
    return templates.TemplateResponse("query.html", {"request": request})

@app.post("/upload_file")
async def upload_file(file: UploadFile = File(...)):
    global vector_store  # Use the global variable
    contents = await file.read()
    text = contents.decode("utf-8")  # Convert bytes to string
    vector_store = get_vector_store(text)  # Update the vector store with the text
    return {"filename": file.filename}

@app.post("/get_answer")
def get_answer_endpoint(query: Query):
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
    query_similar_chunks = chunks_similarity_research(vector_store, query.question, 3)
    answer = get_answer(query.question, query_similar_chunks)
    return {"answer": answer}
