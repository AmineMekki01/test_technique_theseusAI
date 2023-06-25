import tiktoken
import re


def create_chunks(text : str, max_tokens: int = 500):
    
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
