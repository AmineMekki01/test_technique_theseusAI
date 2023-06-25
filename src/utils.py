import os
import openai


def get_api_key() -> str:
    """
    Fetches the OpenAI API key from the environment variables and returns it.
    """

    return os.getenv('OPENAI_API_KEY')

def setup_openai_api() -> None:
    """
    Sets up the OpenAI API using the API key.
    """
    openai.api_key = get_api_key()