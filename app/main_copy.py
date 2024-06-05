from typing import Any

import streamlit as st
from src.chroma import search
from src.astra import astra_chat, astra_intent_classifier, astra_rag
from pprint import pprint as pprint

st.set_page_config(page_title="Astra", page_icon="🗨️", layout="centered")

st.title(":grey[Astra]")
st.subheader("Development of a Chatbot for Scholarly Research using Retrieval Augmented Generation \n Balogun Olamide Abdulmujeeb \n\n 20/SCI01/042", divider="grey", anchor=False)


if "messages" not in st.session_state:
    _messages: list[Any] = []
    st.session_state.messages = _messages

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type a Message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        chat_history: Any | None = (
            st.session_state.messages[-3:] if st.session_state.messages else None
        )
        intent: str = astra_intent_classifier(prompt).strip()
        print(f"\n\n{intent}\n")

        if intent == "query" or intent == "inquiry":
            context: list[dict[str, Any]] | None = search(query=prompt, k=3)

            # Check if there are any results
            if not context:
                response: str = "I'm sorry, I don't have any information on that. Feel free to ask me anything else."

                st.markdown(response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )
            else:
                response: str = astra_rag(
                    prompt,
                    context=[f"{result['doc']} \npaper title:{result['metadata']['title']} \npaper URL:{result['metadata']['url']}" for result in context],
                    chat_history= chat_history
                )
                print(f"\n{chat_history}\nRAG used\n")
                pprint(context)

                st.markdown(response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )
        else:
            response: str = astra_chat(
                prompt,
                chat_history= chat_history
            )
            print(chat_history, "\nLLM used\n\n")

            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
