import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

# import from local modules 
from .utils import get_api_key, setup_openai_api


def create_embeddings(model_name : str = "text-embedding-ada-002") -> object:
    
  """
    Create an embedding model from a model name.

    Parameters:
    ----------
    model_name : str
        The name of the model that will be used for creating vectors

    Returns :
    -------
    embeddings 
        Object containing all necessary information about how 
        we can use this particular type of embedding in our system
  """
  
  setup_openai_api()
  return OpenAIEmbeddings(
  document_model_name = model_name,
  query_model_name = model_name,
  openai_api_key= get_api_key()
  )
  
def create_vectore_store(chunks : list[str], embeddings : object) -> object:
    
    """
        Create a vector store from a list of chunks and an embedding model using FAISS.
    
        Parameters:
        ----------
        
        chunks : list[str]
            A list of chunks to create the vector store from.
            
        embeddings : object
            An embedding model to create the vector store from.
            
        Returns:
        -------
        vectorStore
            Object containing all necessary information about the vector store.
    """
        
    return FAISS.from_texts(chunks, embeddings)    



def chunks_similarity_research(vectorStore : object, query : str, chunks_number : int = 3):
    
  """
    Find the most similar chunks to the query.
    
    Parameters:
    ----------
    vectorStore : object
        The created vector store with all chunk vectors in it.
    
    query : str
        The query to find the most similar chunks to.
    
    chunks_number : int
        The number of chunks to return.
        
    Returns:
    -------
    chunks : list[object] 
        The most similar chunks to the query. A list of objects that have all informations about the chunks including their content.
  """
  
  return vectorStore.similarity_search(query, k=chunks_number)  
