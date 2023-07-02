import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain



# import from local modules 
from utils import get_api_key, setup_openai_api

# OpenAI API
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


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
  
def create_vector_store(chunks : list[str], embeddings : OpenAIEmbeddings) -> FAISS:
    
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



def chunks_similarity_research(vectorStore : FAISS, query : str, chunks_number : int = 3) -> list:
    
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


def get_answer(query : str, similar_chunks_object : list) -> str:
    
    """
        Get the answer to the query from the most similar chunks.
  
        Parameters:
        ----------
        query : str
            The query to find the most similar chunks to.
            
        similar_chunks_object : list[object]  
            The most similar chunks to the query. A list of objects that have all informations about the chunks including their content.

        Returns:
        -------
        answer : str
            The answer to the query.
            
    """
    
    chain = load_qa_chain(OpenAI(),
                          chain_type="stuff"
                        )
    
    return chain.run(input_documents = similar_chunks_object, question = query)