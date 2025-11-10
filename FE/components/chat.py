import streamlit as st
from pathlib import Path

def _load_docs(docs_path: str) -> str:
    path = Path(docs_path)
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""

def chat_interface():
    if "docs_path" not in st.session_state:
        st.info("Generate documentation first to ask questions about the codebase.")
        return

    docs = _load_docs(st.session_state.docs_path)
    if not docs:
        st.warning("No documentation loaded.")
        return

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Show history
    for role, msg in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(msg)

    prompt = st.chat_input("Ask something about this repository...")
    if not prompt:
        return

    # Naive helper using the generated docs as guidance text.
    # (You can later upgrade this to call Gemini again if allowed.)
    answer = (
        "Here's how to approach it based on the generated documentation:\n\n"
        "- Check the **Overview** to confirm the repo's purpose.\n"
        "- Look at the **Repository Structure** and **Key Files** sections for relevant modules.\n"
        "- Use **How to Run Locally** for setup/commands.\n"
        "- Refer to **Possible Improvements** for refactoring ideas.\n\n"
        "For the specific answer, read the sections that mention the components you're asking about."
    )

    st.session_state.chat_history.append(("user", prompt))
    st.session_state.chat_history.append(("assistant", answer))

    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        st.markdown(answer)
