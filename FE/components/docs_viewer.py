import streamlit as st
import markdown
import os

def docs_viewer(md_path: str):
    if not os.path.exists(md_path):
        st.warning("Documentation file not found.")
        return

    raw_md = open(md_path, "r", encoding="utf-8").read()
    
    # Convert Mermaid to HTML (Streamlit supports via markdown-it)
    html = markdown.markdown(
        raw_md,
        extensions=['fenced_code', 'tables', 'nl2br', 'codehilite']
    )

    # Inject Mermaid.js
    mermaid_html = """
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>mermaid.initialize({startOnLoad:true});</script>
    """
    full_html = f"<div class='markdown-body'>{html}</div>{mermaid_html}"

    st.markdown(full_html, unsafe_allow_html=True)