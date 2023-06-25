import tiktoken
import re


def create_chunks(text : str, max_tokens: int = 500) -> list[str]:
    """
    Creates chunks of text that are less than or equal to the maximum number of tokens.

    Parameters :
    ----------
    text : str
        The text to split into chunks.
        
    max_tokens : int
        The maximum number of tokens per chunk.
        
    Returns
    -------
    
    A list containing all of the chunks created from splitting `text` up.
    
    """
    
    # Initialize the tiktoken tokenizer using cl100k_base (chatGPT-3.5)
    encoding = tiktoken.get_encoding("cl100k_base")

    # Split the text into sentences
    sentences = re.split('(?<=[.!?]) +', text)

    chunks = []
    current_chunk = ""
    current_count = 0

    # Loop through each sentence
    for sentence in sentences:
        # Tokenize the sentence and get the count
        tokens = encoding.encode(sentence)
        token_count = len(tokens)

        # If adding the current sentence does not exceed the maximum, add it to the current chunk
        if current_count + token_count <= max_tokens:
            current_chunk += " " + sentence
            current_count += token_count
        else:
            # If it does exceed the maximum, start a new chunk
            chunks.append(current_chunk)
            current_chunk = sentence
            current_count = token_count

    # Add the final chunk
    chunks.append(current_chunk)

    return chunks
