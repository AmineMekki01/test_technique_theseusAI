from fastapi import FastAPI, Request, UploadFile, HTTPException, Depends, File

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

class VectorStore:
    def __init__(self):
        self.store = None

vector_store = VectorStore()


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

@app.get("/")
def home(request: Request):
    
    """
    The home page of the web app.
    
    Parameters:
    ----------
    
    request : Request
        The request object.
    
    Returns:
    -------
    response : Response
    
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/about")
def about(request: Request):
    
    """
    The about page of the web app.
    
    Parameters:
    ----------
    
    request : Request
        The request object.
    
    Returns:
    -------
    response : Response
    
    """
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/query")
async def query(request: Request):
    """
    The query page of the web app.

    Parameters:
    ----------
    request : Request
        The request object.

    Returns:
    -------
    response : Response
    
    """
    return templates.TemplateResponse("query.html", {"request": request})

@app.post("/upload_file")
async def upload_file(file: UploadFile = File(...)) -> dict[str, str]:
    """
    Upload the file and create the vector store from it.
    
    Parameters:
    ----------
    file : UploadFile  
        The file that will uploaded from the web to create the vector store from.

    Returns:
    -------
    response : Response
        The response containing the filename.
        
    """
    contents = await file.read()
    text = contents.decode("utf-8")
    vector_store.store = get_vector_store(text)
    return {"filename": file.filename}


@app.post("/get_answer")
def get_answer_endpoint(query: Query) -> dict[str, str]:
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
    if vector_store.store is None:
        raise HTTPException(status_code=400, detail="No file uploaded yet")
    query_similar_chunks = chunks_similarity_research(vector_store.store, query.question, 3)
    answer = get_answer(query.question, query_similar_chunks)
    return {"answer": answer}
