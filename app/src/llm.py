from typing import Literal 
from groq import Groq, InternalServerError
from openai import OpenAI, InternalServerError as OpenaiInternalServerError
from src.settings import settings
from dotenv import load_dotenv
import os

load_dotenv()

CHAT_MODEL = Literal["llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768", "gemma-7b-it"]
groq_api_key = os.getenv('GROQ_API_KEY')
openrouter_api_key = os.getenv('OPENROUTER_API_KEY')

client = Groq(
    api_key=groq_api_key,
)

openrouter_client = OpenAI(
    base_url = "https://openrouter.ai/api/v1",
    api_key=openrouter_api_key
)

def groq_chat(
    message: str,
    preamble: str,
    model: CHAT_MODEL = "mixtral-8x7b-32768",
    temperature: float = 0.5,
    max_tokens: int = 1024,
    top_p: float = 1,
    stop: str | None = None,
    stream: bool = False,
    chat_history: list[dict] | None = None,
) -> dict:
    """
    Sends a chat message to the Groq LLM and returns the response.

    Args:
        message (str): The user message to be sent to the LLM.
        preamble (str): The system message that sets the behavior of the assistant.
        model (str, optional): The language model which will generate the completion. Defaults to "mixtral-8x7b-32768".
        temperature (float, optional): Controls randomness. Defaults to 0.5.
        max_tokens (int, optional): The maximum number of tokens to generate. Defaults to 1024.
        top_p (float, optional): Controls diversity via nucleus sampling. Defaults to 1.
        stop (str | None, optional): A stop sequence to signal the LLM to stop generating content. Defaults to None.
        stream (bool, optional): If set, partial message deltas will be sent. Defaults to False.
        chat_history (list[dict] | None, optional): The chat history to be used for the conversation. Defaults to None.

    Returns:
        dict: The response from the LLM.
    """
    # Prepare the messages for the chat completion
    messages = []
    messages.append({
            "role": "system",
            "content": preamble
        })
    if chat_history:
        messages.extend(chat_history)
    messages.append({
        "role": "user",
        "content": message
    })

    # Create the chat completion
    try:
        chat_completion = client.chat.completions.create(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stop=stop,
            stream=stream,
        )

        # Return the response
        return chat_completion
    except InternalServerError:
        return{"error": "Groq server is currently unavailable. Please try again later."}

def openrouter_chat(
    message: str,
    preamble: str,
    model: CHAT_MODEL = "mistralai/mixtral-8x7b-instruct",
    temperature: float = 0.5,
    max_tokens: int = 1024,
    top_p: float = 1,
    stop: str | None = None,
    stream: bool = False,
    chat_history: list[dict] | None = None
) -> dict:
    messages = []
    messages.append({
            "role": "system",
            "content": preamble
        })
    if chat_history:
        messages.extend(chat_history)
    messages.append({
        "role": "user",
        "content": message
    })
    
    try:
        chat_completion = openrouter_client.chat.completions.create(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stop=stop,
            stream=stream,
        )

        # Return the response
        return chat_completion
    except OpenaiInternalServerError:
        return{"error": "Groq server is currently unavailable. Please try again later."}


# # Example usage
# response = groq_chat(
#     message="Tell me a joke",
#     preamble="you are a helpful assistant."
# )
# print(response)