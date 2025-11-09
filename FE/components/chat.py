import streamlit as st
import requests

CHAT_API = "http://localhost:8080/chat"

def chat_interface():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask about functions, architecture, or usage..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    resp = requests.post(
                        CHAT_API,
                        json={
                            "message": prompt,
                            "context": st.session_state.get("docs_path", "")
                        },
                        timeout=60
                    )
                    answer = resp.json().get("answer", "No response.")
                except:
                    answer = "Chat backend not available."

                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})