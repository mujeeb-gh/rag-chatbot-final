import time
import streamlit
from src.llm import groq_chat, openrouter_chat
from src.template import CHAT_TEMPLATE, INTENT_CLASSIFIER_TEMPLATE, RAG_TEMPLATE, RAG_EVAL_TEMPLATE


CLASSIFIER_INTENTS: list[str] = [
    # "greeting",
    # "goodbye",
    # "compliment",
    # "feedback",
    "open-ended",
    "query",
    "out-of-scope"
]

import re

def extract_intent(text):
    """
    Extracts the intent from the given text.
    
    Args:
        text (str): The text to search for an intent.
    
    Returns:
        str: The extracted intent ('open-ended', 'query', 'out of scope') if found, otherwise None.
    """
    # Define the regex pattern to match any of the intents
    pattern = r'\b(open-ended|query|out-of-scope)\b'
    
    # Search for the pattern in the input text (case insensitive)
    match = re.search(pattern, text, re.IGNORECASE)
    
    # Return the matched intent if found, else None
    if match:
        return match.group(1).lower()
    else:
        return None

def astra_chat(message: str, chat_history: list[dict] | None = None) -> str:
    """
    Function to chat with the Astra chatbot.

    Args:
        message (str): The message to be sent to the chatbot.
        chat_history (list[dict] | None = None): The chat history. Defaults to None.

    Returns:
        str: The response from the chatbot.
    """
    return openrouter_chat(
        message=message,
        preamble=CHAT_TEMPLATE,
        # model="mixtral-8x7b-32768",
        chat_history=chat_history,
    ).choices[0].message.content


def astra_rag(
    prompt: str, context: list[str], chat_history: list[dict] | None = None
) -> str:
    """
    Generates a response using the RAG (Retrieve, Augment, Generate) model.

    Args:
        prompt (str): The prompt for generating the response.
        context (list[str]): The context information used for generating the response.
        chat_history (list[ChatMessage] | None, optional): The chat history. Defaults to None.

    Returns:
        str: The generated response.

    """
    return openrouter_chat(
        message=prompt,
        preamble=RAG_TEMPLATE.format(context="\n\n".join(context)),
        # model="mixtral-8x7b-32768",
        chat_history=chat_history,
    ).choices[0].message.content


def astra_rag_eval(
    prompt: str, context: list[str], chat_history: list[dict] | None = None
) -> str:
    """
    Generates a response using the RAG (Retrieve, Augment, Generate) model.

    Args:
        prompt (str): The prompt for generating the response.
        context (list[str]): The context information used for generating the response.
        chat_history (list[ChatMessage] | None, optional): The chat history. Defaults to None.

    Returns:
        str: The generated response.

    """
    return openrouter_chat(
        message=prompt,
        preamble=RAG_EVAL_TEMPLATE.format(context="\n\n".join(context)),
        # model="mixtral-8x7b-32768",
        chat_history=chat_history,
    ).choices[0].message.content

def astra_intent_classifier(prompt: str) -> str:
    """
    Classifies the intent of the given prompt using the Astra intent classifier.

    Args:
        prompt (str): The prompt to classify.

    Returns:
        str: The classified intent.

    """
    response = openrouter_chat(
        message=prompt,
        preamble=INTENT_CLASSIFIER_TEMPLATE.format(
            intents="- ".join([f"{intent}\n" for intent in CLASSIFIER_INTENTS])
        ),
        # model="mixtral-8x7b-32768",
    )
    
    if "error" in response:
        # Handle the error gracefully by returning a default message or intent
        return response["error"]
    
    return response.choices[0].message.content
    
def astra_stream(response: str):
    for word in response.split(" "):
        yield word + " "
        time.sleep(0.02)
# Example Usage
# print(astra_chat("hi"), "\n")
# print(astra_rag("what is my company's name?", context=["I own Apple.inc"]), "\n")
# print(astra_intent_classifier("Hello there!"), "\n")
