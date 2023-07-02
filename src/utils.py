import os
import openai
from pypdf import PdfReader
from enum import Enum
class FileType(Enum):
    PDF = ".pdf"
    TXT = ".txt"


def get_api_key():
    """
    Fetches the OpenAI API key from the environment variables and returns it.
    """

    return os.getenv('OPENAI_API_KEY')

def setup_openai_api() -> None:
    """
    Sets up the OpenAI API using the API key.
    """
    openai.api_key = get_api_key()
    
def parse_pdf(file):
    """
    Parses a pdf file and returns the text.
    
    Parameters:
    ----------
    file : UploadFile
    
    Returns:
    -------
    text : str
    """
    pdf = PdfReader(file.file)
    output = []
    for page in pdf.pages:
        text = page.extract_text()
        output.append(text)

    return "\n\n".join(output)

def get_file_type(filename: str) -> FileType:
    """
    Returns the file type based on the filename.

    Parameters:
    ----------
    filename : str
    
    Returns:
    -------
    FileType or None
    """
    if filename.endswith(".pdf"):
        return FileType.PDF
    elif filename.endswith(".txt"):
        return FileType.TXT
    else:
        return None