from pathlib import Path
import streamlit as st

def docs_viewer(docs_path: str):
    path = Path(docs_path)
    if not path.exists():
        st.error("Documentation file not found.")
        return

    content = path.read_text(encoding="utf-8")
    st.markdown("### Generated Documentation")
    st.markdown(content)
